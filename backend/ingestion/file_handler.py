import os
from pathlib import Path
from backend.utils.validation import FileMeta
from pydantic import ValidationError

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(uploaded_file):
    try:
        file_meta = FileMeta(
            filename=uploaded_file.name,
            content_type=uploaded_file.type,
            size=uploaded_file.size
        )

        save_path = UPLOAD_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return True, f" File '{uploaded_file.name}' uploaded successfully."

    except ValidationError as e:
        return False, f" Validation failed: {e.errors()[0]['msg']}"
