# RoomieRadar - Student Roommate Matching Platform

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation Guide](#installation-guide)
- [Usage Instructions](#usage-instructions)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

RoomieRadar is a comprehensive web-based platform designed to help students find compatible roommates and suitable accommodation within their educational institutions. The system uses intelligent matching algorithms to connect students based on lifestyle preferences, study habits, and personality traits.

### Problem Statement
Students often struggle to find compatible roommates, leading to uncomfortable living situations and academic stress. Traditional methods of roommate finding are inefficient and don't consider compatibility factors.

### Solution
RoomieRadar provides a secure, verified platform where students can:
- Create detailed profiles with preferences
- Get matched with compatible roommates using AI algorithms
- Chat with potential roommates before making decisions
- Book accommodation through the platform
- Access safety features and verified profiles

## ✨ Features

### Core Features
- **Smart Matching Algorithm**: AI-powered compatibility analysis
- **User Authentication**: Secure registration and login system
- **Profile Management**: Comprehensive user profiles with preferences
- **Real-time Messaging**: Instant chat system between matched users
- **Room Booking**: Integrated accommodation booking system
- **Verification System**: Email verification and profile validation

### Advanced Features
- **Responsive Design**: Mobile-friendly interface
- **Email Notifications**: Automated email system for account activation
- **Search & Filters**: Advanced filtering for rooms and roommates
- **Safety Features**: User reporting and blocking system
- **Dashboard Analytics**: Personal statistics and match history

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Language**: Python 3.8+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django's built-in authentication system

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive features and AJAX
- **Responsive Design**: Mobile-first approach

### Additional Tools
- **Email Service**: SMTP integration for notifications
- **Version Control**: Git
- **Development Server**: Django development server

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/roomieradar.git
   cd roomieradar
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Create .env file with the following:
   SECRET_KEY=your-secret-key
   DEBUG=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 📖 Usage Instructions

### For Students

1. **Registration**
   - Visit the homepage
   - Click "Create Account"
   - Fill in required details with institutional email
   - Verify email through activation link

2. **Profile Setup**
   - Complete profile with personal information
   - Set roommate preferences (cleanliness, study habits, etc.)
   - Upload profile picture

3. **Finding Roommates**
   - Navigate to "Find Matches"
   - View compatibility scores
   - Chat with potential roommates
   - Make final decisions

4. **Booking Accommodation**
   - Browse available rooms
   - Filter by preferences (AC, sharing, gender)
   - Book suitable accommodation

### For Administrators

1. **User Management**
   - Access admin panel
   - Manage user accounts and profiles
   - Handle verification requests

2. **Room Management**
   - Add/edit room information
   - Manage booking status
   - Update availability

## 🏗 System Architecture

### Application Structure
```
RoomieRadar/
├── accounts/           # User authentication and management
├── base/              # Core models and matching logic
├── chat/              # Messaging system
├── home/              # Landing pages and static content
├── roomieradar_app/   # Room booking and management
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # User uploaded files
└── roomieradar/      # Project settings
```

### Key Components
- **Authentication System**: Handles user registration, login, and verification
- **Matching Algorithm**: Calculates compatibility scores based on preferences
- **Messaging System**: Real-time chat between matched users
- **Booking System**: Room reservation and management
- **Admin Interface**: Backend management tools

## 🗄 Database Schema

### Core Models

#### User (Django's built-in)
- username, email, password
- first_name, last_name
- is_active, date_joined

#### Profile (base/models.py)
- user (OneToOne with User)
- phone, gender, age
- profile_picture
- email_token, is_verified

#### Preferences (base/models.py)
- user (OneToOne with User)
- room_sharing, budget_min, budget_max
- cleanliness, noise_tolerance, bedtime
- study_importance, personality
- smoking_alcohol, food_type

#### Room (roomieradar_app/models.py)
- room_number, room_type
- total_beds, occupied_beds
- gender, ac_type, room_category

#### Booking (roomieradar_app/models.py)
- user (ForeignKey to User)
- room (ForeignKey to Room)
- booked_at

## 🔧 API Documentation

### Authentication Endpoints
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login
- `GET /accounts/activate/` - Email verification
- `POST /accounts/logout/` - User logout

### Profile Endpoints
- `GET /profile/` - View user profile
- `POST /profile/` - Update profile
- `GET /preferences/` - View preferences
- `POST /preferences/` - Update preferences

### Matching Endpoints
- `GET /matches/` - Get compatible roommates
- `POST /matches/filter/` - Apply filters

### Booking Endpoints
- `GET /rooms/` - List available rooms
- `POST /rooms/book/<id>/` - Book a room
- `GET /bookings/` - View user bookings

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### Test Coverage
- Unit tests for models
- Integration tests for views
- Form validation tests
- Authentication flow tests

### Manual Testing Checklist
- [ ] User registration and email verification
- [ ] Profile creation and updates
- [ ] Matching algorithm accuracy
- [ ] Chat functionality
- [ ] Room booking process
- [ ] Responsive design on mobile devices

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           # PostgreSQL configuration
       }
   }
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Migration**
   ```bash
   python manage.py migrate --settings=roomieradar.settings.production
   ```

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: VPS with custom configuration
- **AWS**: Scalable cloud deployment
- **PythonAnywhere**: Simple hosting for Django apps

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Email: support@roomieradar.com
- Documentation: [Wiki](https://github.com/yourusername/roomieradar/wiki)
- Issues: [GitHub Issues](https://github.com/yourusername/roomieradar/issues)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap for responsive design components
- Font Awesome for icons
- All contributors and testers

---

**RoomieRadar** - Making student accommodation easier, one match at a time! 🏠✨