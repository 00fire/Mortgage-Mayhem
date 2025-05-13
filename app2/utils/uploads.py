import uuid, unicodedata, re
from pathlib import Path

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "file"

def upload_to_profile(instance, filename):
    name, ext = Path(filename).stem, Path(filename).suffix
    slug = slugify(name)
    unique = uuid.uuid4().hex[:8]
    return f"profile_pics/{slug}-{unique}{ext}"

def upload_to_property(instance, filename):
    name, ext = Path(filename).stem, Path(filename).suffix
    slug = slugify(name)
    unique = uuid.uuid4().hex[:8]
    return f"property_images/{slug}-{unique}{ext}"
