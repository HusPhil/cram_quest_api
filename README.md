# CramQuest API

CramQuest is a FastAPI-based application for managing study sessions and quests. This document provides a comprehensive overview of the codebase structure and relationships.

## Project Structure

```
cram_quest_v1/
├── app/
│   ├── api/            # API routes and endpoints
│   ├── core/           # Core functionality (database, auth)
│   ├── crud/           # CRUD operations
│   ├── models/         # SQLAlchemy/SQLModel models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic services
│   └── main.py        # Application entry point
├── migrations/         # Alembic database migrations
├── tests/             # Test files
├── alembic.ini        # Alembic configuration
└── requirements.txt    # Project dependencies
```

## Core Components

### Models

The application uses SQLModel (SQLAlchemy + Pydantic) for database models. Key models include:

1. **User Model**
   - Properties: id, username, email, hashed_password
   - Base user authentication model

2. **Player Model**
   - Properties: id, user_id, level, xp, title
   - Represents the gamification aspect of a user
   - Relationships: One-to-One with User and Profile

3. **Profile Model**
   - Properties: id, player_id, avatar_url, bio, mood
   - Mood options: HAPPY, MOTIVATED, NEUTRAL, STRESSED, EXHAUSTED
   - Relationships: One-to-One with Player

4. **Subject Model**
   - Properties: id, player_id, code_name, description, difficulty
   - Relationships: Belongs to Player, has many Quests and StudySessions

5. **Quest Model**
   - Properties: id, subject_id, description, difficulty, status, created_at
   - Relationships: Belongs to a Subject
   - Status options: IN_PROGRESS, COMPLETED

6. **Study Session Model**
   - Properties: id, player_id, subject_id, start_time, end_time, xp_earned, status
   - Tracks individual study sessions
   - Relationships: Belongs to Player and Subject

### Schemas

Pydantic schemas for data validation and serialization:

1. **User Schemas**
   - `UserBase`: Base schema with username and email
   - `UserCreate`: For user registration with password
   - `UserUpdate`: For updating user details
   - `UserRead`: For reading user data

2. **Player Schemas**
   - `PlayerBase`: Base player information
   - `PlayerCreate`: For creating new player profiles
   - `PlayerRead`: For reading player data with stats

3. **Profile Schemas**
   - `ProfileBase`: Base profile information
   - `ProfileUpdate`: For updating profile details
   - `ProfileRead`: For reading profile data

4. **Subject Schemas**
   - `SubjectBase`: Base subject information
   - `SubjectCreate`: For creating new subjects
   - `SubjectRead`: For reading subject data

5. **Quest Schemas**
   - `QuestBase`: Base schema with common fields
   - `QuestCreate`: For creating new quests
   - `QuestUpdate`: For updating existing quests
   - `QuestRead`: For reading quest data

6. **Study Session Schemas**
   - `StudySessionCreate`: For creating new sessions
   - `StudySessionRead`: For reading session data
   - `StudySessionEnd`: For ending study sessions with quest completion

### API Routes

The API is versioned (v1) and includes the following endpoints:

1. **User Routes** (`/api/v1/users/`)
   - Authentication endpoints
   - User CRUD operations

2. **Player Routes** (`/api/v1/players/`)
   - Player profile management
   - XP and level tracking

3. **Profile Routes** (`/api/v1/profiles/`)
   - Profile customization
   - Mood management

4. **Subject Routes** (`/api/v1/subjects/`)
   - Subject CRUD operations
   - Subject statistics

5. **Quest Routes** (`/api/v1/quests/`)
   - GET `/`: List all quests
   - GET `/{quest_id}`: Get specific quest
   - POST `/`: Create new quest
   - PATCH `/{quest_id}`: Update quest
   - DELETE `/{quest_id}`: Delete quest

6. **Study Session Routes** (`/api/v1/study-sessions/`)
   - GET `/`: List all study sessions
   - GET `/{study_session_id}`: Get specific session
   - POST `/`: Create new study session
   - PATCH `/{study_session_id}/end`: End study session

### CRUD Operations

Each model has corresponding CRUD operations in the `crud/` directory:

1. **User CRUD**
   - User registration and authentication
   - Password hashing and verification
   - User profile management

2. **Player CRUD**
   - Player creation and management
   - XP and level calculations
   - Title management

3. **Profile CRUD**
   - Profile customization
   - Mood tracking
   - Avatar management

4. **Subject CRUD**
   - Subject management
   - Progress tracking
   - Difficulty management

5. **Quest CRUD**
   - Create new quests
   - Read quest details
   - Update quest information
   - Delete quests
   - List all quests

6. **Study Session CRUD**
   - Create study sessions
   - Read session details
   - End study sessions
   - List all sessions
   - Calculate XP earned

### Authentication

The application implements authentication using:
- JWT token-based authentication
- User session management
- Protected routes using FastAPI dependencies
- Password hashing with bcrypt

### Database

- Uses SQLite database (cram_quest.db)
- Alembic for database migrations
- Async database operations using SQLAlchemy
- Relationship management with SQLModel

## API Security

- Protected routes require authentication
- JWT token validation
- Database session management
- Input validation using Pydantic schemas
- Password hashing and secure storage

## Dependencies

Key dependencies include:
- FastAPI
- SQLModel
- Alembic
- SQLAlchemy
- Pydantic
- Python-Jose (for JWT)
- Passlib (for password hashing)
- Python-multipart (for form data)
- Email-validator

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
API documentation is available at `http://localhost:8000/docs`