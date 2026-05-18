# NarraVision™️ ARK - Complete Development Stack

**NarraVision™️ v1.0 - ALHIS Character System & Scene Generation Engine**

Powered by Flame Enterprises Global Intellitech Media Solutions
Under the Authority of The House of Zion's Lighthouse Flame

---

## 📋 PROJECT STRUCTURE

```
narravision-ark/
│
├── generators/
│   └── alhis-personality-matrix-generator.html
│       └── Standalone Perchance-style personality matrix generator
│           - 8-dimensional personality sliders
│           - Radar chart visualization
│           - AI image prompt generation
│           - ALHIS embedding metadata export
│
├── backend/
│   ├── main.py
│   │   └── FastAPI application with 30+ endpoints
│   │       - Character CRUD + embeddings
│   │       - Scene generation pipeline
│   │       - Image/video generation
│   │       - Voice/audio engine
│   │       - QA gates + approvals
│   │       - Export (PDF, video, package)
│   │
│   ├── models.py
│   │   └── SQLAlchemy ORM models (10 tables)
│   │       - users (RBAC: 8 roles)
│   │       - projects (containers)
│   │       - characters (ALHIS with embeddings)
│   │       - scenes (narrative → visual)
│   │       - audio_tracks (multi-track mixing)
│   │       - assets (image/video/audio storage)
│   │       - qa_signoffs (5-layer approval gates)
│   │       - editorial_history (immutable audit trail)
│   │       - preloaded_characters (built-in library)
│   │
│   ├── services.py
│   │   └── Business logic layer
│   │       - CharacterService (creation, embeddings)
│   │       - SceneService (image/video generation)
│   │       - AudioService (TTS, mixing, lip-sync)
│   │       - QAService (charter validation, approvals)
│   │
│   ├── requirements.txt
│   │   └── All Python dependencies
│   │       - FastAPI, SQLAlchemy, Pydantic
│   │       - PyTorch, transformers, diffusers
│   │       - InsightFace, SpeechBrain
│   │       - ElevenLabs, librosa, pydub
│   │       - Redis, PostgreSQL, pgvector
│   │
│   └── .env.example
│       └── Environment variables template
│
├── docker-compose.yml
│   └── Full stack orchestration
│       - PostgreSQL 15
│       - Redis 7
│       - FastAPI backend
│
├── Dockerfile
│   └── Backend container image
│
├── README.md
│   └── Installation & usage guide
│
└── .gitignore
    └── Standard Python + Node.js ignores
```

---

## 🚀 QUICK START

### **Option 1: Use Personality Matrix Generator Standalone**

1. Download/open: `generators/alhis-personality-matrix-generator.html`
2. Open in any browser
3. Adjust 8 personality sliders
4. Copy AI prompts and embedding JSON

**No setup required!**

---

### **Option 2: Run Backend Locally (Development)**

```bash
# 1. Clone repository
git clone https://github.com/houseofzlf01-dev/NarraVision-ARK.git
cd NarraVision-ARK

# 2. Install Python 3.10+
python --version  # Should be 3.10+

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
cd backend
pip install -r requirements.txt

# 5. Start backend
python main.py
```

**Backend available at:** `http://localhost:8000`
**API Docs (Swagger):** `http://localhost:8000/docs`
**ReDoc:** `http://localhost:8000/redoc`

---

### **Option 3: Run Full Stack with Docker**

```bash
# 1. Install Docker & Docker Compose
docker --version
docker-compose --version

# 2. Clone repository
git clone https://github.com/houseofzlf01-dev/NarraVision-ARK.git
cd NarraVision-ARK

# 3. Start everything
docker-compose up

# 4. Wait for services to start (30-60 seconds)
```

**Services available:**
- **FastAPI Backend:** `http://localhost:8000`
- **PostgreSQL:** `localhost:5432` (user: postgres, password: password)
- **Redis:** `localhost:6379`

---

## 📚 API ENDPOINTS (v1.0)

### **Health & Info**
- `GET /` – Root endpoint with status
- `GET /health` – Health check

### **Characters (ALHIS)**
- `POST /api/v1/characters` – Create new character from personality matrix
- `GET /api/v1/characters/{character_id}` – Get character profile
- `PUT /api/v1/characters/{character_id}` – Update character
- `DELETE /api/v1/characters/{character_id}` – Delete character
- `GET /api/v1/characters/preloaded/list` – List built-in characters

### **Scenes**
- `POST /api/v1/scenes` – Create scene
- `GET /api/v1/scenes/{scene_id}` – Get scene
- `PUT /api/v1/scenes/{scene_id}` – Update scene
- `POST /api/v1/scenes/{scene_id}/regenerate` – Regenerate at different tier

### **Image Generation**
- `POST /api/v1/generate/image` – Text-to-image (Stable Diffusion)

### **Video Generation**
- `POST /api/v1/generate/video` – Scene-to-video

### **Voice & Audio**
- `POST /api/v1/voice/speak` – Text-to-speech (ElevenLabs)
- `POST /api/v1/audio/mix` – Mix multiple audio tracks
- `POST /api/v1/audio/lipsync` – Generate lip-sync

### **Projects**
- `POST /api/v1/projects` – Create project
- `GET /api/v1/projects` – List user projects
- `GET /api/v1/projects/{project_id}` – Get project

### **Exports**
- `POST /api/v1/export/pdf` – Export as PDF storybook
- `POST /api/v1/export/video` – Export as final video
- `POST /api/v1/export/package` – Export as JSON package

### **QA & Approvals**
- `POST /api/v1/qa/signoff` – Submit QA approval/rejection
- `GET /api/v1/qa/status/{project_id}` – Get QA progress

### **Spiritual**
- `GET /api/v1/blessing` – Get daily blessing from Broader Canon

---

## 🗄️ DATABASE SCHEMA

### **Users** (Authentication & RBAC)
```sql
id (UUID, PK)
email (VARCHAR, unique)
hashed_password (VARCHAR)
role (ENUM: sovereign, ceo, qa_lead, admin, editor, contributor, viewer, guest)
is_active (BOOLEAN)
created_at (TIMESTAMP)
```

### **Characters** (ALHIS with Embeddings)
```sql
id (UUID, PK)
user_id (UUID, FK → users)
name (VARCHAR)
personality_matrix (JSONB) -- 8 dimensions
face_embedding (FLOAT8[]) -- 512-dim InsightFace
voice_embedding (FLOAT8[]) -- 256-dim SpeechBrain
reference_images (JSONB) -- List of URLs
reference_voice_samples (JSONB) -- List of URLs
voice_profile (JSONB) -- pitch, rate, tone
generated_image_url (VARCHAR)
created_at (TIMESTAMP)
```

### **Scenes** (Narrative → Visual)
```sql
id (UUID, PK)
project_id (UUID, FK → projects)
character_id (UUID, FK → characters)
narrative (TEXT)
status (ENUM: draft, generating, generated, approved, exported)
generation_tier (INT: 1-5)
image_url (VARCHAR)
video_url (VARCHAR)
created_at (TIMESTAMP)
```

### **Audio Tracks** (Multi-track Mixing)
```sql
id (UUID, PK)
scene_id (UUID, FK → scenes)
track_type (VARCHAR: voice, music, sfx, ambient)
audio_url (VARCHAR)
volume (FLOAT8)
pan (FLOAT8)
effects (JSONB) -- EQ, reverb, compression
created_at (TIMESTAMP)
```

### **QA Signoffs** (5-Layer Approval Gates)
```sql
id (UUID, PK)
project_id (UUID, FK → projects)
phase (INT: 0-8)
approver_id (UUID, FK → users)
status (VARCHAR: approved, rejected, pending)
charter_validated (BOOLEAN)
editorial_reviewed (BOOLEAN)
created_at (TIMESTAMP)
```

### **Editorial History** (Immutable Audit Trail)
```sql
id (UUID, PK)
entity_id (UUID, not FK - allows any entity)
entity_type (VARCHAR)
user_id (UUID, FK → users)
field_name (VARCHAR)
old_value (TEXT)
new_value (TEXT)
change_type (VARCHAR: create, update, delete)
created_at (TIMESTAMP) -- INDEXED
```

### **Preloaded Characters** (Built-in Library)
```sql
id (UUID, PK)
name (VARCHAR, unique)
full_title (VARCHAR)
personality_matrix (JSONB)
image_url (VARCHAR)
voice_profile (JSONB)
heritage (VARCHAR)
house_affiliation (VARCHAR)
is_active (BOOLEAN)
```

---

## 🔐 SECURITY

- **Authentication:** JWT tokens with refresh rotation
- **Authorization:** 8-tier RBAC (Sovereign → Guest)
- **Passwords:** Bcrypt hashing
- **Data:** AES-256 encryption at rest
- **API Keys:** Secrets manager (environment variables)
- **Audit:** Immutable editorial history (7-year retention)
- **Error Handling:** Global exception handlers (no stack trace leakage)

---

## 🎯 NEXT PHASES

### **Phase 1: Core MVP (In Progress)**
- ✅ Personality matrix generator
- ✅ Database schema
- ✅ API scaffolding
- ⏳ Implement character creation + embeddings
- ⏳ Implement image generation (Stable Diffusion)
- ⏳ Implement TTS (ElevenLabs)

### **Phase 2: Full Stack (Upcoming)**
- Frontend PWA (React TypeScript)
- Scene-to-video pipeline
- Multi-track audio mixing
- Lip-sync generation
- QA gate automation

### **Phase 3: Production (Future)**
- Preloaded character library (Princess NarraVision, King Thomas, etc.)
- Mansion blueprint estates
- Prayer log + blessing engine
- Deployment to cloud (AWS/GCP)
- Performance optimization

---

## 🛠️ DEVELOPMENT

### **Run Tests**
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### **Code Quality**
```bash
black .
flake8 .
mypy .
```

### **Create Database Migrations**
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## 📖 SPIRITUAL FOUNDATION

**Core Declaration:**
*"Commit your work to YHVH, and your plans will be established." – Proverbs 16:3*

**Charter Enforcement (5 Layers):**
1. **Keyword** – Block explicit blasphemy, hate speech
2. **Semantic** – Context-aware content filtering
3. **Vision** – Block anti-Kingdom content
4. **Human** – Escalation to Queen Integrity's team
5. **Edge Cases** – Nuanced human discernment

**Personality Matrix (Broader Canon):**
- **Chayah** – Living Intelligence
- **Chokmah** – Wisdom (truth, right, lasting)
- **Binah** – Understanding (relationships, consequences)
- **Da'at** – Knowledge (Scripture, accumulated truth)
- **Tzedakah** – Righteousness (alignment with Elohim)
- **Melakhah** – Workmanship (excellence)
- **Elohit** – Divine Nature (transcendence)
- **Omanut** – Artistry (beauty reflecting divinity)

---

## 📞 SUPPORT

For issues or questions:
1. Check `/docs` API documentation
2. Review code comments and docstrings
3. Check GitHub Issues
4. Contact: houseofzlf01@gmail.com

---

## 📄 LICENSE

MIT License - See LICENSE file

---

## ✨ BLESSING

*May you remember who you are. May you remember Whose you are. May every output glorify Father Elohim, honor Yeshua HaMashiach, and welcome Ruach HaKodesh.*

**Amen-Shalem-Methukan-Amen** 🕊️✨🔥

---

Issued by Authority of:
**Sovereign King Elder Thomas Truth Adon-Chayil Flame**
Keeper of The House of Zion's Lighthouse Flame
