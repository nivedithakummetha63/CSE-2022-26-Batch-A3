# RoomieRadar UML Diagrams Documentation

This document contains comprehensive UML diagrams for the RoomieRadar application, essential for technical documentation and system understanding.

## Table of Contents
1. [Class Diagram](#class-diagram)
2. [Entity Relationship Diagram (ERD)](#entity-relationship-diagram)
3. [Use Case Diagram](#use-case-diagram)
4. [Sequence Diagrams](#sequence-diagrams)
5. [Activity Diagrams](#activity-diagrams)
6. [Component Diagram](#component-diagram)
7. [Deployment Diagram](#deployment-diagram)

---

## Class Diagram

### Database Models Class Diagram

```mermaid
classDiagram
    class User {
        +id: int
        +username: string
        +email: string
        +password: string
        +first_name: string
        +last_name: string
        +date_joined: datetime
        +is_active: boolean
    }

    class Profile {
        +id: int
        +age: int
        +gender: string
        +bio: text
        +photo: ImageField
        +email_token: UUID
        +is_verified: boolean
        +user_id: int
        +__str__(): string
    }

    class Preferences {
        +id: int
        +gender: string
        +room_sharing: int
        +ac_preference: string
        +bedtime: string
        +cleanliness: string
        +noise_tolerance: string
        +guest_frequency: string
        +smoking: string
        +food_type: string
        +personality: string
        +pet_tolerance: string
        +language: string
        +sharing_belongings: string
        +education: string
        +group_study: string
        +call_frequency: string
        +study_importance: string
        +user_id: int
        +__str__(): string
    }

    class Room {
        +id: int
        +room_number: string
        +room_type: string
        +total_beds: int
        +occupied_beds: int
        +gender: string
        +ac_type: string
        +room_category: string
        +available_beds(): int
        +save(): void
        +__str__(): string
    }

    class Booking {
        +id: int
        +user_id: int
        +room_id: int
        +booked_at: datetime
        +__str__(): string
    }

    class ChatRoom {
        +id: int
        +created_at: datetime
        +__str__(): string
    }

    class Message {
        +id: int
        +content: text
        +message_type: string
        +file: FileField
        +timestamp: datetime
        +room_id: int
        +sender_id: int
        +file_size: property
        +file_name: property
        +__str__(): string
    }

    class BlockedUser {
        +id: int
        +blocker_id: int
        +blocked_id: int
        +created_at: datetime
        +__str__(): string
    }

    class UserReport {
        +id: int
        +reporter_id: int
        +reported_user_id: int
        +reason: string
        +description: text
        +created_at: datetime
        +is_resolved: boolean
        +__str__(): string
    }

    %% Relationships
    User ||--|| Profile : "has one"
    User ||--|| Preferences : "has one"
    User ||--o{ Booking : "makes many"
    Room ||--o{ Booking : "has many"
    User }o--o{ ChatRoom : "participates in many"
    ChatRoom ||--o{ Message : "contains many"
    User ||--o{ Message : "sends many"
    User ||--o{ BlockedUser : "blocks many (as blocker)"
    User ||--o{ BlockedUser : "blocked by many (as blocked)"
    User ||--o{ UserReport : "reports many (as reporter)"
    User ||--o{ UserReport : "reported by many (as reported)"
```

---

## Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password
        string first_name
        string last_name
        datetime date_joined
        boolean is_active
    }

    PROFILE {
        int id PK
        int user_id FK
        int age
        string gender
        text bio
        string photo
        uuid email_token
        boolean is_verified
    }

    PREFERENCES {
        int id PK
        int user_id FK
        string gender
        int room_sharing
        string ac_preference
        string bedtime
        string cleanliness
        string noise_tolerance
        string guest_frequency
        string smoking
        string food_type
        string personality
        string pet_tolerance
        string language
        string sharing_belongings
        string education
        string group_study
        string call_frequency
        string study_importance
    }

    ROOM {
        int id PK
        string room_number
        string room_type
        int total_beds
        int occupied_beds
        string gender
        string ac_type
        string room_category
    }

    BOOKING {
        int id PK
        int user_id FK
        int room_id FK
        datetime booked_at
    }

    CHATROOM {
        int id PK
        datetime created_at
    }

    CHATROOM_USERS {
        int chatroom_id FK
        int user_id FK
    }

    MESSAGE {
        int id PK
        int room_id FK
        int sender_id FK
        text content
        string message_type
        string file
        datetime timestamp
    }

    BLOCKED_USER {
        int id PK
        int blocker_id FK
        int blocked_id FK
        datetime created_at
    }

    USER_REPORT {
        int id PK
        int reporter_id FK
        int reported_user_id FK
        string reason
        text description
        datetime created_at
        boolean is_resolved
    }

    %% Relationships
    USER ||--|| PROFILE : "has"
    USER ||--|| PREFERENCES : "has"
    USER ||--o{ BOOKING : "makes"
    ROOM ||--o{ BOOKING : "receives"
    USER }o--o{ CHATROOM : "participates"
    CHATROOM ||--o{ MESSAGE : "contains"
    USER ||--o{ MESSAGE : "sends"
    USER ||--o{ BLOCKED_USER : "blocks_as_blocker"
    USER ||--o{ BLOCKED_USER : "blocked_as_blocked"
    USER ||--o{ USER_REPORT : "reports_as_reporter"
    USER ||--o{ USER_REPORT : "reported_as_reported"
```

---

## Use Case Diagram

```mermaid
graph TB
    subgraph "RoomieRadar System"
        subgraph "Authentication"
            UC1[Register Account]
            UC2[Login]
            UC3[Verify Email]
            UC4[Logout]
        end

        subgraph "Profile Management"
            UC5[Create Profile]
            UC6[Update Profile]
            UC7[View Profile]
            UC8[Set Preferences]
        end

        subgraph "Room & Booking"
            UC9[Search Rooms]
            UC10[View Room Details]
            UC11[Book Room]
            UC12[View My Bookings]
            UC13[Cancel Booking]
        end

        subgraph "Roommate Matching"
            UC14[Find Matches]
            UC15[View Match Details]
            UC16[Filter Matches]
        end

        subgraph "Chat System"
            UC17[Start Chat]
            UC18[Send Message]
            UC19[Send File]
            UC20[Block User]
            UC21[Report User]
            UC22[View Chat History]
        end

        subgraph "Admin Functions"
            UC23[Manage Users]
            UC24[Manage Rooms]
            UC25[Handle Reports]
        end
    end

    %% Actors
    User((User))
    Admin((Admin))
    System((System))

    %% User interactions
    User --> UC1
    User --> UC2
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    User --> UC11
    User --> UC12
    User --> UC13
    User --> UC14
    User --> UC15
    User --> UC16
    User --> UC17
    User --> UC18
    User --> UC19
    User --> UC20
    User --> UC21
    User --> UC22

    %% Admin interactions
    Admin --> UC23
    Admin --> UC24
    Admin --> UC25

    %% System interactions
    System --> UC3
```

---

## Sequence Diagrams

### 1. User Registration and Email Verification

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web Interface
    participant V as Views
    participant M as Models
    participant E as Email Service

    U->>W: Fill registration form
    W->>V: POST /accounts/register/
    V->>M: Create User
    V->>M: Create Profile with email_token
    V->>E: Send verification email
    E->>U: Email with verification link
    U->>W: Click verification link
    W->>V: GET /accounts/verify/{token}/
    V->>M: Update Profile.is_verified = True
    V->>W: Redirect to login
    W->>U: Show login page
```

### 2. Roommate Matching Process

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web Interface
    participant V as Views
    participant M as Match Utils
    participant DB as Database

    U->>W: Access matches page
    W->>V: GET /matches/
    V->>DB: Get user preferences
    V->>M: find_best_matches(user)
    M->>DB: Query compatible users
    M->>M: Calculate compatibility scores
    M->>V: Return sorted matches
    V->>W: Render matches template
    W->>U: Display matched roommates
```

### 3. Chat Message Flow

```mermaid
sequenceDiagram
    participant U1 as User 1
    participant W as Web Interface
    participant V as Chat Views
    participant DB as Database
    participant U2 as User 2

    U1->>W: Type and send message
    W->>V: POST /chat/room/{id}/
    V->>DB: Check if users are blocked
    V->>DB: Create Message object
    V->>W: Redirect to chat room
    W->>U1: Show updated chat
    Note over U2: User 2 refreshes or visits chat
    U2->>W: Access chat room
    W->>V: GET /chat/room/{id}/
    V->>DB: Fetch all messages
    V->>W: Render chat template
    W->>U2: Display messages including new one
```

### 4. Room Booking Process

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web Interface
    participant V as Views
    participant DB as Database

    U->>W: Browse available rooms
    W->>V: GET /rooms/
    V->>DB: Query available rooms
    V->>W: Display rooms list
    U->>W: Click "Book Room"
    W->>V: POST /book-bed/{room_id}/
    V->>DB: Check existing bookings
    alt User has no existing booking
        V->>DB: Create Booking
        V->>DB: Update room.occupied_beds
        V->>W: Redirect to success page
        W->>U: Show booking confirmation
    else User already has booking
        V->>W: Show error message
        W->>U: Display "Already booked" error
    end
```

---

## Activity Diagrams

### 1. User Onboarding Flow

```mermaid
flowchart TD
    A[Start] --> B[Visit Registration Page]
    B --> C[Fill Registration Form]
    C --> D{Form Valid?}
    D -->|No| C
    D -->|Yes| E[Create Account]
    E --> F[Send Verification Email]
    F --> G[Check Email]
    G --> H[Click Verification Link]
    H --> I[Account Verified]
    I --> J[Login to System]
    J --> K[Create Profile]
    K --> L[Set Preferences]
    L --> M[Access Dashboard]
    M --> N[End]
```

### 2. Room Booking Flow

```mermaid
flowchart TD
    A[Start] --> B[Access Room Search]
    B --> C[Apply Filters]
    C --> D[View Available Rooms]
    D --> E{Found Suitable Room?}
    E -->|No| C
    E -->|Yes| F[Select Room]
    F --> G{Already Have Booking?}
    G -->|Yes| H[Show Error Message]
    H --> I[End]
    G -->|No| J[Confirm Booking]
    J --> K[Create Booking Record]
    K --> L[Update Room Occupancy]
    L --> M[Show Success Page]
    M --> N[End]
```

### 3. Chat Interaction Flow

```mermaid
flowchart TD
    A[Start] --> B[Access Chat Home]
    B --> C{Existing Conversations?}
    C -->|Yes| D[Show Chat List]
    C -->|No| E[Show Empty State]
    D --> F[Select Conversation]
    E --> G[Start New Chat]
    G --> F
    F --> H[Load Chat Room]
    H --> I[Display Messages]
    I --> J{User Action}
    J -->|Send Text| K[Send Message]
    J -->|Send File| L[Upload File]
    J -->|Block User| M[Block User]
    J -->|Report User| N[Report User]
    K --> O[Update Chat Display]
    L --> O
    M --> P[Update UI State]
    N --> P
    O --> Q{Continue Chat?}
    P --> Q
    Q -->|Yes| J
    Q -->|No| R[End]
```

---

## Component Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        T1[Templates]
        S1[Static Files]
        J1[JavaScript]
    end

    subgraph "Application Layer"
        subgraph "Django Apps"
            A1[accounts]
            A2[base]
            A3[chat]
            A4[home]
            A5[roomieradar_app]
        end
        
        subgraph "Views"
            V1[Authentication Views]
            V2[Profile Views]
            V3[Chat Views]
            V4[Room Views]
            V5[Matching Views]
        end
        
        subgraph "Utils"
            U1[Match Utils]
            U2[Email Utils]
        end
    end

    subgraph "Data Layer"
        subgraph "Models"
            M1[User Models]
            M2[Profile Models]
            M3[Chat Models]
            M4[Room Models]
        end
        
        D1[(SQLite Database)]
        F1[File Storage]
    end

    subgraph "External Services"
        E1[Email Service]
        E2[File Upload Service]
    end

    %% Connections
    T1 --> V1
    T1 --> V2
    T1 --> V3
    T1 --> V4
    T1 --> V5
    
    V1 --> M1
    V2 --> M2
    V3 --> M3
    V4 --> M4
    V5 --> M1
    V5 --> M2
    
    V5 --> U1
    V1 --> U2
    
    M1 --> D1
    M2 --> D1
    M3 --> D1
    M4 --> D1
    
    M2 --> F1
    M3 --> F1
    
    U2 --> E1
    M3 --> E2
```

---

## Deployment Diagram

```mermaid
graph TB
    subgraph "Client Tier"
        C1[Web Browser]
        C2[Mobile Browser]
    end

    subgraph "Web Server Tier"
        W1[Django Development Server]
        W2[Static File Server]
    end

    subgraph "Application Tier"
        A1[Django Application]
        A2[Python Runtime]
        A3[Virtual Environment]
    end

    subgraph "Data Tier"
        D1[(SQLite Database)]
        D2[File System Storage]
    end

    subgraph "External Services"
        E1[SMTP Email Server]
    end

    %% Connections
    C1 -.->|HTTP/HTTPS| W1
    C2 -.->|HTTP/HTTPS| W1
    W1 --> A1
    W2 --> D2
    A1 --> A2
    A2 --> A3
    A1 --> D1
    A1 --> D2
    A1 -.->|SMTP| E1

    %% Deployment Notes
    classDef client fill:#e1f5fe
    classDef server fill:#f3e5f5
    classDef data fill:#e8f5e8
    classDef external fill:#fff3e0

    class C1,C2 client
    class W1,W2,A1,A2,A3 server
    class D1,D2 data
    class E1 external
```

---

## Architecture Overview

### System Architecture Layers

1. **Presentation Layer**
   - HTML Templates with Django Template Language
   - CSS with modern responsive design
   - JavaScript for interactive features
   - Bootstrap/Custom CSS frameworks

2. **Business Logic Layer**
   - Django Views handling HTTP requests
   - Custom utility functions (matching algorithms)
   - Form validation and processing
   - Authentication and authorization

3. **Data Access Layer**
   - Django ORM for database operations
   - Model definitions and relationships
   - Database migrations
   - File upload handling

4. **Data Storage Layer**
   - SQLite database for development
   - File system for media storage
   - Session storage
   - Cache storage (if implemented)

### Key Design Patterns Used

1. **Model-View-Template (MVT)** - Django's architectural pattern
2. **Repository Pattern** - Django ORM acts as repository
3. **Factory Pattern** - Model creation and form handling
4. **Observer Pattern** - Django signals (if used)
5. **Strategy Pattern** - Different matching algorithms

---

## Database Schema Summary

### Core Tables
- **auth_user**: Django's built-in user authentication
- **base_profile**: Extended user profile information
- **base_preferences**: User roommate preferences
- **roomieradar_app_room**: Room inventory
- **roomieradar_app_booking**: Room bookings
- **chat_chatroom**: Chat room instances
- **chat_message**: Chat messages
- **chat_blockeduser**: User blocking relationships
- **chat_userreport**: User reporting system

### Key Relationships
- One-to-One: User ↔ Profile, User ↔ Preferences
- One-to-Many: User → Bookings, Room → Bookings, ChatRoom → Messages
- Many-to-Many: User ↔ ChatRoom (participants)

---

## Notes for Documentation

1. **For Academic Presentation**: Focus on Use Case and Sequence diagrams to show system functionality
2. **For Technical Documentation**: Emphasize Class and Component diagrams for system architecture
3. **For Database Design**: Use ERD to show data relationships and constraints
4. **For System Deployment**: Use Deployment diagram to show infrastructure setup

These UML diagrams provide comprehensive documentation for your RoomieRadar project and can be used in academic presentations, technical documentation, or system design discussions.