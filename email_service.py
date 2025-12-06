"""
Email Service for EcoHarvest Farm Appointment System
Handles sending emails for password resets and appointment notifications
"""

import smtplib
import secrets
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Admin email (get from environment or use default)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "kennedynyambura5981@gmail.com")

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your-app-password")
SENDER_NAME = "EcoHarvest Farm"

# Debug: Print email configuration on startup
print(f"[DEBUG] Email Configuration Loaded:")
print(f"  SMTP_SERVER: {SMTP_SERVER}")
print(f"  SMTP_PORT: {SMTP_PORT}")
print(f"  SENDER_EMAIL: {SENDER_EMAIL}")
print(f"  ADMIN_EMAIL: {ADMIN_EMAIL}")
print(f"  SENDER_PASSWORD: {'*' * len(SENDER_PASSWORD) if SENDER_PASSWORD else 'NOT SET'}")
sys.stdout.flush()

# Store reset tokens in memory (in production, use database)
reset_tokens = {}


def generate_reset_token(email: str) -> str:
    """Generate a password reset token"""
    token = secrets.token_urlsafe(32)
    # Token expires in 24 hours
    reset_tokens[token] = {
        "email": email,
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    return token


def verify_reset_token(token: str) -> str:
    """Verify reset token and return email if valid"""
    if token not in reset_tokens:
        return None
    
    token_data = reset_tokens[token]
    if datetime.now() > token_data["expires_at"]:
        del reset_tokens[token]
        return None
    
    return token_data["email"]


def send_password_reset_email(email: str, reset_link: str) -> bool:
    """
    Send password reset email to client
    
    Args:
        email: Client email address
        reset_link: Password reset link
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[INFO] Attempting to send password reset email to {email}")
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = email
        msg['Subject'] = "🌾 Password Reset - EcoHarvest Farm"

        body = f"""
Dear Client,

We received a request to reset your password for your EcoHarvest Farm account.

Click the link below to reset your password (valid for 24 hours):
{reset_link}

If you didn't request this, please ignore this email.

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        print(f"[INFO] Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print(f"[INFO] Logging in as {SENDER_EMAIL}")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"[OK] Password reset email sent to {email}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send password reset email to {email}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def send_appointment_cancellation_email(
    client_email: str,
    client_name: str,
    appointment_time: datetime,
    cancellation_reason: str
) -> bool:
    """
    Send appointment cancellation email to client
    
    Args:
        client_email: Client email address
        client_name: Client name
        appointment_time: Original appointment time
        cancellation_reason: Reason for cancellation
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = client_email
        msg['Subject'] = "🌾 Appointment Cancellation - EcoHarvest Farm"

        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        
        body = f"""
Dear {client_name},

We regret to inform you that your consultation appointment has been cancelled.

Appointment Details:
📅 Date & Time: {formatted_time}
❌ Status: Cancelled

Reason for Cancellation:
{cancellation_reason}

Refund Policy:
✅ You will receive a full refund as per our terms and conditions.

Next Steps:
Please visit our website to book a new consultation at your convenience.
We look forward to serving you soon!

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"[OK] Cancellation email sent to {client_email}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send cancellation email: {str(e)}")
        return False


def send_admin_appointment_notification(
    client_name: str,
    client_email: str,
    client_phone: str,
    appointment_time: datetime,
    notes: str = None
) -> bool:
    """
    Send appointment notification email to admin
    
    Args:
        client_name: Client name
        client_email: Client email
        client_phone: Client phone
        appointment_time: Appointment time
        notes: Optional appointment notes
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[INFO] Attempting to send admin notification to {ADMIN_EMAIL}")
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"🌾 New Appointment Booking - {client_name}"

        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        notes_section = f"\nNotes:\n{notes}" if notes else ""
        
        body = f"""
Dear Admin,

A new appointment has been booked!

Client Details:
👤 Name: {client_name}
📧 Email: {client_email}
📱 Phone: {client_phone}

Appointment Details:
📅 Date & Time: {formatted_time}
⏱️ Duration: 1 Hour
✅ Status: Confirmed
{notes_section}

Action Required:
Please review the appointment details and prepare for the consultation.

Best regards,
EcoHarvest Farm System
🌾 Sustainable Farming Consultation Services
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        print(f"[INFO] Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print(f"[INFO] Logging in as {SENDER_EMAIL}")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"[OK] Admin notification sent for appointment with {client_name}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send admin notification to {ADMIN_EMAIL}: {str(e)}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False


def send_appointment_confirmation_email(
    client_email: str,
    client_name: str,
    appointment_time: datetime,
    notes: str = None
) -> bool:
    """
    Send appointment confirmation email to client
    
    Args:
        client_email: Client email address
        client_name: Client name
        appointment_time: Appointment time
        notes: Optional appointment notes
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[INFO] Attempting to send confirmation email to {client_email}")
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = client_email
        msg['Subject'] = "🌾 Appointment Confirmation - EcoHarvest Farm"

        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        
        notes_section = f"\nSpecial Requests/Notes:\n{notes}" if notes else ""
        
        body = f"""
Dear {client_name},

Thank you for booking a consultation with EcoHarvest Farm!

Appointment Details:
📅 Date & Time: {formatted_time}
⏱️ Duration: 1 Hour
✅ Status: Confirmed
{notes_section}

Important Information:
- Please arrive 5 minutes early
- If you need to reschedule, contact us at least 24 hours in advance
- 20% cancellation fee applies for client-initiated cancellations

We look forward to discussing your farming consultation needs!

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        print(f"[INFO] Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print(f"[INFO] Logging in as {SENDER_EMAIL}")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"[OK] Confirmation email sent to {client_email}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send confirmation email to {client_email}: {str(e)}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False
