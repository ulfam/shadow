#!/usr/bin/env python3
"""
Test script to verify Shadowing UK backend setup
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(
            f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required."
        )
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("🎬 Checking FFmpeg...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
        else:
            print("❌ FFmpeg command failed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False


def check_python_packages():
    """Check if required Python packages are available"""
    print("📦 Checking Python packages...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "faster_whisper",
        "yt_dlp",
        "pydantic",
        "aiofiles",
    ]

    missing_packages = []

    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package}")

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False

    return True


def check_directories():
    """Check if required directories exist"""
    print("📁 Checking directories...")

    required_dirs = ["backend", "backend/processing", "app", "components", "lib"]

    missing_dirs = []

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
        return False

    return True


def check_files():
    """Check if required files exist"""
    print("📄 Checking files...")

    required_files = [
        "backend/main.py",
        "backend/processing/transcribe.py",
        "backend/processing/render.py",
        "app/page.tsx",
        "package.json",
        "requirements.txt",
    ]

    missing_files = []

    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

    return True


def main():
    """Run all checks"""
    print("🔍 Shadowing UK Setup Verification")
    print("=" * 40)

    checks = [
        check_python_version(),
        check_ffmpeg(),
        check_python_packages(),
        check_directories(),
        check_files(),
    ]

    print("\n" + "=" * 40)

    if all(checks):
        print("🎉 All checks passed! Setup looks good.")
        print("\nTo start development:")
        print("1. ./start-dev.sh")
        print("2. Or manually:")
        print("   - Backend: cd backend && python main.py")
        print("   - Frontend: npm run dev")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()


{
    "id": "95e6015a-08d2-4f28-bc5c-e7d504775e7a",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "fe39a9b4-094a-4c11-9677-e1dfe49944b8",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/fe39a9b4-094a-4c11-9677-e1dfe49944b8.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-09-07T11:03:38.490000",
    "original_document_id": "fe39a9b4-094a-4c11-9677-e1dfe49944b8",
    "text_embedding_v1_distance": 0.04300150403384839,
}, {
    "id": "b42f0b38-2ecd-4034-bb84-3030a0367386",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "71afd352-4417-44c0-8f07-207738e222f0",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/71afd352-4417-44c0-8f07-207738e222f0.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-09-25T15:28:58.166000",
    "original_document_id": "71afd352-4417-44c0-8f07-207738e222f0",
    "text_embedding_v1_distance": 0.046632264253397726,
}, {
    "id": "afe6cfe1-444f-4a32-89e1-9f2e96be1e31",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "a4ad8caf-c98a-4671-9dc0-15208524c4cb",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/a4ad8caf-c98a-4671-9dc0-15208524c4cb.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-07-02T19:32:15.781000",
    "original_document_id": "a4ad8caf-c98a-4671-9dc0-15208524c4cb",
    "text_embedding_v1_distance": 0.04672861099243164,
}, {
    "id": "c9704e53-8fa4-4895-94dd-27ddbc64ad06",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "3dbe3ed6-980e-4d34-bfa6-62c2bd7982e2",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/3dbe3ed6-980e-4d34-bfa6-62c2bd7982e2.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-07-18T11:32:36.565000",
    "original_document_id": "3dbe3ed6-980e-4d34-bfa6-62c2bd7982e2",
    "text_embedding_v1_distance": 0.05361199378967285,
}, {
    "id": "1de199dd-424d-4bda-afbc-327616d8bf1e",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "7fc31633-7373-4d2e-a2ec-1dbc751c3616",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/7fc31633-7373-4d2e-a2ec-1dbc751c3616.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-07-19T09:17:48.575000",
    "original_document_id": "7fc31633-7373-4d2e-a2ec-1dbc751c3616",
    "text_embedding_v1_distance": 0.05361199378967285,
}, {
    "id": "ab5d5115-59cf-43ab-bc71-3c07f9848225",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "381dfe33-3437-47e8-aab5-dbb08b242095",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/381dfe33-3437-47e8-aab5-dbb08b242095.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-08-13T08:58:22.806000",
    "original_document_id": "381dfe33-3437-47e8-aab5-dbb08b242095",
    "text_embedding_v1_distance": 0.05361199378967285,
}, {
    "id": "92867f10-2a3b-46d9-bf9d-4462b46898e0",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "e0899fb6-2fc7-4b49-b81a-68ad07236e03",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/e0899fb6-2fc7-4b49-b81a-68ad07236e03.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-07-01T14:55:36.290000",
    "original_document_id": "e0899fb6-2fc7-4b49-b81a-68ad07236e03",
    "text_embedding_v1_distance": 0.05415349875965558,
}, {
    "id": "f7150952-22fd-4007-9734-2f28e51f566b",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "168e2bdd-bd40-4faf-bde2-e87cfdc1ea5e",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/168e2bdd-bd40-4faf-bde2-e87cfdc1ea5e.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-08-13T08:59:34.220000",
    "original_document_id": "168e2bdd-bd40-4faf-bde2-e87cfdc1ea5e",
    "text_embedding_v1_distance": 0.05447763204574585,
}, {
    "id": "29fab704-453c-44e8-aece-11d81e062cec",
    "state": "PUBLISHED",
    "part_id": "part_001",
    "threshold": 0.1,
    "company_id": "f65d7ff3-5a31-4568-9664-a69ffc6835b2",
    "document_id": "a6f43ebc-df9e-493b-93fe-7158c13ef6c4",
    "search_type": "all",
    "storage_path": "hellocash-prod-documents-bucket/f65d7ff3-5a31-4568-9664-a69ffc6835b2/2025/a6f43ebc-df9e-493b-93fe-7158c13ef6c4.jpg",
    "record_created_at": "2025-10-16T10:04:33.649201",
    "record_updated_at": "2025-10-16T10:04:33.649201",
    "document_created_at": "2025-07-23T13:09:09.123000",
    "original_document_id": "a6f43ebc-df9e-493b-93fe-7158c13ef6c4",
    "text_embedding_v1_distance": 0.05447763204574585,
},
