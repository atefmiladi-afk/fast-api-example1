from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    email_tokens = relationship("EmailToken", back_populates="user", cascade="all, delete-orphan")


class EmailToken(Base):
    __tablename__ = "email_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String(64), unique=True, nullable=False, index=True)
    purpose = Column(String(32), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="email_tokens")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, nullable=False, index=True)
    name_de = Column(String(120), nullable=False)
    name_en = Column(String(120), nullable=False)
    description = Column(Text, default="")
    emoji = Column(String(16), default="")
    color = Column(String(32), default="#2563eb")
    image_url = Column(String(500), default="")

    words = relationship("Word", back_populates="category", cascade="all, delete-orphan")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    german = Column(String(120), nullable=False)
    article = Column(String(16), default="")
    english = Column(String(120), nullable=False)
    example_de = Column(String(255), default="")
    example_en = Column(String(255), default="")
    image_url = Column(String(500), default="")
    audio_hint = Column(String(120), default="")

    category = relationship("Category", back_populates="words")
    progress = relationship("UserProgress", back_populates="word", cascade="all, delete-orphan")


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "word_id", name="uq_user_word"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False, index=True)
    learned = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="progress")
    word = relationship("Word", back_populates="progress")
