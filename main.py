"""
Appointment Booking System - FastAPI Backend
A comprehensive system for managing appointments with real-time notifications
and calendar management capabilities.

Author: Appointment System
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from email_service import (
    send_password_reset_email,
    send_appointment_cancellation_email,
    send_appointment_confirmation_email,
    send_admin_appointment_notification,
    generate_reset_token,
    verify_reset_token,
)
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import json
import asyncio
import os
from typing import List, Optional
from passlib.context import CryptContext
from sqlalchemy import select
from concurrent.futures import ThreadPoolExecutor

from database import init_db, get_db, SessionLocal
from models import Appointment, Owner, Notification, User
from schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AvailableSlotResponse,
    NotificationResponse,
    OwnerResponse,
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthResponse,
    UserResponse,
)
from services import (
    AppointmentService,
    AvailabilityService,
    NotificationService,
)

# ============================================================================
# LIFESPAN EVENT HANDLER
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    Initializes database on startup.
    """
    # Startup
    await init_db()
    print("[OK] Database initialized successfully")
    yield
    # Shutdown
    print("[OK] Application shutting down")


# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Appointment Booking System",
    description="A professional appointment booking system with real-time notifications",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

# Initialize services
appointment_service = AppointmentService()
availability_service = AvailabilityService()
notification_service = NotificationService()

# Thread pool for sending emails asynchronously
email_executor = ThreadPoolExecutor(max_workers=2)

# Store active WebSocket connections for real-time notifications
active_connections: List[WebSocket] = []


# ============================================================================
# EMAIL HELPER FUNCTIONS
# ============================================================================

def send_admin_email_wrapper(client_name: str, client_email: str, client_phone: str, appointment_time: datetime, notes: str = None):
    """Wrapper function for sending admin notification email"""
    try:
        send_admin_appointment_notification(
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            appointment_time=appointment_time,
            notes=notes
        )
    except Exception as e:
        print(f"[ERROR] Failed to send admin email in background: {str(e)}")


def send_client_email_wrapper(client_email: str, client_name: str, appointment_time: datetime, notes: str = None):
    """Wrapper function for sending client confirmation email"""
    try:
        send_appointment_confirmation_email(
            client_email=client_email,
            client_name=client_name,
            appointment_time=appointment_time,
            notes=notes
        )
    except Exception as e:
        print(f"[ERROR] Failed to send client email in background: {str(e)}")


# ============================================================================
# WEBSOCKET ENDPOINT - Real-time Notifications
# ============================================================================


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time notifications.
    Clients connect here to receive live updates about new appointments.
    """
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except Exception as e:
        active_connections.remove(websocket)


async def broadcast_notification(message: dict):
    """
    Broadcasts a notification to all connected WebSocket clients.

    Args:
        message: Dictionary containing notification data
    """
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)

    for connection in disconnected:
        active_connections.remove(connection)


# ============================================================================
# APPOINTMENT ENDPOINTS
# ============================================================================


@app.post("/api/appointments", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    appointment_data: AppointmentCreate, db=Depends(get_db)
):
    """
    Create a new appointment booking.

    This endpoint:
    - Validates the appointment time slot
    - Checks for conflicts with existing appointments
    - Creates the appointment in the database
    - Sends real-time notification to the owner
    - Records the booking in the system

    Args:
        appointment_data: Appointment details (client name, email, date, time)
        db: Database session

    Returns:
        AppointmentResponse: Created appointment details

    Raises:
        HTTPException: If time slot is invalid or already booked
    """
    # Validate appointment time
    appointment_time = datetime.fromisoformat(appointment_data.appointment_time)

    # Check if slot is available
    is_available = await availability_service.check_availability(
        appointment_time, db
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time slot is already booked. Please select another time.",
        )

    # Create appointment
    appointment = await appointment_service.create_appointment(
        appointment_data, db
    )

    # Send notification to owner
    notification_data = {
        "type": "new_appointment",
        "title": "New Appointment Booking",
        "message": f"New appointment from {appointment.client_name} on {appointment_time.strftime('%Y-%m-%d %H:%M')}",
        "appointment_id": appointment.id,
        "client_name": appointment.client_name,
        "client_email": appointment.client_email,
        "appointment_time": appointment.appointment_time.isoformat(),
    }
    await broadcast_notification(notification_data)

    # Save notification to database
    await notification_service.create_notification(
        appointment_id=appointment.id,
        notification_type="new_appointment",
        message=notification_data["message"],
        db=db,
    )

    # Send emails asynchronously (non-blocking)
    loop = asyncio.get_event_loop()
    
    # Send admin notification email
    loop.run_in_executor(
        email_executor,
        send_admin_email_wrapper,
        appointment.client_name,
        appointment.client_email,
        appointment.client_phone or "Not provided",
        appointment.appointment_time,
        appointment.notes
    )
    
    # Send client confirmation email
    loop.run_in_executor(
        email_executor,
        send_client_email_wrapper,
        appointment.client_email,
        appointment.client_name,
        appointment.appointment_time,
        appointment.notes
    )

    return AppointmentResponse.from_orm(appointment)


@app.get("/api/appointments", response_model=List[AppointmentResponse])
async def list_appointments(email: str = None, db=Depends(get_db)):
    """
    Retrieve appointments.
    
    If email is provided, returns only appointments for that client.
    If no email is provided, returns all appointments (for admin).

    Args:
        email: Optional client email to filter appointments
        db: Database session

    Returns:
        List[AppointmentResponse]: List of appointments
    """
    try:
        if email:
            # Filter appointments by client email
            result = await db.execute(
                select(Appointment).where(Appointment.client_email == email).order_by(Appointment.appointment_time)
            )
            appointments = result.scalars().all()
        else:
            # Get all appointments (for admin)
            appointments = await appointment_service.get_all_appointments(db)
        
        return [AppointmentResponse.from_orm(apt) for apt in appointments]
    except Exception as e:
        print(f"[ERROR] Failed to fetch appointments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch appointments: {str(e)}"
        )


@app.get("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db=Depends(get_db)):
    """
    Retrieve a specific appointment by ID.

    Args:
        appointment_id: ID of the appointment to retrieve
        db: Database session

    Returns:
        AppointmentResponse: Appointment details

    Raises:
        HTTPException: If appointment not found
    """
    appointment = await appointment_service.get_appointment(appointment_id, db)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    return AppointmentResponse.from_orm(appointment)


@app.delete("/api/appointments/{appointment_id}", status_code=204)
async def delete_appointment(appointment_id: int, db=Depends(get_db)):
    """
    Cancel an appointment.

    Args:
        appointment_id: ID of the appointment to cancel
        db: Database session

    Raises:
        HTTPException: If appointment not found
    """
    success = await appointment_service.delete_appointment(appointment_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )


@app.put("/api/appointments/{appointment_id}/cancel")
async def cancel_appointment_with_email(
    appointment_id: int,
    cancellation_data: dict,
    db=Depends(get_db)
):
    """
    Cancel an appointment and send email to client.

    Args:
        appointment_id: ID of the appointment to cancel
        cancellation_data: Contains cancellation_reason, client_email, client_name
        db: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If appointment not found
    """
    # Get the appointment
    appointment = await appointment_service.get_appointment(appointment_id, db)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )

    # Cancel the appointment
    success = await appointment_service.delete_appointment(appointment_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Failed to cancel appointment"
        )

    # Send email to client
    send_appointment_cancellation_email(
        client_email=cancellation_data.get('client_email', ''),
        client_name=cancellation_data.get('client_name', 'Client'),
        appointment_time=appointment.appointment_time,
        cancellation_reason=cancellation_data.get('cancellation_reason', 'No reason provided')
    )

    return {"message": "Appointment cancelled successfully"}


# ============================================================================
# AVAILABILITY ENDPOINTS
# ============================================================================


@app.get("/api/available-slots", response_model=List[AvailableSlotResponse])
async def get_available_slots(
    date: str, db=Depends(get_db)
):
    """
    Get available appointment slots for a specific date.

    Business Hours:
    - Start: 8:00 AM
    - End: 6:00 PM
    - Session Duration: 1 hour
    - Break Duration: 10 minutes
    - Lunch Break: 1 hour (typically 12:00 PM - 1:00 PM)

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        List[AvailableSlotResponse]: List of available time slots

    Raises:
        HTTPException: If date format is invalid
    """
    try:
        slot_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD",
        )

    available_slots = await availability_service.get_available_slots(
        slot_date, db
    )
    return available_slots


@app.get("/api/calendar", response_model=dict)
async def get_calendar(db=Depends(get_db)):
    """
    Get the complete calendar view with all appointments.

    Returns:
        dict: Calendar data with appointments grouped by date
    """
    try:
        calendar_data = await appointment_service.get_calendar_view(db)
        return calendar_data
    except Exception as e:
        print(f"[ERROR] Failed to fetch calendar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch calendar: {str(e)}"
        )


@app.get("/api/notifications", response_model=List[NotificationResponse])
async def get_notifications(db=Depends(get_db)):
    """
    Retrieve all notifications.

    Returns:
        List[NotificationResponse]: List of all notifications
    """
    try:
        notifications = await notification_service.get_all_notifications(db)
        return [NotificationResponse.from_orm(notif) for notif in notifications]
    except Exception as e:
        print(f"[ERROR] Failed to fetch notifications: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notifications: {str(e)}"
        )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================


@app.post("/api/auth/register", response_model=AuthResponse)
async def register(data: RegisterRequest, db=Depends(get_db)):
    """Register a new client account."""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(data.password)
    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    
    return AuthResponse(
        message="Account created successfully",
        user=UserResponse(name=new_user.name, email=new_user.email)
    )


@app.post("/api/auth/login", response_model=AuthResponse)
async def login(data: LoginRequest, db=Depends(get_db)):
    """Login a client account."""
    # Find user by email
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return AuthResponse(
        message="Logged in successfully",
        user=UserResponse(name=user.name, email=user.email)
    )


@app.post("/api/auth/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db=Depends(get_db)):
    """Handle forgot password request and send reset email."""
    token = generate_reset_token(data.email)
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    success = send_password_reset_email(data.email, reset_link)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send reset email")
    
    return {"message": "Password reset link sent to your email", "email": data.email}


@app.post("/api/auth/reset-password")
async def reset_password(data: ResetPasswordRequest, db=Depends(get_db)):
    """Reset password with token."""
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired reset token")
    
    return {"message": "Password reset successfully", "email": email}


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring system status.

    Returns:
        dict: System status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EcoHarvest Farm Appointment Booking System",
    }


# ============================================================================
# STATIC FILES & ROOT ENDPOINT
# ============================================================================


@app.get("/")
async def root():
    """
    Serve the frontend index.html file.
    """
    return FileResponse("frontend/index.html")


# Mount static files (CSS, JS, images, etc.) - MUST be after routes
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
