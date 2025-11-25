"""Storage service for handling file uploads."""
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from fastapi import UploadFile

from plantos_backend.settings import get_settings


class StorageService(Protocol):
    def upload_image(self, file: UploadFile) -> str:
        ...


class LocalStorageService:
    """Stores files in a local directory."""

    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        # Ensure this directory is served statically if we want to view images,
        # but for now we just return the path.

    def upload_image(self, file: UploadFile) -> str:
        file_ext = Path(file.filename).suffix if file.filename else ".jpg"
        filename = f"{uuid4()}{file_ext}"
        file_path = self.upload_dir / filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return absolute path for now, or a relative URL if we had a static mount.
        # For the AI processing, absolute path is fine if running locally.
        return str(file_path.absolute())


class GCSStorageService:
    """Stores files in Google Cloud Storage."""
    
    def __init__(self, bucket_name: str):
        from google.cloud import storage
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_image(self, file: UploadFile) -> str:
        file_ext = Path(file.filename).suffix if file.filename else ".jpg"
        blob_name = f"uploads/{uuid4()}{file_ext}"
        blob = self.bucket.blob(blob_name)
        
        blob.upload_from_file(file.file)
        return blob.public_url


def get_storage_service() -> StorageService:
    settings = get_settings()
    if settings.environment == "production":
        # Assume bucket name is in settings or env
        bucket_name = os.getenv("PLANTOS_STORAGE_BUCKET", "plantos-uploads")
        return GCSStorageService(bucket_name)
    else:
        return LocalStorageService()
