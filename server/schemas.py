from pydantic import BaseModel, Field, field_validator

from server.config import MAX_TEXT_LENGTH
from server.prosody import field_description, validate


class TTSRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TEXT_LENGTH,
        description="要合成的文本",
    )
    voice: str = Field(
        default="zh-CN-XiaoxiaoNeural",
        description="音色 ID（ShortName），见 GET /voices",
    )
    rate: str = Field(default="+0%", description=field_description("rate"))
    volume: str = Field(default="+0%", description=field_description("volume"))
    pitch: str = Field(default="+0Hz", description=field_description("pitch"))

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, value: str) -> str:
        return validate("rate", value)

    @field_validator("volume")
    @classmethod
    def validate_volume(cls, value: str) -> str:
        return validate("volume", value)

    @field_validator("pitch")
    @classmethod
    def validate_pitch(cls, value: str) -> str:
        return validate("pitch", value)
