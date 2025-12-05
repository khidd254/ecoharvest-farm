# Appointment Booking System

A professional, full-stack appointment booking system built with FastAPI and React. Features real-time notifications, conflict detection, and an intuitive calendar interface.

## 🎯 Features

### Core Functionality
- **Appointment Booking**: Clients can book appointments through an intuitive web interface
- **Availability Management**: Automatic slot generation based on business hours
- **Conflict Detection**: Prevents double-booking and overlapping appointments
- **Real-time Notifications**: WebSocket-based instant notifications to the owner
- **Calendar View**: Visual representation of all scheduled appointments
- **Responsive Design**: Beautiful, modern UI that works on all devices

### Business Rules
- **Business Hours**: 8:00 AM - 6:00 PM
- **Session Duration**: 2 hours per appointment
- **Break Duration**: 15 minutes between sessions
- **Lunch Break**: 12:00 PM - 1:00 PM (no appointments)
- **No Overlapping**: System prevents double-booking

### Technical Features
- **Async/Await**: Non-blocking database operations
- **WebSocket Support**: Real-time notifications
- **CORS Enabled**: Cross-origin requests supported
- **SQLite Database**: Lightweight, file-based persistence
- **Comprehensive Logging**: Detailed documentation and error handling
- **RESTful API**: Clean, well-documented endpoints

## 📋 Project Structure

```
appointment-handling/
├── main.py                 # FastAPI application and routes
├── database.py             # Database configuration and session management
├── models.py               # SQLAlchemy ORM models
├── schemas.py              # Pydantic request/response schemas
├── services.py             # Business logic services
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── frontend/
    ├── index.html          # HTML entry point
    └── app.js              # React application
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "f:\Projects\appointment handling"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI server**
   ```bash
   python main.py
   ```

   The server will start at `http://localhost:8000`

2. **Open your browser**
   Navigate to `http://localhost:8000` to access the application

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Appointments

**Create Appointment**
```
POST /appointments
Content-Type: application/json

{
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "client_phone": "+1234567890",
  "appointment_time": "2024-01-15T10:00:00",
  "notes": "First time client"
}

Response: 201 Created
{
  "id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "client_phone": "+1234567890",
  "appointment_time": "2024-01-15T10:00:00",
  "duration_minutes": 120,
  "status": "confirmed",
  "notes": "First time client",
  "created_at": "2024-01-15T09:00:00",
  "updated_at": "2024-01-15T09:00:00"
}
```

**Get All Appointments**
```
GET /appointments

Response: 200 OK
[
  {
    "id": 1,
    "client_name": "John Doe",
    ...
  }
]
```

**Get Specific Appointment**
```
GET /appointments/{appointment_id}

Response: 200 OK
{
  "id": 1,
  ...
}
```

**Delete Appointment**
```
DELETE /appointments/{appointment_id}

Response: 204 No Content
```

#### Availability

**Get Available Slots**
```
GET /available-slots?date=2024-01-15

Response: 200 OK
[
  {
    "time": "2024-01-15T08:00:00",
    "end_time": "2024-01-15T10:00:00",
    "is_available": true
  },
  {
    "time": "2024-01-15T10:15:00",
    "end_time": "2024-01-15T12:00:00",
    "is_available": false
  }
]
```

#### Calendar

**Get Calendar View**
```
GET /calendar

Response: 200 OK
{
  "2024-01-15": [
    {
      "id": 1,
      "client_name": "John Doe",
      "client_email": "john@example.com",
      "start_time": "2024-01-15T10:00:00",
      "end_time": "2024-01-15T12:00:00",
      "status": "confirmed"
    }
  ]
}
```

#### Notifications

**Get All Notifications**
```
GET /notifications

Response: 200 OK
[
  {
    "id": 1,
    "appointment_id": 1,
    "notification_type": "new_appointment",
    "message": "New appointment from John Doe on 2024-01-15 10:00",
    "is_read": false,
    "created_at": "2024-01-15T09:00:00"
  }
]
```

**Get Unread Notifications**
```
GET /notifications/unread

Response: 200 OK
[...]
```

**Mark Notification as Read**
```
PATCH /notifications/{notification_id}/read

Response: 200 OK
{
  "message": "Notification marked as read"
}
```

#### Health Check

**System Status**
```
GET /health

Response: 200 OK
{
  "status": "healthy",
  "timestamp": "2024-01-15T09:00:00",
  "service": "Appointment Booking System"
}
```

### WebSocket

**Real-time Notifications**
```
WebSocket: ws://localhost:8000/ws/notifications

Message Format:
{
  "type": "new_appointment",
  "title": "New Appointment Booking",
  "message": "New appointment from John Doe on 2024-01-15 10:00",
  "appointment_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "appointment_time": "2024-01-15T10:00:00"
}
```

## 🏗️ Architecture

### Backend (FastAPI)

**main.py**
- FastAPI application setup
- Route definitions
- WebSocket endpoint for real-time notifications
- CORS middleware configuration

**database.py**
- SQLAlchemy async engine setup
- Session management
- Database initialization

**models.py**
- Owner: Service provider information
- Appointment: Booking details
- Notification: System notifications

**schemas.py**
- Pydantic models for request/response validation
- Data transformation and validation rules

**services.py**
- AppointmentService: Appointment CRUD operations
- AvailabilityService: Slot availability and conflict detection
- NotificationService: Notification management

### Frontend (React)

**index.html**
- HTML entry point
- Tailwind CSS styling
- React CDN links

**app.js**
- React components
- API service layer
- State management
- Real-time notification handling

## 🔐 Security Considerations

1. **Input Validation**: All inputs are validated using Pydantic schemas
2. **CORS**: Configured to allow cross-origin requests (adjust as needed)
3. **Email Validation**: Email addresses are validated using EmailStr
4. **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
5. **Database**: Uses parameterized queries to prevent SQL injection

## 🧪 Testing the System

### Manual Testing

1. **Book an Appointment**
   - Navigate to the booking form
   - Fill in client details
   - Select a date and available time slot
   - Submit the form
   - Verify confirmation message

2. **Check Real-time Notifications**
   - Open the notification center
   - Book an appointment
   - Verify notification appears in real-time

3. **View Calendar**
   - Click "View Calendar" tab
   - Verify all appointments are displayed
   - Check appointment details

4. **Test Conflict Detection**
   - Try to book an appointment at an already booked time
   - Verify error message appears

### API Testing with cURL

```bash
# Get available slots
curl "http://localhost:8000/api/available-slots?date=2024-01-15"

# Create appointment
curl -X POST "http://localhost:8000/api/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "client_phone": "+1234567890",
    "appointment_time": "2024-01-15T10:00:00",
    "notes": "Test appointment"
  }'

# Get all appointments
curl "http://localhost:8000/api/appointments"

# Get calendar
curl "http://localhost:8000/api/calendar"

# Health check
curl "http://localhost:8000/api/health"
```

## 📊 Database Schema

### owners table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Owner's name |
| email | String | Owner's email (unique) |
| phone | String | Owner's phone |
| business_hours_start | String | Start time (HH:MM) |
| business_hours_end | String | End time (HH:MM) |
| created_at | DateTime | Creation timestamp |

### appointments table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| owner_id | Integer | Foreign key to owners |
| client_name | String | Client's name |
| client_email | String | Client's email |
| client_phone | String | Client's phone |
| appointment_time | DateTime | Appointment start time |
| duration_minutes | Integer | Appointment duration |
| status | String | confirmed/cancelled/completed |
| notes | Text | Additional notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### notifications table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| owner_id | Integer | Foreign key to owners |
| appointment_id | Integer | Foreign key to appointments |
| notification_type | String | Type of notification |
| message | Text | Notification message |
| is_read | Boolean | Read status |
| created_at | DateTime | Creation timestamp |

## 🎨 UI Features

### Responsive Design
- Mobile-friendly layout
- Tablet and desktop optimized
- Touch-friendly buttons and inputs

### Visual Feedback
- Smooth transitions and animations
- Loading states
- Success/error messages
- Real-time notification badges

### Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation support
- High contrast colors

## 🔧 Configuration

### Business Hours
Edit `services.py` to change business hours:
```python
BUSINESS_START = time(8, 0)   # 8:00 AM
BUSINESS_END = time(18, 0)    # 6:00 PM
LUNCH_START = time(12, 0)     # 12:00 PM
LUNCH_END = time(13, 0)       # 1:00 PM
```

### Session Duration
Edit `services.py` to change session duration:
```python
SESSION_DURATION = 120  # 2 hours in minutes
BREAK_DURATION = 15     # 15 minutes
```

### Database
Edit `database.py` to change database:
```python
DATABASE_URL = "sqlite+aiosqlite:///./appointments.db"
```

## 📝 Logging

The application includes comprehensive logging. Enable SQL query logging by setting `echo=True` in `database.py`:
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True to see SQL queries
    ...
)
```

## 🚨 Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify `main.py`:
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8001,  # Change port number
    reload=True,
)
```

### Database Errors
Delete `appointments.db` to reset the database:
```bash
rm appointments.db  # macOS/Linux
del appointments.db # Windows
```

### WebSocket Connection Issues
Ensure your firewall allows WebSocket connections on port 8000.

## 📚 Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sqlalchemy**: ORM
- **pydantic**: Data validation
- **aiosqlite**: Async SQLite driver
- **python-multipart**: Form data parsing
- **email-validator**: Email validation

## 🤝 Contributing

To extend the system:

1. **Add New Endpoints**: Edit `main.py`
2. **Add Business Logic**: Edit `services.py`
3. **Add Database Models**: Edit `models.py`
4. **Add Validation**: Edit `schemas.py`
5. **Update Frontend**: Edit `frontend/app.js`

## 📄 License

This project is provided as-is for appointment management purposes.

## 📞 Support

For issues or questions, review the code documentation and API endpoints above.

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production Ready
