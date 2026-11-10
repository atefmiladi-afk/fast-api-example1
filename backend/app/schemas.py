from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    message: str
    email: str | None = None


class ForgotPasswordIn(BaseModel):
    email: str = Field(min_length=5, max_length=255)


class ResetPasswordIn(BaseModel):
    token: str
    password: str = Field(min_length=6, max_length=128)


class VerifyEmailIn(BaseModel):
    token: str


class ResendVerificationIn(BaseModel):
    email: str = Field(min_length=5, max_length=255)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class WordOut(BaseModel):
    id: int
    german: str
    article: str
    english: str
    example_de: str
    example_en: str
    image_url: str
    audio_hint: str
    learned: bool = False

    model_config = {"from_attributes": True}


class CategoryOut(BaseModel):
    id: int
    slug: str
    name_de: str
    name_en: str
    description: str
    emoji: str
    color: str
    image_url: str
    word_count: int = 0
    learned_count: int = 0

    model_config = {"from_attributes": True}


class CategoryDetail(CategoryOut):
    words: list[WordOut] = []


class ProgressUpdate(BaseModel):
    learned: bool


class ProgressOut(BaseModel):
    word_id: int
    learned: bool
