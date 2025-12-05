"""
Pydantic Schemas for Request/Response Validation

This module defines:
- Request schemas for incoming data validation
- Response schemas for API responses
- Data transformation and validation rules
"""

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List


class AppointmentCreate(BaseModel):
    """
    Schema for creating a new appointment.

    Attributes:
        client_name: Name of the client (required, 2-255 characters)
        client_email: Email address of the client (required, valid email)
        client_phone: Phone number of the client (optional)
        appointment_time: ISO format datetime string (required)
        notes: Additional notes about the appointment (optional)
    """

    client_name: str = Field(..., min_length=2, max_length=255)
    client_email: EmailStr
    client_phone: Optional[str] = None
    appointment_time: str = Field(
        ..., description="ISO format datetime string (e.g., 2024-01-15T10:00:00)"
    )
    notes: Optional[str] = None

    @validator("appointment_time")
    def validate_appointment_time(cls, v):
        """Validate that appointment time is in the future."""
        try:
            apt_time = datetime.fromisoformat(v)
            if apt_time < datetime.now():
                raise ValueError("Appointment time must be in the future")
            return v
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid datetime format: {str(e)}")

    class Config:
        schema_extra = {
            "example": {
                "client_name": "John Doe",
                "client_email": "john@example.com",
                "client_phone": "+1234567890",
                "appointment_time": "2024-01-15T10:00:00",
                "notes": "First time client",
            }
        }


class AppointmentResponse(BaseModel):
    """
    Schema for appointment response data.

    Attributes:
        id: Appointment ID
        client_name: Name of the client
        client_email: Email of the client
        client_phone: Phone number of the client
        appointment_time: Appointment datetime
        duration_minutes: Duration in minutes
        status: Appointment status
        notes: Additional notes
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int
    client_name: str
    client_email: str
    client_phone: Optional[str]
    appointment_time: datetime
    duration_minutes: int
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AvailableSlotResponse(BaseModel):
    """
    Schema for available appointment slots.

    Attributes:
        time: Start time of the available slot (ISO format)
        end_time: End time of the available slot (ISO format)
        is_available: Whether the slot is available
    """

    time: str
    end_time: str
    is_available: bool

    class Config:
        schema_extra = {
            "example": {
                "time": "2024-01-15T10:00:00",
                "end_time": "2024-01-15T12:00:00",
                "is_available": True,
            }
        }


class NotificationResponse(BaseModel):
    """
    Schema for notification response data.

    Attributes:
        id: Notification ID
        appointment_id: Associated appointment ID
        notification_type: Type of notification
        message: Notification message
        is_read: Whether the notification has been read
        created_at: Creation timestamp
    """

    id: int
    appointment_id: Optional[int]
    notification_type: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OwnerResponse(BaseModel):
    """
    Schema for owner response data.

    Attributes:
        id: Owner ID
        name: Owner's name
        email: Owner's email
        phone: Owner's phone
        business_hours_start: Business start time
        business_hours_end: Business end time
    """

    id: int
    name: str
    email: str
    phone: Optional[str]
    business_hours_start: str
    business_hours_end: str

    class Config:
        from_attributes = True


class CalendarEventResponse(BaseModel):
    """
    Schema for calendar event data.

    Attributes:
        id: Event ID
        title: Event title
        start: Start datetime
        end: End datetime
        client_name: Client name
        client_email: Client email
        client_phone: Client phone number
        notes: Appointment notes
        status: Event status
    """

    id: int
    title: str
    start: datetime
    end: datetime
    client_name: str
    client_email: str
    client_phone: Optional[str] = None
    notes: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    """Schema for user response."""
    name: Optional[str] = None
    email: str


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    message: str
    user: UserResponse
