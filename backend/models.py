"""
Database Models for NarraVision™️ ARK
SQLAlchemy ORM Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, LargeBinary, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB, FLOAT8
from datetime import datetime
import uuid
import enum

Base = declarative_base()

# ========================================
# ENUMS
# ========================================
class UserRole(str, enum.Enum):
    SOVEREIGN = "sovereign"
    CEO = "ceo"
    QA_LEAD = "qa_lead"
    ADMIN = "admin"
    EDITOR = "editor"
    CONTRIBUTOR = "contributor"
    VIEWER = "viewer"
    GUEST = "guest"

class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    APPROVED = "approved"
    EXPORTED = "exported"
    ARCHIVED = "archived"

class SceneStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    GENERATED = "generated"
    EDITED = "edited"
    APPROVED = "approved"
    EXPORTED = "exported"

class GenerationTier(int, enum.Enum):
    TIER_1 = 1  # <5s, Good
    TIER_2 = 2  # <15s, Better
    TIER_3 = 3  # <45s, High
    TIER_4 = 4  # <120s, Ultra-photorealistic
    TIER_5 = 5  # <300s, Hero shot (4K, 60fps)

# ========================================
# USER MODEL
# ========================================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.CONTRIBUTOR, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    def __repr__(self):
        return f"<User {self.email}>"

# ========================================
# PROJECT MODEL
# ========================================
class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False)
    cover_image_url = Column(String(2048))
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)

    def __repr__(self):
        return f"<Project {self.title}>"

# ========================================
# CHARACTER MODEL (ALHIS)
# ========================================
class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    age = Column(String(100))
    heritage = Column(String(255))
    role = Column(String(255))
    
    # Personality Matrix (Broader Canon)
    personality_matrix = Column(JSONB, nullable=False, default={
        "chayah": 0,
        "chokmah": 0,
        "binah": 0,
        "daatKnowledge": 0,
        "tzedakah": 0,
        "melakhah": 0,
        "elohit": 0,
        "omanut": 0
    })
    
    # Embeddings
    face_embedding = Column(FLOAT8)  # 512-dim InsightFace
    face_embedding_model = Column(String(100), default="buffalo_l")
    face_embedding_threshold = Column(FLOAT8, default=0.94)
    
    voice_embedding = Column(FLOAT8)  # 256-dim SpeechBrain
    voice_embedding_model = Column(String(100), default="spkrec_xvect_voxceleb")
    voice_embedding_threshold = Column(FLOAT8, default=0.85)
    
    # Reference Materials
    reference_images = Column(JSONB, default=[])  # List of image URLs
    reference_voice_samples = Column(JSONB, default=[])  # List of audio URLs
    reference_video = Column(String(2048))
    
    # Voice Profile
    voice_profile = Column(JSONB, default={
        "pitch": 1.0,
        "rate": 1.0,
        "volume": 1.0,
        "tone": "neutral"
    })
    
    # Generated Assets
    generated_image_url = Column(String(2048))
    generated_image_seed = Column(Integer)
    lora_training_preset = Column(String(50), default="standard")  # light, standard, high-fidelity
    
    # Metadata
    metadata = Column(JSONB, default={})
    version = Column(Integer, default=1)
    is_preloaded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Character {self.name}>"

# ========================================
# SCENE MODEL
# ========================================
class Scene(Base):
    __tablename__ = "scenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), index=True)
    
    title = Column(String(255), nullable=False)
    narrative = Column(Text, nullable=False)
    status = Column(Enum(SceneStatus), default=SceneStatus.DRAFT, nullable=False)
    
    # Generation Settings
    generation_tier = Column(Enum(GenerationTier), default=GenerationTier.TIER_2)
    seed = Column(Integer)
    generation_time_ms = Column(Integer)
    
    # Generated Assets
    image_url = Column(String(2048))
    video_url = Column(String(2048))
    background_url = Column(String(2048))
    
    # AI Generation Parameters
    ai_parameters = Column(JSONB, default={})
    
    # Versioning
    version = Column(Integer, default=1)
    previous_versions = Column(JSONB, default=[])
    
    # Metadata
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Scene {self.title}>"

# ========================================
# AUDIO TRACK MODEL
# ========================================
class AudioTrack(Base):
    __tablename__ = "audio_tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"), nullable=False, index=True)
    
    track_type = Column(String(50), nullable=False)  # voice, music, sfx, ambient
    audio_url = Column(String(2048), nullable=False)
    
    # Mixing Settings
    volume = Column(FLOAT8, default=1.0)
    pan = Column(FLOAT8, default=0.0)  # -1.0 (left) to 1.0 (right)
    muted = Column(Boolean, default=False)
    
    # Effects
    effects = Column(JSONB, default={
        "eq": None,
        "reverb": None,
        "compression": None
    })
    
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AudioTrack {self.track_type}>"

# ========================================
# ASSET MODEL
# ========================================
class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    
    asset_type = Column(String(50), nullable=False)  # image, video, audio, etc.
    filename = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    
    file_size = Column(Integer)
    mime_type = Column(String(100))
    
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Asset {self.filename}>"

# ========================================
# QA SIGNOFF MODEL
# ========================================
class QASignoff(Base):
    __tablename__ = "qa_signoffs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    
    phase = Column(Integer, nullable=False)  # 0-8 QA phases
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    status = Column(String(50), nullable=False)  # approved, rejected, pending
    comments = Column(Text)
    
    charter_validated = Column(Boolean, default=False)
    editorial_reviewed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<QASignoff Phase {self.phase}>"

# ========================================
# EDITORIAL HISTORY MODEL
# ========================================
class EditorialHistory(Base):
    __tablename__ = "editorial_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False)  # character, scene, project, etc.
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    field_name = Column(String(255), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    
    change_type = Column(String(50), nullable=False)  # create, update, delete
    reason = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<EditorialHistory {self.entity_type}#{self.entity_id}>"

# ========================================
# PRELOADED CHARACTER PROFILES
# ========================================
class PreloadedCharacter(Base):
    __tablename__ = "preloaded_characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(255), nullable=False, unique=True)
    full_title = Column(String(255))
    description = Column(Text)
    role = Column(String(255))
    
    # Personality Matrix
    personality_matrix = Column(JSONB, nullable=False)
    
    # Image & Voice
    image_url = Column(String(2048))
    introduction_text = Column(Text)
    royal_declaration = Column(Text)
    
    # Voice Profile
    voice_profile = Column(JSONB, default={
        "pitch": 1.0,
        "rate": 1.0,
        "volume": 1.0,
        "tone": "neutral"
    })
    
    # Heritage
    heritage = Column(String(255))
    house_affiliation = Column(String(255), default="The House of Zion's Lighthouse Flame")
    
    # Embeddings (placeholder URLs)
    face_embedding_url = Column(String(2048))
    voice_embedding_url = Column(String(2048))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PreloadedCharacter {self.name}>"
