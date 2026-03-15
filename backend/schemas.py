from pydantic import BaseModel, field_validator

# 画像制限
MAX_IMAGE_BASE64_SIZE = 10 * 1024 * 1024  # 10MB (base64文字列の長さ)
MAX_IMAGES_PER_REQUEST = 5
ALLOWED_MEDIA_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


class ImageAttachment(BaseModel):
    media_type: str
    data: str  # base64-encoded

    @field_validator("media_type")
    @classmethod
    def validate_media_type(cls, v: str) -> str:
        if v not in ALLOWED_MEDIA_TYPES:
            raise ValueError(f"許可されていない画像形式です。対応形式: {', '.join(sorted(ALLOWED_MEDIA_TYPES))}")
        return v

    @field_validator("data")
    @classmethod
    def validate_data_size(cls, v: str) -> str:
        if len(v) > MAX_IMAGE_BASE64_SIZE:
            size_mb = len(v) / (1024 * 1024)
            raise ValueError(f"画像サイズが大きすぎます（{size_mb:.1f}MB）。10MB以下にしてください。")
        return v


def validate_image_count(images: list[ImageAttachment]) -> list[ImageAttachment]:
    """リクエストレベルの画像枚数バリデーション"""
    if len(images) > MAX_IMAGES_PER_REQUEST:
        raise ValueError(f"画像は最大{MAX_IMAGES_PER_REQUEST}枚までです。")
    return images
