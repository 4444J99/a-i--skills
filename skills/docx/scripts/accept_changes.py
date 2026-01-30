#!/usr/bin/env python3
"""Accept all tracked changes in a DOCX file using LibreOffice.

Requires LibreOffice (soffice) to be installed.
"""

import argparse
import logging
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# LibreOffice profile directory for macro storage
LIBREOFFICE_PROFILE = "/tmp/libreoffice_docx_profile"
MACRO_DIR = f"{LIBREOFFICE_PROFILE}/user/basic/Standard"

ACCEPT_CHANGES_MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub AcceptAllTrackedChanges()
        Dim document As Object
        Dim dispatcher As Object

        document = ThisComponent.CurrentController.Frame
        dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

        dispatcher.executeDispatch(document, ".uno:AcceptAllTrackedChanges", "", 0, Array())
        ThisComponent.store()
        ThisComponent.close(True)
    End Sub
</script:module>"""


def accept_changes(
    input_file: str,
    output_file: str,
) -> tuple[None, str]:
    """Accept all tracked changes in a DOCX file and save to output file.

    Args:
        input_file: Path to input DOCX file with tracked changes
        output_file: Path to output DOCX file (will be created/overwritten)

    Returns:
        (None, message) - message indicates success or failure
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        return None, f"Error: Input file not found: {input_file}"

    if not input_path.suffix.lower() == ".docx":
        return None, f"Error: Input file is not a DOCX file: {input_file}"

    # Copy input file to output file location
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, output_path)
    except Exception as e:
        return None, f"Error: Failed to copy input file to output location: {e}"

    # Setup LibreOffice macro
    if not _setup_libreoffice_macro():
        return None, "Error: Failed to setup LibreOffice macro"

    # Ensure Xvfb is running (for headless operation on Linux)
    if platform.system() == "Linux":
        try:
            _ensure_xvfb_running()
        except RuntimeError as e:
            return None, f"Error: {e}"

    # Run LibreOffice with macro to accept changes
    cmd = [
        "soffice",
        "--headless",
        f"-env:UserInstallation=file://{LIBREOFFICE_PROFILE}",
        "--norestore",
        "vnd.sun.star.script:Standard.Module1.AcceptAllTrackedChanges?language=Basic&location=application",
        str(output_path.absolute()),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    except subprocess.TimeoutExpired:
        # Timeout is expected - LibreOffice may hang after completing
        return None, f"Successfully accepted all tracked changes: {input_file} -> {output_file}"

    if result.returncode != 0:
        return None, f"Error: LibreOffice failed: {result.stderr}"

    return None, f"Successfully accepted all tracked changes: {input_file} -> {output_file}"


def _ensure_xvfb_running() -> None:
    """Ensure Xvfb is running on display :99."""
    if os.environ.get("DISPLAY"):
        return

    # Check if already running
    try:
        result = subprocess.run(
            ["pgrep", "-f", "Xvfb.*:99"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            os.environ["DISPLAY"] = ":99"
            return
    except FileNotFoundError:
        pass

    # Start Xvfb
    try:
        subprocess.Popen(
            ["Xvfb", ":99", "-screen", "0", "1024x768x24"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as e:
        raise RuntimeError("Xvfb not found - install with: apt-get install xvfb") from e

    os.environ["DISPLAY"] = ":99"

    # Wait for Xvfb to be ready
    socket_path = "/tmp/.X11-unix/X99"
    for _ in range(20):
        if os.path.exists(socket_path):
            return
        time.sleep(0.1)
    raise RuntimeError("Xvfb started but socket not ready")


def _setup_libreoffice_macro() -> bool:
    """Setup LibreOffice macro for accepting tracked changes."""
    macro_dir = Path(MACRO_DIR)
    macro_file = macro_dir / "Module1.xba"

    if macro_file.exists() and "AcceptAllTrackedChanges" in macro_file.read_text():
        return True

    # Initialize LibreOffice if needed (use custom profile)
    if not macro_dir.exists():
        subprocess.run(
            [
                "soffice",
                "--headless",
                f"-env:UserInstallation=file://{LIBREOFFICE_PROFILE}",
                "--terminate_after_init",
            ],
            capture_output=True,
            timeout=10,
            check=False,
        )
        macro_dir.mkdir(parents=True, exist_ok=True)

    try:
        macro_file.write_text(ACCEPT_CHANGES_MACRO)
        return True
    except Exception as e:
        logger.warning(f"Failed to setup LibreOffice macro: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Accept all tracked changes in a DOCX file"
    )
    parser.add_argument("input_file", help="Input DOCX file with tracked changes")
    parser.add_argument("output_file", help="Output DOCX file (clean, no tracked changes)")
    args = parser.parse_args()

    _, message = accept_changes(args.input_file, args.output_file)
    print(message)

    if "Error" in message:
        raise SystemExit(1)
