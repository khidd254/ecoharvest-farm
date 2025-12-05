"""
Business Logic Services

This module contains the core business logic for:
- Appointment management
- Availability checking
- Notification handling
- Calendar operations

Services are decoupled from FastAPI routes for better testability and reusability.
"""

from datetime import datetime, timedelta, time, date
from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import Appointment, Owner, Notification
from schemas import AvailableSlotResponse, CalendarEventResponse


class AppointmentService:
    """
    Service for managing appointments.

    Handles:
    - Creating appointments
    - Retrieving appointments
    - Deleting appointments
    - Calendar views
    """

    async def create_appointment(
        self, appointment_data, db: AsyncSession
    ) -> Appointment:
        """
        Create a new appointment in the database.

        Args:
            appointment_data: AppointmentCreate schema
            db: Database session

        Returns:
            Appointment: Created appointment object
        """
        appointment_time = datetime.fromisoformat(appointment_data.appointment_time)

        appointment = Appointment(
            owner_id=1,  # Default owner
            client_name=appointment_data.client_name,
            client_email=appointment_data.client_email,
            client_phone=appointment_data.client_phone,
            appointment_time=appointment_time,
            duration_minutes=120,  # 2 hours
            status="confirmed",
            notes=appointment_data.notes,
        )

        db.add(appointment)
        await db.flush()
        await db.refresh(appointment)
        return appointment

    async def get_all_appointments(self, db: AsyncSession) -> List[Appointment]:
        """
        Retrieve all appointments from the database.

        Args:
            db: Database session

        Returns:
            List[Appointment]: List of all appointments
        """
        result = await db.execute(
            select(Appointment).order_by(Appointment.appointment_time)
        )
        return result.scalars().all()

    async def get_appointment(
        self, appointment_id: int, db: AsyncSession
    ) -> Optional[Appointment]:
        """
        Retrieve a specific appointment by ID.

        Args:
            appointment_id: ID of the appointment
            db: Database session

        Returns:
            Optional[Appointment]: Appointment object or None if not found
        """
        result = await db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def delete_appointment(
        self, appointment_id: int, db: AsyncSession
    ) -> bool:
        """
        Delete (cancel) an appointment.

        Args:
            appointment_id: ID of the appointment to delete
            db: Database session

        Returns:
            bool: True if deleted successfully, False if not found
        """
        appointment = await self.get_appointment(appointment_id, db)
        if not appointment:
            return False

        appointment.status = "cancelled"
        await db.flush()
        return True

    async def get_calendar_view(self, db: AsyncSession) -> dict:
        """
        Get calendar view with all appointments grouped by date.

        Args:
            db: Database session

        Returns:
            dict: Calendar data with appointments grouped by date
        """
        appointments = await self.get_all_appointments(db)

        calendar = {}
        for apt in appointments:
            date_key = apt.appointment_time.date().isoformat()
            if date_key not in calendar:
                calendar[date_key] = []

            calendar[date_key].append(
                {
                    "id": apt.id,
                    "client_name": apt.client_name,
                    "client_email": apt.client_email,
                    "client_phone": apt.client_phone,
                    "notes": apt.notes,
                    "start_time": apt.appointment_time.isoformat(),
                    "end_time": apt.end_time.isoformat(),
                    "status": apt.status,
                }
            )

        return calendar


class AvailabilityService:
    """
    Service for checking and managing appointment availability.

    Handles:
    - Checking slot availability
    - Generating available slots
    - Conflict detection
    """

    # Business hours configuration
    BUSINESS_START = time(8, 0)  # 8:00 AM
    BUSINESS_END = time(18, 0)  # 6:00 PM
    SESSION_DURATION = 60  # 1 hour in minutes
    BREAK_DURATION = 10  # 10 minutes
    LUNCH_START = time(12, 30)  # 12:30 PM
    LUNCH_END = time(14, 0)  # 2:00 PM

    async def check_availability(
        self, appointment_time: datetime, db: AsyncSession
    ) -> bool:
        """
        Check if a specific time slot is available.

        Validates:
        - Time is within business hours
        - Time is not during lunch break
        - No conflicting appointments exist
        - Time slot is at least SESSION_DURATION long

        Args:
            appointment_time: Requested appointment datetime
            db: Database session

        Returns:
            bool: True if slot is available, False otherwise
        """
        # Check business hours
        if not self._is_within_business_hours(appointment_time):
            return False

        # Check lunch break
        if self._is_lunch_break(appointment_time):
            return False

        # Check for conflicting appointments
        end_time = appointment_time + timedelta(minutes=self.SESSION_DURATION)
        
        # Get all non-cancelled appointments
        result = await db.execute(
            select(Appointment).where(
                Appointment.status != "cancelled"
            )
        )
        appointments = result.scalars().all()
        
        # Check if any appointment conflicts with the requested time
        for apt in appointments:
            # Only check appointments on the same date
            if apt.appointment_time.date() != appointment_time.date():
                continue
                
            apt_end = apt.appointment_time + timedelta(minutes=apt.duration_minutes)
            # Check if there's an overlap
            if apt.appointment_time < end_time and apt_end > appointment_time:
                return False
        
        return True

    async def get_available_slots(
        self, slot_date: datetime.date, db: AsyncSession
    ) -> List[AvailableSlotResponse]:
        """
        Generate list of available appointment slots for a given date.

        Generates slots considering:
        - Business hours (8 AM - 6 PM)
        - Session duration (1 hour)
        - Break duration (10 minutes between sessions)
        - Lunch break (12 PM - 1 PM)
        - Existing appointments

        Args:
            slot_date: Date to get available slots for
            db: Database session

        Returns:
            List[AvailableSlotResponse]: List of available time slots
        """
        available_slots = []

        # Start from business hours start
        current_time = datetime.combine(slot_date, self.BUSINESS_START)
        business_end = datetime.combine(slot_date, self.BUSINESS_END)

        while current_time + timedelta(minutes=self.SESSION_DURATION) <= business_end:
            # Skip lunch break
            if self._is_lunch_break(current_time):
                # Move to after lunch
                current_time = datetime.combine(slot_date, self.LUNCH_END)
                # Check if we're still within business hours after lunch
                if current_time + timedelta(minutes=self.SESSION_DURATION) > business_end:
                    break
                continue

            # Check if slot is available
            is_available = await self.check_availability(current_time, db)

            slot_end = current_time + timedelta(minutes=self.SESSION_DURATION)

            available_slots.append(
                AvailableSlotResponse(
                    time=current_time.isoformat(),
                    end_time=slot_end.isoformat(),
                    is_available=is_available,
                )
            )

            # Move to next slot (session + break)
            current_time = slot_end + timedelta(minutes=self.BREAK_DURATION)

        return available_slots

    def _is_within_business_hours(self, appointment_time: datetime) -> bool:
        """
        Check if appointment time is within business hours.

        Args:
            appointment_time: Appointment datetime to check

        Returns:
            bool: True if within business hours
        """
        apt_time = appointment_time.time()
        end_time = (
            appointment_time + timedelta(minutes=self.SESSION_DURATION)
        ).time()

        # Check if appointment starts and ends within business hours
        return (
            apt_time >= self.BUSINESS_START
            and end_time <= self.BUSINESS_END
        )

    def _is_lunch_break(self, appointment_time: datetime) -> bool:
        """
        Check if appointment time conflicts with lunch break.

        Args:
            appointment_time: Appointment datetime to check

        Returns:
            bool: True if during lunch break
        """
        apt_time = appointment_time.time()
        end_time = (
            appointment_time + timedelta(minutes=self.SESSION_DURATION)
        ).time()

        # Check if appointment overlaps with lunch break
        lunch_start = self.LUNCH_START
        lunch_end = self.LUNCH_END

        return not (end_time <= lunch_start or apt_time >= lunch_end)


class NotificationService:
    """
    Service for managing notifications.

    Handles:
    - Creating notifications
    - Retrieving notifications
    - Marking notifications as read
    """

    async def create_notification(
        self,
        appointment_id: int,
        notification_type: str,
        message: str,
        db: AsyncSession,
    ) -> Notification:
        """
        Create a new notification.

        Args:
            appointment_id: Associated appointment ID
            notification_type: Type of notification
            message: Notification message
            db: Database session

        Returns:
            Notification: Created notification object
        """
        notification = Notification(
            owner_id=1,  # Default owner
            appointment_id=appointment_id,
            notification_type=notification_type,
            message=message,
            is_read=False,
        )

        db.add(notification)
        await db.flush()
        await db.refresh(notification)
        return notification

    async def get_all_notifications(self, db: AsyncSession) -> List[Notification]:
        """
        Retrieve all notifications.

        Args:
            db: Database session

        Returns:
            List[Notification]: List of all notifications
        """
        result = await db.execute(
            select(Notification).order_by(Notification.created_at.desc())
        )
        return result.scalars().all()

    async def get_unread_notifications(self, db: AsyncSession) -> List[Notification]:
        """
        Retrieve unread notifications only.

        Args:
            db: Database session

        Returns:
            List[Notification]: List of unread notifications
        """
        result = await db.execute(
            select(Notification)
            .where(Notification.is_read == False)
            .order_by(Notification.created_at.desc())
        )
        return result.scalars().all()

    async def mark_as_read(
        self, notification_id: int, db: AsyncSession
    ) -> bool:
        """
        Mark a notification as read.

        Args:
            notification_id: ID of the notification
            db: Database session

        Returns:
            bool: True if marked successfully, False if not found
        """
        result = await db.execute(
            select(Notification).where(Notification.id == notification_id)
        )
        notification = result.scalar_one_or_none()

        if not notification:
            return False

        notification.is_read = True
        await db.flush()
        return True
