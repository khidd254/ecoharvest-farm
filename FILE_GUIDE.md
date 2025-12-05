# File Guide - Appointment Booking System

Complete guide to all files in the project and their purposes.

---

## 📁 Project Files Overview

### 🔧 Configuration & Setup Files

#### `requirements.txt`
**Purpose**: Python package dependencies
**Contains**: List of all required packages with versions
**Usage**: `pip install -r requirements.txt`
**Key Packages**:
- fastapi: Web framework
- uvicorn: ASGI server
- sqlalchemy: Database ORM
- pydantic: Data validation
- aiosqlite: Async SQLite driver

#### `.env.example`
**Purpose**: Environment configuration template
**Contains**: Configuration variables for the application
**Usage**: Copy to `.env` and modify as needed
**Variables**:
- DATABASE_URL: Database connection string
- HOST/PORT: Server configuration
- BUSINESS_HOURS: Operating hours
- SESSION_DURATION: Appointment length

#### `run.bat`
**Purpose**: Windows startup script
**Usage**: Double-click or run `run.bat` in Command Prompt
**Does**:
1. Checks Python installation
2. Creates virtual environment if needed
3. Installs dependencies
4. Starts the application

#### `run.sh`
**Purpose**: macOS/Linux startup script
**Usage**: `chmod +x run.sh && ./run.sh`
**Does**:
1. Checks Python installation
2. Creates virtual environment if needed
3. Installs dependencies
4. Starts the application

---

## 🐍 Backend Files

### `main.py` (400+ lines)
**Purpose**: FastAPI application and route definitions
**Key Components**:
- FastAPI app initialization
- CORS middleware configuration
- WebSocket endpoint for real-time notifications
- REST API endpoints:
  - Appointment CRUD operations
  - Availability management
  - Calendar views
  - Notification handling
  - Health checks

**Key Functions**:
- `create_appointment()`: POST /api/appointments
- `list_appointments()`: GET /api/appointments
- `get_appointment()`: GET /api/appointments/{id}
- `delete_appointment()`: DELETE /api/appointments/{id}
- `get_available_slots()`: GET /api/available-slots
- `get_calendar()`: GET /api/calendar
- `get_notifications()`: GET /api/notifications
- `websocket_endpoint()`: WS /ws/notifications
- `broadcast_notification()`: Send real-time updates

**Dependencies**: database, models, schemas, services

---

### `database.py` (60+ lines)
**Purpose**: Database configuration and session management
**Key Components**:
- SQLAlchemy async engine setup
- Session factory configuration
- Database initialization function
- Dependency injection for FastAPI

**Key Functions**:
- `init_db()`: Create all database tables
- `get_db()`: FastAPI dependency for database sessions

**Configuration**:
- DATABASE_URL: SQLite by default
- Connection pooling for performance
- Async support for non-blocking operations

---

### `models.py` (150+ lines)
**Purpose**: SQLAlchemy ORM database models
**Models**:

#### Owner
- Represents the service provider
- Fields: id, name, email, phone, business_hours_start, business_hours_end, created_at
- Relationships: appointments, notifications

#### Appointment
- Represents a booked appointment
- Fields: id, owner_id, client_name, client_email, client_phone, appointment_time, duration_minutes, status, notes, created_at, updated_at
- Relationships: owner, notifications
- Properties: end_time (calculated)

#### Notification
- Represents system notifications
- Fields: id, owner_id, appointment_id, notification_type, message, is_read, created_at
- Relationships: owner, appointment

---

### `schemas.py` (150+ lines)
**Purpose**: Pydantic request/response validation schemas
**Schemas**:

#### AppointmentCreate
- Request schema for creating appointments
- Fields: client_name, client_email, client_phone, appointment_time, notes
- Validation: Email format, future dates, required fields

#### AppointmentResponse
- Response schema for appointments
- Fields: All appointment fields
- Used for: API responses

#### AvailableSlotResponse
- Response schema for available time slots
- Fields: time, end_time, is_available
- Used for: /api/available-slots endpoint

#### NotificationResponse
- Response schema for notifications
- Fields: id, appointment_id, notification_type, message, is_read, created_at
- Used for: /api/notifications endpoint

#### OwnerResponse
- Response schema for owner information
- Fields: id, name, email, phone, business_hours_start, business_hours_end

#### CalendarEventResponse
- Response schema for calendar events
- Fields: id, title, start, end, client_name, client_email, status

---

### `services.py` (350+ lines)
**Purpose**: Business logic services
**Services**:

#### AppointmentService
- Handles appointment CRUD operations
- Methods:
  - `create_appointment()`: Create new appointment
  - `get_all_appointments()`: Retrieve all appointments
  - `get_appointment()`: Get specific appointment
  - `delete_appointment()`: Cancel appointment
  - `get_calendar_view()`: Get calendar data

#### AvailabilityService
- Manages appointment availability and slot generation
- Configuration:
  - BUSINESS_START: 8:00 AM
  - BUSINESS_END: 6:00 PM
  - SESSION_DURATION: 120 minutes
  - BREAK_DURATION: 15 minutes
  - LUNCH_START: 12:00 PM
  - LUNCH_END: 1:00 PM
- Methods:
  - `check_availability()`: Verify slot is available
  - `get_available_slots()`: Generate available slots for a date
  - `_is_within_business_hours()`: Validate business hours
  - `_is_lunch_break()`: Check lunch break conflict

#### NotificationService
- Manages notifications
- Methods:
  - `create_notification()`: Create new notification
  - `get_all_notifications()`: Retrieve all notifications
  - `get_unread_notifications()`: Get unread only
  - `mark_as_read()`: Mark notification as read

---

## 🎨 Frontend Files

### `frontend/index.html` (50+ lines)
**Purpose**: HTML entry point for the web application
**Contains**:
- HTML structure
- Meta tags for responsiveness
- CDN links for React, Tailwind CSS, Lucide icons
- CSS styling (gradients, animations, glass effect)
- Root div for React mounting

**Styles**:
- Gradient backgrounds
- Glass morphism effects
- Smooth transitions
- Responsive design

---

### `frontend/app.js` (600+ lines)
**Purpose**: React application with all UI components
**Key Components**:

#### ApiService
- Centralized API communication layer
- Methods:
  - `getAvailableSlots()`: Fetch available time slots
  - `createAppointment()`: Book appointment
  - `getAppointments()`: List all appointments
  - `getCalendar()`: Get calendar view
  - `getNotifications()`: Fetch notifications
  - `markNotificationRead()`: Mark notification as read

#### NotificationCenter
- Real-time notification display
- Features:
  - WebSocket connection for live updates
  - Notification badge with unread count
  - Notification dropdown panel
  - Auto-dismiss after 5 seconds

#### BookingForm
- Appointment booking interface
- Features:
  - Client information input
  - Date selection
  - Time slot selection
  - Form validation
  - Success/error messages
  - Loading states

#### CalendarView
- Display all scheduled appointments
- Features:
  - Appointments grouped by date
  - Client information display
  - Appointment status
  - Responsive layout

#### App
- Main application component
- Features:
  - Tab navigation (Booking/Calendar)
  - Header with notifications
  - Footer with business hours
  - State management

---

## 📚 Documentation Files

### `README.md` (500+ lines)
**Purpose**: Complete project documentation
**Sections**:
- Features overview
- Project structure
- Getting started guide
- API documentation (all endpoints)
- Architecture overview
- Database schema
- Security considerations
- Testing procedures
- Configuration options
- Troubleshooting guide
- Dependencies list

**Use When**: Need complete API reference or feature details

---

### `SETUP.md` (400+ lines)
**Purpose**: Detailed setup instructions for all platforms
**Sections**:
- Prerequisites
- Windows setup (step-by-step)
- macOS setup (step-by-step)
- Linux setup (step-by-step)
- Verification procedures
- Configuration options
- Advanced setup (Docker, PostgreSQL, etc.)
- Troubleshooting guide
- Setup checklist

**Use When**: Installing the system for the first time

---

### `QUICK_START.md` (50+ lines)
**Purpose**: 5-minute quick start guide
**Sections**:
- Quick start for Windows
- Quick start for macOS/Linux
- What's included
- Testing procedures
- Getting help

**Use When**: Want to get running immediately

---

### `TESTING.md` (400+ lines)
**Purpose**: Comprehensive testing guide
**Sections**:
- Manual testing procedures (7 tests)
- API testing with cURL (10 tests)
- Edge case testing (5 tests)
- Performance testing (2 tests)
- Browser console testing
- Test checklist
- Debugging tips
- Test report template

**Use When**: Testing the system or verifying functionality

---

### `PROJECT_SUMMARY.md` (300+ lines)
**Purpose**: High-level project overview
**Sections**:
- Project overview
- Key features delivered
- Project structure
- Architecture diagrams
- API endpoints summary
- Database schema
- UI/UX features
- Getting started
- Technology stack
- Future enhancements
- Success criteria checklist

**Use When**: Need project overview or status report

---

### `FILE_GUIDE.md` (This file)
**Purpose**: Guide to all project files
**Sections**:
- Configuration files
- Backend files
- Frontend files
- Documentation files

**Use When**: Need to understand file organization

---

## 📊 File Statistics

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| Backend | 5 | 1000+ | Core application logic |
| Frontend | 2 | 650+ | User interface |
| Configuration | 4 | 100+ | Setup and environment |
| Documentation | 6 | 1500+ | Guides and references |
| **Total** | **17** | **3250+** | Complete system |

---

## 🔄 File Dependencies

```
main.py
├── database.py
├── models.py
├── schemas.py
└── services.py
    └── models.py

frontend/app.js
└── (No dependencies - standalone React app)

Documentation files
└── (Independent - reference only)
```

---

## 📝 File Modification Guide

### To Add a New Endpoint
1. Edit `main.py` - Add route
2. Edit `services.py` - Add business logic
3. Edit `schemas.py` - Add request/response schemas
4. Update `README.md` - Document endpoint

### To Change Business Hours
1. Edit `services.py` - Update AvailabilityService constants
2. Update `README.md` - Document change
3. Update `.env.example` - If using environment variables

### To Add a New Database Field
1. Edit `models.py` - Add field to model
2. Delete `appointments.db` - Reset database
3. Restart application - Database recreates with new schema
4. Update `schemas.py` - Add field to schemas
5. Update `README.md` - Document change

### To Modify Frontend
1. Edit `frontend/app.js` - Update React components
2. Edit `frontend/index.html` - Update HTML/CSS if needed
3. No restart needed - Browser will reload

### To Update Documentation
1. Edit relevant `.md` file
2. Keep consistent with code changes
3. Update PROJECT_SUMMARY.md if major changes

---

## 🗂️ File Organization Best Practices

### Backend Organization
```
Backend files handle:
- models.py: Data structure (what)
- schemas.py: Validation (how to validate)
- services.py: Logic (how to process)
- database.py: Storage (where to store)
- main.py: Routes (when to call)
```

### Frontend Organization
```
Frontend file handles:
- index.html: Structure (markup)
- app.js: Logic (components & state)
- Styling: Tailwind CSS (inline)
- API calls: ApiService (centralized)
```

### Documentation Organization
```
Documentation files handle:
- README.md: Complete reference
- SETUP.md: Installation guide
- QUICK_START.md: Fast start
- TESTING.md: Test procedures
- PROJECT_SUMMARY.md: Overview
- FILE_GUIDE.md: File organization
```

---

## 🔐 File Permissions

### Windows
- All files: Read/Write for user
- `run.bat`: Executable

### macOS/Linux
- All files: Read/Write for user
- `run.sh`: Executable (chmod +x)
- Database file: Read/Write

---

## 💾 Backup Recommendations

### Critical Files to Backup
- `appointments.db` - Contains all appointment data
- `.env` - Contains configuration (if created)

### Safe to Regenerate
- `venv/` - Virtual environment (can be recreated)
- `__pycache__/` - Python cache (auto-generated)

### Version Control
Recommended `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
appointments.db
.DS_Store
```

---

## 📋 File Checklist

Before deployment, verify:
- [ ] All `.py` files present and readable
- [ ] `requirements.txt` has all dependencies
- [ ] `frontend/` folder has `index.html` and `app.js`
- [ ] Documentation files are complete
- [ ] `run.bat` and `run.sh` are executable
- [ ] `.env.example` is present
- [ ] No sensitive data in any files
- [ ] All code is properly commented

---

## 🚀 Quick File Reference

| Need | File |
|------|------|
| Start application | `run.bat` or `run.sh` |
| API documentation | `README.md` |
| Setup help | `SETUP.md` |
| Quick start | `QUICK_START.md` |
| Testing | `TESTING.md` |
| Project overview | `PROJECT_SUMMARY.md` |
| File guide | `FILE_GUIDE.md` |
| Add endpoint | `main.py` + `services.py` |
| Change business hours | `services.py` |
| Modify UI | `frontend/app.js` |
| Database schema | `models.py` |
| Data validation | `schemas.py` |

---

**Total Project Files**: 17  
**Total Lines of Code**: 3250+  
**Documentation**: Complete  
**Status**: Production Ready ✅
