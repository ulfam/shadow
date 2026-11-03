#!/usr/bin/env python3
"""
Test script to verify directory structure creation
"""

import uuid
from pathlib import Path

# Test the same directory structure logic as main.py
DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "input"
WORK_DIR = DATA_DIR / "work"
OUTPUT_DIR = DATA_DIR / "output"


def get_job_dirs(job_id: str):
    """Get job-specific directories"""
    return {
        "input": INPUT_DIR / job_id,
        "work": WORK_DIR / job_id,
        "output": OUTPUT_DIR / job_id,
    }


def test_directory_creation():
    """Test directory creation"""
    job_id = str(uuid.uuid4())
    job_dirs = get_job_dirs(job_id)

    print(f"Testing directory creation for job: {job_id}")
    print(f"Base directories:")
    print(f"  INPUT_DIR: {INPUT_DIR}")
    print(f"  WORK_DIR: {WORK_DIR}")
    print(f"  OUTPUT_DIR: {OUTPUT_DIR}")
    print()

    print("Job-specific directories:")
    for dir_path in job_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")

    print()
    print("Verifying structure:")
    for name, dir_path in job_dirs.items():
        if dir_path.exists():
            print(f"  ✅ {name}: {dir_path}")
        else:
            print(f"  ❌ {name}: {dir_path} (not found)")

    # Clean up
    import shutil

    shutil.rmtree(DATA_DIR)
    print(f"\nCleaned up: {DATA_DIR}")


if __name__ == "__main__":
    test_directory_creation()
