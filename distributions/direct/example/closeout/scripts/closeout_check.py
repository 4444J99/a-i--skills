#!/usr/bin/env python3
"""Read-only closeout inventory and durable-ownership checks (Python stdlib only)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit, urlunsplit

OBSERVATIONS: list[str] = []
READBACK_CACHE: dict[str, Any] = {}
GIT_LOCATION_VARS = {
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_PREFIX",
    "GIT_NAMESPACE",
    "GIT_CEILING_DIRECTORIES",
    "GIT_IMPLICIT_WORK_TREE",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
}
MAX_INVENTORY_PATHS = 10000


def observation_env() -> dict[str, str]:
    return {
        **{
            key: value
            for key, value in os.environ.items()
            if key not in GIT_LOCATION_VARS
        },
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_GRAFT_FILE": os.devnull,
    }


class Unmeasured(Exception):
    """A required observation was unavailable."""


def digest(value: Any) -> str:
    data = (
        value
        if isinstance(value, bytes)
        else json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode()
    )
    return hashlib.sha256(data).hexdigest()


def run(
    args: list[str], root: str | Path | None = None, *, input_data: bytes | None = None
) -> bytes:
    try:
        result = subprocess.run(
            args,
            cwd=root,
            input=input_data,
            check=False,
            capture_output=True,
            timeout=30,
            env=observation_env(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unmeasured(f"{args[0]} unavailable: {type(exc).__name__}") from exc
    if result.returncode:
        raise Unmeasured(f"{args[0]} observation failed (exit {result.returncode})")
    if "ls-remote" in args or "show" in args or args[:2] == ["gh", "api"]:
        OBSERVATIONS.append(digest({"args": args, "stdout": digest(result.stdout)}))
    return result.stdout


def git(root: str | Path, *args: str) -> bytes:
    if args and args[0] == "diff":
        args = (args[0], "--no-ext-diff", "--no-textconv", *args[1:])
    return run(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args])


def safe_url(url: str) -> str:
    """Never project remote credentials, query parameters or fragments."""
    if "://" not in url:
        return url.rstrip("/")
    try:
        parsed = urlsplit(url)
        host = parsed.hostname or ""
        if ":" in host:
            host = "[" + host + "]"
        if parsed.port:
            host += ":" + str(parsed.port)
        return urlunsplit((parsed.scheme, host, parsed.path.rstrip("/"), "", ""))
    except ValueError as exc:
        raise Unmeasured("remote URL could not be classified") from exc


def identity(url: str) -> str:
    value = safe_url(url.strip()).removesuffix(".git")
    if "://" in value:
        parsed = urlsplit(value)
        if parsed.hostname == "github.com" and parsed.port in (None, 22, 443):
            return "github.com/" + parsed.path.strip("/").lower()
    match = re.fullmatch(r"git@github.com:(.+)", value)
    return "github.com/" + match[1].lower() if match else value


def github_repo(repository: str) -> str:
    if not repository.startswith("github.com/"):
        raise Unmeasured("authenticated GitHub evidence unsupported for this remote")
    return repository.removeprefix("github.com/")


def gh_json(endpoint: str) -> Any:
    try:
        return json.loads(run(["gh", "api", "--hostname", "github.com", endpoint]))
    except (ValueError, UnicodeError) as exc:
        raise Unmeasured("GitHub returned invalid JSON") from exc


def discover(
    root: str | Path,
    invoked: str | Path | None = None,
    working_directory: str | Path | None = None,
) -> dict[str, str] | None:
    """Skip only the invoked file and byte-identical copies, never descriptions."""
    root = Path(root)
    invoked = Path(invoked or Path(__file__).resolve().parents[1] / "SKILL.md")
    own = invoked.read_bytes() if invoked.is_file() else None
    for directory in (".agents", ".codex", ".claude"):
        path = root / directory / "skills/closeout/SKILL.md"
        if path.is_file():
            if path.resolve() == invoked.resolve() or (
                own is not None and path.read_bytes() == own
            ):
                continue
            return {"kind": "skill", "path": str(path)}
    directory = Path(working_directory or root).resolve()
    root = root.resolve()
    if not directory.is_relative_to(root):
        raise Unmeasured("working_directory must be contained by its scoped repository")
    while True:
        for name in ("AGENTS.md", "CLAUDE.md"):
            path = directory / name
            if path.is_file() and re.search(
                r"(?im)^#{1,6}\s+.*\b(closeout|session end|session close|session review)\b",
                path.read_text(),
            ):
                return {"kind": "instructions", "path": str(path)}
        if directory == root:
            break
        directory = directory.parent
    tracked = os.fsdecode(git(root, "ls-files", "-z")).split("\0")
    for name in sorted(tracked):
        if re.match(r"scripts/closeout[^/]*$|done\.sh$", name):
            return {"kind": "predicate", "path": str(root / name)}
    for name in ("Makefile", "package.json"):
        path = root / name
        if name not in tracked or not path.is_file():
            continue
        content = path.read_text()
        if (name == "Makefile" and re.search(r"(?m)^closeout\s*:", content)) or (
            name == "package.json"
            and "closeout" in json.loads(content).get("scripts", {})
        ):
            return {"kind": "predicate", "path": str(path)}
    return None


def organvm_overlay(root: str | Path) -> bool:
    """Only repository instruction sentinels and actual ledger locations opt in."""
    root = Path(root)
    tracked = set(os.fsdecode(git(root, "ls-files", "-z")).split("\0"))
    for name in ("AGENTS.md", "CLAUDE.md"):
        if (
            name in tracked
            and "<!-- ORGANVM:AUTO:START -->" in (root / name).read_text()
        ):
            return True
    ledger = "INST-INDEX-RERUM-FACIENDARUM.md"
    concrete_id = r"\b(?:DONE-\d{3,}|IRF-[A-Z]{2,}-\d{3,})\b"
    if ledger in tracked and re.search(concrete_id, (root / ledger).read_text()):
        return True
    for name in tracked:
        if re.match(r"\.(?:agents|codex|claude)/plans/[^/]+\.md$", name) and re.search(
            concrete_id, (root / name).read_text()
        ):
            return True
    return False


def remote_state(root: str | Path, selected: str | None = None) -> dict[str, str]:
    names = git(root, "remote").decode().splitlines()
    if selected is None:
        branch = git(root, "branch", "--show-current").decode().strip()
        configured = (
            subprocess.run(
                ["git", "-C", str(root), "config", "--get", f"branch.{branch}.remote"],
                check=False,
                capture_output=True,
                timeout=30,
                env=observation_env(),
            )
            .stdout.decode()
            .strip()
        )
        if configured in names:
            selected = configured
        elif len(names) == 1:
            selected = names[0]
        else:
            raise Unmeasured("remote must be explicit when absent or ambiguous")
    if selected not in names:
        raise Unmeasured("selected remote does not exist")
    url = git(root, "remote", "get-url", selected).decode().strip()
    parsed = urlsplit(url) if "://" in url else None
    local_path = None
    if parsed is not None and parsed.scheme == "file":
        if parsed.hostname not in (None, "", "localhost"):
            raise Unmeasured("non-local file remote cannot be classified")
        local_path = Path(unquote(parsed.path))
    elif parsed is None and not re.match(r"[^/]+:.+", url):
        local_path = Path(url).expanduser()
        if not local_path.is_absolute():
            local_path = Path(root) / local_path
    if local_path is not None:
        common = git(
            root, "rev-parse", "--path-format=absolute", "--git-common-dir"
        ).strip()
        remote_common = git(
            local_path.resolve(),
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ).strip()
        if (
            Path(os.fsdecode(common)).resolve()
            == Path(os.fsdecode(remote_common)).resolve()
        ):
            raise Unmeasured(
                "the scoped Git store cannot serve as its own remote publication"
            )
    rows = git(root, "ls-remote", "--symref", selected, "HEAD").decode().splitlines()
    default = next((r.split()[1] for r in rows if r.startswith("ref: ")), None)
    tip = next(
        (
            r.split()[0]
            for r in rows
            if r.endswith("\tHEAD") and not r.startswith("ref:")
        ),
        None,
    )
    if not default or not tip:
        raise Unmeasured("remote default branch could not be measured")
    return {
        "remote": selected,
        "url": safe_url(url),
        "repository": identity(url),
        "default_ref": default,
        "default_tip": tip,
    }


def file_digest(path: Path) -> str:
    if path.is_symlink():
        return digest(os.fsencode(os.readlink(path)))
    value = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                value.update(chunk)
    return value.hexdigest()


def require_filter_free_status(root: str | Path) -> None:
    """Do not execute repository clean/process programs during observation."""
    for entry in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if entry.startswith(b"160000 "):
            raise Unmeasured(
                "Git submodule content requires separately measured scoped observation"
            )
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "config",
                "--null",
                "--name-only",
                "--get-regexp",
                r"^filter\..*\.(clean|process)$",
            ],
            check=False,
            capture_output=True,
            timeout=30,
            env=observation_env(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unmeasured("Git filter configuration unavailable") from exc
    if result.returncode not in (0, 1):
        raise Unmeasured("Git filter configuration could not be measured")
    drivers = set()
    for key in os.fsdecode(result.stdout).split("\0"):
        match = re.fullmatch(r"filter\.(.*)\.(?:clean|process)", key)
        if match:
            drivers.add(match[1])
    if not drivers:
        return
    paths = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if len(paths.split(b"\0")) - 1 > MAX_INVENTORY_PATHS:
        raise Unmeasured("filter attribute census exceeds 10000 paths")
    attrs = run(
        [
            "git",
            "-c",
            "core.fsmonitor=false",
            "-C",
            str(root),
            "check-attr",
            "-z",
            "--stdin",
            "filter",
        ],
        input_data=paths,
    ).split(b"\0")
    for index in range(2, len(attrs), 3):
        if os.fsdecode(attrs[index]) in drivers:
            raise Unmeasured(
                "active Git content filter requires separately measured observation"
            )


def working_status(root: str | Path) -> bytes:
    """Include ignored outputs and content hidden by index flags without changing flags."""
    require_filter_free_status(root)
    data = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    known = set()
    chunks = data.split(b"\0")
    pos = 0
    while pos < len(chunks):
        entry = chunks[pos]
        pos += 1
        if not entry:
            continue
        known.add(entry[3:])
        if b"R" in entry[:2] or b"C" in entry[:2]:
            pos += 1
    additions = []
    for name in git(
        root, "ls-files", "--others", "--ignored", "--exclude-standard", "-z"
    ).split(b"\0"):
        if name and name not in known:
            additions.append(b"!! " + name + b"\0")
            known.add(name)
    for entry in git(root, "ls-files", "-v", "-z").split(b"\0"):
        if entry and (entry[:1].islower() or entry[:1] == b"S"):
            name = entry[2:]
            if name not in known:
                additions.append(b"F  " + name + b"\0")
                known.add(name)
    if len(known) > MAX_INVENTORY_PATHS:
        raise Unmeasured(
            "content census exceeds 10000 paths; measurement is incomplete"
        )
    return data + b"".join(additions)


def inventory(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise Unmeasured("evidence must be a JSON object")
    if document.get("schema") != "closeout.evidence.v1" or not document.get(
        "session_id"
    ):
        raise Unmeasured("schema and native session_id are required")
    if not isinstance(document.get("non_file_obligations"), list):
        raise Unmeasured(
            "declare non_file_obligations explicitly, including an empty list"
        )
    if not isinstance(document.get("scopes"), list) or not document["scopes"]:
        raise Unmeasured("at least one scoped repository is required")
    scopes, items, seen = {}, [], set()

    def add(scope: str, kind: str, key: str, content: Any) -> None:
        item_id = f"{scope}:{kind}:{key}"
        items.append(
            {
                "id": item_id,
                "scope": scope,
                "kind": kind,
                "fingerprint": digest(content),
                "content": content,
            }
        )

    for scope in document["scopes"]:
        sid = scope["id"]
        if sid in seen:
            raise Unmeasured("duplicate scope id")
        seen.add(sid)
        root = Path(scope["root"]).expanduser().resolve(strict=True)
        actual = Path(
            git(root, "rev-parse", "--show-toplevel").decode().strip()
        ).resolve()
        if root != actual:
            raise Unmeasured("scope root must be its actual repository root")
        if "base" not in scope:
            raise Unmeasured("every scope requires its exact session base")
        base = (
            git(root, "rev-parse", "--verify", scope["base"] + "^{commit}")
            .decode()
            .strip()
        )
        if base != scope["base"]:
            raise Unmeasured("session base must be a full immutable commit hash")
        ancestry = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", base, "HEAD"],
            check=False,
            capture_output=True,
            timeout=30,
            env=observation_env(),
        )
        if ancestry.returncode:
            raise Unmeasured("session base is not an ancestor of the scoped HEAD")
        state = remote_state(root, scope.get("remote"))
        baseline_ref = scope.get("base_ref", state["default_ref"])
        if not baseline_ref.startswith("refs/heads/"):
            raise Unmeasured("base_ref must be a published branch")
        published = (
            git(root, "ls-remote", state["remote"], baseline_ref).decode().splitlines()
        )
        if len(published) != 1:
            raise Unmeasured("session base provenance branch unavailable")
        published_tip = published[0].split()[0]
        base_proof = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "merge-base",
                "--is-ancestor",
                base,
                published_tip,
            ],
            check=False,
            capture_output=True,
            timeout=30,
            env=observation_env(),
        )
        if base_proof.returncode:
            raise Unmeasured(
                "session base is not proven in its published baseline branch"
            )
        head = git(root, "rev-parse", "HEAD").decode().strip()
        upstream = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "rev-parse",
                "--abbrev-ref",
                "--symbolic-full-name",
                "@{u}",
            ],
            check=False,
            capture_output=True,
            timeout=30,
            env=observation_env(),
        )
        scopes[sid] = {
            **state,
            "root": str(root),
            "base": base,
            "head": head,
            "upstream": upstream.stdout.decode().strip()
            if upstream.returncode == 0
            else None,
            "protocol": discover(
                root, working_directory=scope.get("working_directory")
            ),
            "organvm_overlay": organvm_overlay(root),
        }
        entries = working_status(root).split(b"\0")
        index = 0
        while index < len(entries):
            entry = entries[index]
            index += 1
            if not entry:
                continue
            status, name = entry[:2].decode(), os.fsdecode(entry[3:])
            if (root / name).is_dir() and not (root / name).is_symlink():
                raise Unmeasured(
                    "changed submodule/directory requires its own declared repository scope"
                )
            previous = None
            if "R" in status or "C" in status:
                previous = os.fsdecode(entries[index])
                index += 1
            add(
                sid,
                "file",
                name,
                {
                    "path": name,
                    "status": status,
                    "previous": previous,
                    "bytes": file_digest(root / name),
                    "index": digest(
                        git(root, "diff", "--cached", "--binary", "--", name)
                    ),
                    "mode": (root / name).lstat().st_mode
                    if (root / name).exists() or (root / name).is_symlink()
                    else None,
                },
            )
        for commit in git(root, "rev-list", base + "..HEAD").decode().splitlines():
            add(sid, "commit", commit, {"sha": commit})
        known_commits = {
            row["content"]["sha"]
            for row in items
            if row["scope"] == sid and row["kind"] == "commit"
        }
        local_branches = set()
        for row in os.fsdecode(
            git(
                root, "for-each-ref", "--format=%(objectname) %(refname)", "refs/heads/"
            )
        ).splitlines():
            tip, ref = row.split(" ", 1)
            local_branches.add(ref.removeprefix("refs/heads/"))
            commits = (
                git(root, "rev-list", tip, "--not", state["default_tip"])
                .decode()
                .splitlines()
            )
            if ref != state["default_ref"] or commits:
                add(sid, "branch", ref, {"ref": ref, "sha": tip})
            for commit in commits:
                if commit not in known_commits:
                    add(sid, "commit", commit, {"sha": commit})
                    known_commits.add(commit)
        if state["repository"].startswith("github.com/"):
            repository = github_repo(state["repository"])
            for page in range(1, 21):
                pulls = gh_json(
                    f"repos/{repository}/pulls?state=open&per_page=100&page={page}"
                )
                if not isinstance(pulls, list):
                    raise Unmeasured("GitHub PR inventory returned an invalid list")
                for pull in pulls:
                    head_data = pull.get("head", {})
                    repo_data = head_data.get("repo") or {}
                    if (
                        repo_data.get("full_name", "").lower() == repository.lower()
                        and head_data.get("ref") in local_branches
                    ):
                        add(
                            sid,
                            "pull-request",
                            str(pull["number"]),
                            {
                                "number": pull["number"],
                                "head": head_data.get("sha"),
                                "branch": head_data.get("ref"),
                                "body": digest(pull.get("body") or ""),
                                "state": pull.get("state"),
                            },
                        )
                if len(pulls) < 100:
                    break
            else:
                raise Unmeasured("GitHub PR inventory exceeded 2000 open records")
        for stash in git(root, "stash", "list", "--format=%H").decode().splitlines():
            add(sid, "stash", stash, {"sha": stash})
        for record in (
            git(root, "worktree", "list", "--porcelain").decode().strip().split("\n\n")
        ):
            fields = dict(
                line.split(" ", 1) if " " in line else (line, "")
                for line in record.splitlines()
            )
            path = fields.get("worktree")
            # A pristine caller at its declared session base predates this work.
            if (
                path == str(root)
                and head == base
                and not any(x["scope"] == sid for x in items)
            ):
                continue
            if path and "bare" not in fields:
                sibling = Path(path)
                if not sibling.is_dir():
                    raise Unmeasured(
                        "registered worktree unavailable for content measurement"
                    )
                statuses = working_status(sibling)
                fields["status"] = digest(statuses)
                changed = []
                chunks = statuses.split(b"\0")
                pos = 0
                while pos < len(chunks):
                    chunk = chunks[pos]
                    pos += 1
                    if not chunk:
                        continue
                    name = os.fsdecode(chunk[3:])
                    target = sibling / name
                    if target.is_dir() and not target.is_symlink():
                        raise Unmeasured("sibling submodule requires explicit scope")
                    changed.append(
                        {
                            "path": name,
                            "content": file_digest(target),
                            "mode": target.lstat().st_mode
                            if target.exists() or target.is_symlink()
                            else None,
                            "index": digest(
                                git(sibling, "diff", "--cached", "--binary", "--", name)
                            ),
                        }
                    )
                    if b"R" in chunk[:2] or b"C" in chunk[:2]:
                        pos += 1
                fields["changes"] = changed
                add(sid, "worktree", path, fields)
    for obligation in document["non_file_obligations"]:
        if not isinstance(obligation, dict) or not all(
            isinstance(obligation.get(k), str) and obligation[k]
            for k in ("id", "scope", "description")
        ):
            raise Unmeasured(
                "non-file obligations require id, scope, and substantive description"
            )
        if obligation["scope"] not in scopes:
            raise Unmeasured("non-file obligation references unknown scope")
        add(obligation["scope"], "declared", obligation["id"], obligation)
    if len({item["id"] for item in items}) != len(items):
        raise Unmeasured("duplicate inventory item")
    snapshot = {
        "session_id": document["session_id"],
        "scopes": scopes,
        "items": sorted(items, key=lambda x: x["id"]),
    }
    return {**snapshot, "fingerprint": digest(snapshot)}


def binding(session: str, repository: str, item: dict[str, Any]) -> dict[str, str]:
    return {
        "session_id": session,
        "repository": repository,
        "item_id": item["id"],
        "fingerprint": item["fingerprint"],
    }


def validate_record(record: Any, expected: dict[str, str], disposition: str) -> bool:
    if not isinstance(record, dict) or record.get("binding") != expected:
        return False
    if record.get("disposition") != disposition:
        return False
    if disposition == "excluded":
        return bool(
            isinstance(record.get("rationale"), str)
            and record["rationale"].strip()
            and isinstance(record.get("source_session"), str)
            and record["source_session"].strip()
            and record["source_session"] != expected["session_id"]
        )
    return all(
        isinstance(record.get(key), str) and record[key].strip()
        for key in ("owner", "next_action")
    )


def _read_record(owner: dict[str, Any], state: dict[str, Any]) -> Any:
    kind = owner.get("kind")
    if kind == "git-record":
        ref, path = owner["ref"], owner["path"]
        if (
            not ref.startswith("refs/heads/")
            or path.startswith("/")
            or ".." in Path(path).parts
        ):
            raise Unmeasured(
                "git owner requires a branch ref and repository-relative record path"
            )
        rows = (
            git(state["root"], "ls-remote", state["remote"], ref).decode().splitlines()
        )
        if len(rows) != 1:
            raise Unmeasured("owner branch absent or ambiguous on remote")
        tip = rows[0].split()[0]
        content = git(state["root"], "show", f"{tip}:{path}")
        try:
            return json.loads(content)
        except ValueError as exc:
            raise Unmeasured("pushed owner record is not JSON") from exc
    if kind in ("github-issue", "github-pr"):
        repo = github_repo(state["repository"])
        if owner.get("repository", state["repository"]) != state["repository"]:
            raise Unmeasured("owner repository identity mismatch")
        number = int(owner["number"])
        endpoint = "issues" if kind == "github-issue" else "pulls"
        data = gh_json(f"repos/{repo}/{endpoint}/{number}")
        if data.get("state") != "open" or (
            kind == "github-pr" and data.get("merged_at")
        ):
            return None
        body = data.get("body") or ""
        match = re.search(r"<!-- closeout-owner\s*\n(.*?)\n-->", body, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match[1])
        except ValueError:
            return None
    raise Unmeasured("unsupported durable owner kind")


def read_record(owner: dict[str, Any], state: dict[str, Any]) -> Any:
    reference = {
        key: owner.get(key) for key in ("kind", "repository", "ref", "path", "number")
    }
    key = digest(
        {
            "reference": reference,
            "root": state.get("root"),
            "remote": state.get("remote"),
            "repository": state["repository"],
        }
    )
    if key not in READBACK_CACHE:
        try:
            READBACK_CACHE[key] = _read_record(owner, state)
        except (
            Unmeasured,
            OSError,
            ValueError,
            KeyError,
            TypeError,
            AttributeError,
            subprocess.TimeoutExpired,
        ) as exc:
            READBACK_CACHE[key] = Unmeasured(str(exc))
    result = READBACK_CACHE[key]
    if isinstance(result, Unmeasured):
        raise result
    return result


def landed(owner: dict[str, Any], state: dict[str, Any], item: dict[str, Any]) -> bool:
    if item["kind"] not in ("commit", "branch"):
        raise Unmeasured("landing proof applies only to commit obligations")
    sha = item["content"]["sha"]
    if owner.get("pull_request") is not None:
        repo = github_repo(state["repository"])
        number = int(owner["pull_request"])
        data = gh_json(f"repos/{repo}/pulls/{number}")
        if data.get("state") != "closed" or not data.get("merged_at"):
            return False
        if (
            identity(data.get("base", {}).get("repo", {}).get("clone_url", ""))
            != state["repository"]
        ):
            return False
        # Read every page; a squash landing binds the original commit to its repository-qualified PR.
        commits = []
        for page in range(1, 101):
            batch = gh_json(
                f"repos/{repo}/pulls/{number}/commits?per_page=100&page={page}"
            )
            if not isinstance(batch, list):
                raise Unmeasured("invalid PR commit list")
            commits.extend(row["sha"] for row in batch)
            if len(batch) < 100:
                break
        else:
            raise Unmeasured("PR commit list exceeded bounded measurement")
        if sha not in commits:
            return False
        sha = data["merge_commit_sha"]
    result = subprocess.run(
        [
            "git",
            "-C",
            state["root"],
            "merge-base",
            "--is-ancestor",
            sha,
            state["default_tip"],
        ],
        check=False,
        capture_output=True,
        timeout=30,
        env=observation_env(),
    )
    if result.returncode not in (0, 1):
        raise Unmeasured(
            "remote landing commit/default objects unavailable locally; fetch before checking"
        )
    return result.returncode == 0


def check(document: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    OBSERVATIONS.clear()
    READBACK_CACHE.clear()
    snapshot = inventory(document)
    owners = document.get("owners")
    if not isinstance(owners, dict):
        raise Unmeasured("owners must map inventory ids to evidence references")
    dangling, unmeasured, verified = [], [], []
    for item in snapshot["items"]:
        owner = owners.get(item["id"])
        if not isinstance(owner, dict):
            dangling.append({"id": item["id"], "reason": "missing-owner"})
            continue
        state = snapshot["scopes"][item["scope"]]
        if owner.get("fingerprint") != item["fingerprint"]:
            dangling.append({"id": item["id"], "reason": "stale-item-binding"})
            continue
        try:
            if owner.get("kind") == "landed":
                valid = landed(owner, state, item)
            else:
                record = read_record(owner, state)
                records = record if isinstance(record, list) else [record]
                expected = binding(document["session_id"], state["repository"], item)
                disposition = owner.get("disposition", "owned")
                valid = disposition in ("owned", "excluded") and any(
                    validate_record(row, expected, disposition) for row in records
                )
                if valid and disposition == "excluded":
                    matching = next(
                        row
                        for row in records
                        if validate_record(row, expected, disposition)
                    )
                    source = matching.get("source_evidence")
                    if not isinstance(source, dict):
                        valid = False
                    else:
                        source_record = read_record(source, state)
                        source_records = (
                            source_record
                            if isinstance(source_record, list)
                            else [source_record]
                        )
                        source_binding = {
                            **expected,
                            "session_id": matching["source_session"],
                        }
                        valid = any(
                            validate_record(row, source_binding, "owned")
                            for row in source_records
                        )
                OBSERVATIONS.append(digest(record))
            (verified if valid else dangling).append(
                {
                    "id": item["id"],
                    "reason": "verified"
                    if valid
                    else "remote-record-does-not-own-item",
                }
            )
        except (
            Unmeasured,
            KeyError,
            ValueError,
            OSError,
            TypeError,
            AttributeError,
            subprocess.TimeoutExpired,
        ) as exc:
            unmeasured.append({"id": item["id"], "reason": str(exc)})
    code = 2 if unmeasured else 1 if dangling else 0
    return code, {
        "schema": "closeout.result.v1",
        "operation": "check",
        "status": ("owned", "dangling", "unmeasured")[code],
        "session_id": document["session_id"],
        "inventory_fingerprint": snapshot["fingerprint"],
        "evidence_fingerprint": digest(document),
        "readback_fingerprint": digest(OBSERVATIONS),
        "verified": verified,
        "dangling": dangling,
        "unmeasured": unmeasured,
        "session_released": False,
        "note": "Ownership only. Repository session predicates retain their authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("inventory", "check"))
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument(
        "--twice",
        action="store_true",
        help="perform two fresh checks and require an unchanged fixed point",
    )
    args = parser.parse_args()
    try:
        document = json.loads(args.evidence.read_text())
        if args.operation == "inventory":
            result, code = {"schema": "closeout.inventory.v1", **inventory(document)}, 0
        else:
            code, result = check(document)
            if args.twice and code == 0:
                second_document = json.loads(args.evidence.read_text())
                second_code, second = check(second_document)
                stable = (
                    second_code == 0
                    and second["inventory_fingerprint"]
                    == result["inventory_fingerprint"]
                    and second["evidence_fingerprint"] == result["evidence_fingerprint"]
                    and second["readback_fingerprint"] == result["readback_fingerprint"]
                )
                result = {**second, "passes": [code, second_code], "stable": stable}
                code = second_code if second_code else 0 if stable else 2
                if not stable:
                    result["status"] = "unmeasured" if code == 2 else second["status"]
                    result["reason"] = "ownership or evidence changed between passes"
    except (
        Unmeasured,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        subprocess.TimeoutExpired,
    ) as exc:
        code, result = (
            2,
            {
                "schema": "closeout.result.v1",
                "operation": args.operation,
                "status": "unmeasured",
                "reason": str(exc),
                "session_released": False,
            },
        )
    print(json.dumps(result, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
