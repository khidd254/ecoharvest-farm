"""
Email Service for EcoHarvest Farm Appointment System
Handles sending emails for password resets and appointment notifications using Resend
"""

import secrets
import sys
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Admin email (get from environment or use default)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "kennedynyambura5981@gmail.com")

# Email Configuration
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "onboarding@resend.dev")
SENDER_NAME = "EcoHarvest Farm"

# Initialize Resend client (lazy import)
resend_client = None

def _init_resend():
    """Initialize Resend client on first use"""
    global resend_client
    if resend_client is not None:
        return resend_client
    
    try:
        from resend import AsyncResend
        if RESEND_API_KEY:
            # For sync usage, we'll use the module-level functions
            import resend as resend_module
            resend_module.api_key = RESEND_API_KEY
            resend_client = resend_module  # Store the module itself
            print(f"[OK] Resend client initialized successfully")
            sys.stdout.flush()
        else:
            print(f"[WARNING] RESEND_API_KEY not set")
            sys.stdout.flush()
    except (ImportError, AttributeError) as e:
        print(f"[WARNING] Failed to initialize Resend: {str(e)}")
        sys.stdout.flush()
    
    return resend_client

# Debug: Print email configuration on startup
print(f"[DEBUG] Email Configuration Loaded:")
print(f"  SENDER_EMAIL: {SENDER_EMAIL}")
print(f"  ADMIN_EMAIL: {ADMIN_EMAIL}")
print(f"  RESEND_API_KEY: {'*' * 10 if RESEND_API_KEY else 'NOT SET'}")
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
        sys.stdout.flush()
        
        client = _init_resend()
        if not client:
            print(f"[WARNING] Resend client not available")
            sys.stdout.flush()
            return False
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
<h2>🌾 Password Reset - EcoHarvest Farm</h2>

<p>Dear Client,</p>

<p>We received a request to reset your password for your EcoHarvest Farm account.</p>

<p>Click the link below to reset your password (valid for 24 hours):</p>

<p><a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a></p>

<p>If you didn't request this, please ignore this email.</p>

<p>Best regards,<br>EcoHarvest Farm Team<br>🌾 Sustainable Farming Consultation Services</p>
</body>
</html>
        """
        
        print(f"[INFO] Sending password reset email via Resend to {email}")
        sys.stdout.flush()
        
        response = client.emails.send(
            from_=f"{SENDER_NAME} <{SENDER_EMAIL}>",
            to=email,
            subject="🌾 Password Reset - EcoHarvest Farm",
            html=html_body,
        )
        
        print(f"[OK] Password reset email sent to {email}")
        print(f"[INFO] Resend response: {response}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send password reset email to {email}: {str(e)}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
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
        print(f"[INFO] Attempting to send cancellation email to {client_email}")
        sys.stdout.flush()
        
        client = _init_resend()
        if not client:
            print(f"[WARNING] Resend client not available")
            sys.stdout.flush()
            return False
        
        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
<h2>🌾 Appointment Cancellation - EcoHarvest Farm</h2>

<p>Dear {client_name},</p>

<p>We regret to inform you that your consultation appointment has been cancelled.</p>

<h3>Appointment Details:</h3>
<ul>
<li><strong>Date & Time:</strong> {formatted_time}</li>
<li><strong>Status:</strong> ❌ Cancelled</li>
</ul>

<h3>Reason for Cancellation:</h3>
<p>{cancellation_reason}</p>

<h3>Refund Policy:</h3>
<p>✅ You will receive a full refund as per our terms and conditions.</p>

<h3>Next Steps:</h3>
<p>Please visit our website to book a new consultation at your convenience.<br>We look forward to serving you soon!</p>

<p>Best regards,<br>EcoHarvest Farm Team<br>🌾 Sustainable Farming Consultation Services</p>
</body>
</html>
        """
        
        print(f"[INFO] Sending cancellation email via Resend to {client_email}")
        sys.stdout.flush()
        
        response = client.emails.send(
            from_=f"{SENDER_NAME} <{SENDER_EMAIL}>",
            to=client_email,
            subject="🌾 Appointment Cancellation - EcoHarvest Farm",
            html=html_body,
        )
        
        print(f"[OK] Cancellation email sent to {client_email}")
        print(f"[INFO] Resend response: {response}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send cancellation email: {str(e)}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
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
        sys.stdout.flush()
        
        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        notes_section = f"\nNotes:\n{notes}" if notes else ""
        
        # Log the appointment details
        log_message = f"""
[APPOINTMENT NOTIFICATION]
Client: {client_name}
Email: {client_email}
Phone: {client_phone}
Date & Time: {formatted_time}
{notes_section}
"""
        print(log_message)
        sys.stdout.flush()
        
        client = _init_resend()
        if not client:
            print(f"[WARNING] Resend client not available")
            sys.stdout.flush()
            return False
        
        # Send email via Resend
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
<h2>🌾 New Appointment Booking - {client_name}</h2>

<p>A new appointment has been booked!</p>

<h3>Client Details:</h3>
<ul>
<li><strong>Name:</strong> {client_name}</li>
<li><strong>Email:</strong> {client_email}</li>
<li><strong>Phone:</strong> {client_phone}</li>
</ul>

<h3>Appointment Details:</h3>
<ul>
<li><strong>Date & Time:</strong> {formatted_time}</li>
<li><strong>Duration:</strong> 1 Hour</li>
<li><strong>Status:</strong> Confirmed</li>
{f'<li><strong>Notes:</strong> {notes}</li>' if notes else ''}
</ul>

<p><strong>Action Required:</strong> Please review the appointment details and prepare for the consultation.</p>

<p>Best regards,<br>EcoHarvest Farm System<br>🌾 Sustainable Farming Consultation Services</p>
</body>
</html>
"""
        
        print(f"[INFO] Sending email via Resend to {ADMIN_EMAIL}")
        sys.stdout.flush()
        
        response = client.emails.send(
            from_=f"{SENDER_NAME} <{SENDER_EMAIL}>",
            to=ADMIN_EMAIL,
            subject=f"🌾 New Appointment Booking - {client_name}",
            html=html_body,
        )
        
        print(f"[OK] Admin notification sent for appointment with {client_name}")
        print(f"[INFO] Resend response: {response}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send admin notification: {str(e)}")
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
        sys.stdout.flush()
        
        formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
        notes_section = f"<li><strong>Special Requests/Notes:</strong> {notes}</li>" if notes else ""
        
        # Log the confirmation details
        log_message = f"""
[APPOINTMENT CONFIRMATION]
Client: {client_name}
Email: {client_email}
Date & Time: {formatted_time}
"""
        print(log_message)
        sys.stdout.flush()
        
        client = _init_resend()
        if not client:
            print(f"[WARNING] Resend client not available")
            sys.stdout.flush()
            return False
        
        # Send email via Resend
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
<h2>🌾 Appointment Confirmation - EcoHarvest Farm</h2>

<p>Dear {client_name},</p>

<p>Thank you for booking a consultation with EcoHarvest Farm!</p>

<h3>Appointment Details:</h3>
<ul>
<li><strong>Date & Time:</strong> {formatted_time}</li>
<li><strong>Duration:</strong> 1 Hour</li>
<li><strong>Status:</strong> Confirmed</li>
{notes_section}
</ul>

<h3>Important Information:</h3>
<ul>
<li>Please arrive 5 minutes early</li>
<li>If you need to reschedule, contact us at least 24 hours in advance</li>
<li>20% cancellation fee applies for client-initiated cancellations</li>
</ul>

<p>We look forward to discussing your farming consultation needs!</p>

<p>Best regards,<br>EcoHarvest Farm Team<br>🌾 Sustainable Farming Consultation Services</p>
</body>
</html>
        """
        
        print(f"[INFO] Sending confirmation email via Resend to {client_email}")
        sys.stdout.flush()
        
        response = client.emails.send(
            from_=f"{SENDER_NAME} <{SENDER_EMAIL}>",
            to=client_email,
            subject="🌾 Appointment Confirmation - EcoHarvest Farm",
            html=html_body,
        )
        
        print(f"[OK] Confirmation email sent to {client_email}")
        print(f"[INFO] Resend response: {response}")
        sys.stdout.flush()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send confirmation email to {client_email}: {str(e)}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return False
