# RoomieRadar - Technical Documentation

## 🏗️ System Architecture

### Overview
RoomieRadar follows Django's Model-View-Template (MVT) architecture pattern with a modular app-based structure.

### Application Modules

#### 1. Accounts App
- **Purpose**: User authentication and account management
- **Key Files**:
  - `models.py`: User profile extensions
  - `views.py`: Registration, login, activation
  - `emails.py`: Email notification system
  - `urls.py`: Authentication routes

#### 2. Base App
- **Purpose**: Core functionality and matching logic
- **Key Files**:
  - `models.py`: Profile and Preferences models
  - `views.py`: Dashboard and profile management
  - `match_utils.py`: Compatibility algorithm

#### 3. Chat App
- **Purpose**: Real-time messaging system
- **Key Files**:
  - `models.py`: Message and conversation models
  - `views.py`: Chat interface and message handling

#### 4. RoomieRadar App
- **Purpose**: Room booking and management
- **Key Files**:
  - `models.py`: Room and Booking models
  - `views.py`: Room listing and booking logic

#### 5. Home App
- **Purpose**: Landing pages and static content
- **Key Files**:
  - `views.py`: Homepage and feature pages
  - Templates for marketing pages

## 🧮 Matching Algorithm

### Compatibility Calculation
```python
def calculate_similarity(user_pref, candidate_pref):
    fields = [
        'bedtime', 'cleanliness', 'noise_tolerance',
        'guest_frequency', 'smoking_alcohol', 'food_type',
        'personality', 'pet_tolerance', 'language',
        'sharing_belongings', 'education', 'group_study',
        'call_frequency', 'study_importance'
    ]
    
    score = 0
    total = len(fields)
    
    for field in fields:
        if getattr(user_pref, field, None) == getattr(candidate_pref, field, None):
            score += 1
    
    return round((score / total) * 100, 2)
```

### Matching Process
1. Filter users by basic criteria (gender, room type, AC preference)
2. Calculate compatibility scores for all potential matches
3. Sort by compatibility percentage
4. Return top 5 matches

## 🔐 Security Features

### Authentication
- Django's built-in authentication system
- Email verification required
- Password validation rules
- Session management

### Data Protection
- CSRF protection enabled
- XSS filtering
- SQL injection prevention through ORM
- Secure password hashing

### Privacy Controls
- Profile visibility settings
- User blocking and reporting
- Data anonymization options

## 📊 Database Design

### Key Relationships
- User ↔ Profile (One-to-One)
- User ↔ Preferences (One-to-One)
- User ↔ Booking (One-to-Many)
- Room ↔ Booking (One-to-Many)

### Indexing Strategy
- Primary keys on all models
- Foreign key indexes
- Email field indexing for quick lookups

## 🎨 Frontend Architecture

### Design System
- CSS Custom Properties for theming
- Gradient-based color scheme
- Responsive grid layouts
- Mobile-first approach

### Interactive Elements
- Smooth animations and transitions
- Hover effects and micro-interactions
- Form validation feedback
- Loading states

### Performance Optimization
- Minified CSS and JavaScript
- Image optimization
- Lazy loading for images
- Efficient DOM manipulation

## 📧 Email System

### Configuration
- SMTP integration with Gmail
- HTML email templates
- Plain text fallbacks
- Custom sender branding

### Email Types
- Account activation
- Password reset
- Booking confirmations
- Match notifications

## 🔄 Deployment Pipeline

### Development
1. Local development with SQLite
2. Debug mode enabled
3. Development server

### Production
1. PostgreSQL database
2. Static file serving
3. Environment variables
4. Error logging

## 📈 Performance Considerations

### Database Optimization
- Efficient queries with select_related
- Pagination for large datasets
- Database connection pooling

### Caching Strategy
- Template fragment caching
- Database query caching
- Static file caching

### Scalability
- Modular app structure
- Stateless design
- Horizontal scaling ready

## 🐛 Error Handling

### User-Friendly Messages
- Form validation errors
- Success confirmations
- Warning notifications
- Error page templates

### Logging
- Application error logging
- User action tracking
- Performance monitoring
- Security event logging

## 🔧 Configuration Management

### Settings Structure
- Base settings
- Development overrides
- Production configuration
- Environment variables

### Feature Flags
- Debug mode toggle
- Email backend switching
- Database configuration
- Static file handling