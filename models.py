"""
SQLAlchemy Database Models

This module defines the data models for:
- Appointments
- Owners
- Notifications

All models use SQLAlchemy ORM for database operations.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """
    User model for client accounts.

    Attributes:
        id: Unique identifier
        name: User's full name
        email: User's email address (unique)
        password_hash: Hashed password
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class Owner(Base):
    """
    Owner model representing the service provider.

    Attributes:
        id: Unique identifier
        name: Owner's name
        email: Owner's email address
        phone: Owner's phone number
        business_hours_start: Business start time (default: 8:00 AM)
        business_hours_end: Business end time (default: 6:00 PM)
        created_at: Timestamp when owner was created
    """

    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    business_hours_start = Column(String(5), default="08:00")  # HH:MM format
    business_hours_end = Column(String(5), default="18:00")  # HH:MM format
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")

    def __repr__(self):
        return f"<Owner(id={self.id}, name={self.name}, email={self.email})>"


class Appointment(Base):
    """
    Appointment model representing a booked appointment.

    Attributes:
        id: Unique identifier
        owner_id: Foreign key to Owner
        client_name: Name of the client booking the appointment
        client_email: Email of the client
        client_phone: Phone number of the client
        appointment_time: Date and time of the appointment
        duration_minutes: Duration of the appointment (default: 120 minutes = 2 hours)
        status: Appointment status (confirmed, cancelled, completed)
        notes: Additional notes about the appointment
        created_at: Timestamp when appointment was created
        updated_at: Timestamp when appointment was last updated
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), default=1)
    client_name = Column(String(255), nullable=False, index=True)
    client_email = Column(String(255), nullable=False)
    client_phone = Column(String(20))
    appointment_time = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=120)  # 2 hours
    status = Column(String(50), default="confirmed")  # confirmed, cancelled, completed
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("Owner", back_populates="appointments")
    notifications = relationship("Notification", back_populates="appointment")

    def __repr__(self):
        return f"<Appointment(id={self.id}, client={self.client_name}, time={self.appointment_time})>"

    @property
    def end_time(self):
        """Calculate appointment end time based on duration."""
        from datetime import timedelta

        return self.appointment_time + timedelta(minutes=self.duration_minutes)


class Notification(Base):
    """
    Notification model for tracking system notifications.

    Attributes:
        id: Unique identifier
        owner_id: Foreign key to Owner
        appointment_id: Foreign key to Appointment
        notification_type: Type of notification (new_appointment, cancellation, reminder)
        message: Notification message
        is_read: Whether the notification has been read
        created_at: Timestamp when notification was created
    """

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), default=1)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    notification_type = Column(String(50), nullable=False)  # new_appointment, cancellation, reminder
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    owner = relationship("Owner", back_populates="notifications")
    appointment = relationship("Appointment", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.notification_type}, read={self.is_read})>"
