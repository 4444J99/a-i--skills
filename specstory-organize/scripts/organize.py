#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Organize SpecStory history files into YYYY/MM subdirectories.

Moves .md files from .specstory/history/ into .specstory/history/YYYY/MM/
based on the timestamp in the filename (not the file's modification time).

Compatible with Python 2.7+ and Python 3.x
"""

from __future__ import print_function

import os
import re
import shutil
import sys

# Pattern to extract YYYY-MM-DD from filenames like:
#   2025-09-17_13-45-37Z-description.md
#   2025-10-09_13-19Z-description.md
#   2025-10-15_02-58-52Z.md
DATE_PATTERN = re.compile(r'^(\d{4})-(\d{2})-\d{2}_')


def find_specstory_history():
    """
    Find the .specstory/history directory relative to current working directory.
    Returns the path if found, None otherwise.
    """
    history_dir = os.path.join(os.getcwd(), '.specstory', 'history')
    if os.path.isdir(history_dir):
        return history_dir
    return None


def extract_year_month(filename):
    """
    Extract year and month from a filename.
    Returns (year, month) tuple if found, None otherwise.
    """
    match = DATE_PATTERN.match(filename)
    if match:
        return (match.group(1), match.group(2))
    return None


def organize_history(history_dir, dry_run=False):
    """
    Organize .md files in history_dir into YYYY/MM subdirectories.

    Args:
        history_dir: Path to the .specstory/history directory
        dry_run: If True, only print what would be done without moving files

    Returns:
        Tuple of (moved_count, skipped_count, error_count)
    """
    moved = 0
    skipped = 0
    errors = 0

    # Get list of files in history directory (not subdirectories)
    try:
        entries = os.listdir(history_dir)
    except OSError as e:
        print("Error listing directory: %s" % e)
        return (0, 0, 1)

    for entry in entries:
        entry_path = os.path.join(history_dir, entry)

        # Skip directories
        if os.path.isdir(entry_path):
            continue

        # Skip non-.md files
        if not entry.endswith('.md'):
            print("Skipping non-.md file: %s" % entry)
            skipped += 1
            continue

        # Extract year and month from filename
        date_parts = extract_year_month(entry)
        if date_parts is None:
            print("Skipping file without valid timestamp: %s" % entry)
            skipped += 1
            continue

        year, month = date_parts

        # Build destination directory path
        dest_dir = os.path.join(history_dir, year, month)
        dest_path = os.path.join(dest_dir, entry)

        if dry_run:
            print("Would move: %s -> %s/%s/" % (entry, year, month))
            moved += 1
            continue

        try:
            # Create year directory if needed
            year_dir = os.path.join(history_dir, year)
            if not os.path.exists(year_dir):
                os.mkdir(year_dir)

            # Create month directory if needed
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)

            # Remove destination file if it exists (to allow overwrite)
            if os.path.exists(dest_path):
                os.remove(dest_path)

            # Move the file
            shutil.move(entry_path, dest_path)
            print("Moved: %s -> %s/%s/" % (entry, year, month))
            moved += 1

        except OSError as e:
            print("Error moving %s: %s" % (entry, e))
            errors += 1
        except Exception as e:
            print("Unexpected error moving %s: %s" % (entry, e))
            errors += 1

    return (moved, skipped, errors)


def main():
    """Main entry point."""
    # Check for --dry-run flag
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    # Find the history directory
    history_dir = find_specstory_history()

    if history_dir is None:
        print("Error: Could not find .specstory/history directory")
        print("Make sure you are running this script from a project root")
        print("that contains a .specstory/history directory.")
        sys.exit(1)

    print("Organizing: %s" % history_dir)
    if dry_run:
        print("(Dry run - no files will be moved)")
    print("")

    moved, skipped, errors = organize_history(history_dir, dry_run=dry_run)

    print("")
    print("Complete: %d moved, %d skipped, %d errors" % (moved, skipped, errors))

    if errors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
