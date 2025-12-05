# Email Integration Setup Guide

## Overview
The EcoHarvest Farm appointment system includes email functionality for:
- ✅ Appointment cancellation notifications
- ✅ Password reset emails
- ✅ Appointment confirmations

## Email Service Architecture

### Files
- `email_service.py` - Core email service with functions for sending emails
- `.env` - Email configuration (create from `.env.example`)

### Email Functions

#### 1. Appointment Cancellation Email
```python
send_appointment_cancellation_email(
    client_email: str,
    client_name: str,
    appointment_time: datetime,
    cancellation_reason: str
) -> bool
```
**Triggered when:** Admin cancels an appointment
**Recipient:** Client
**Content:** Appointment details, cancellation reason, refund policy

#### 2. Password Reset Email
```python
send_password_reset_email(
    email: str,
    reset_link: str
) -> bool
```
**Triggered when:** Client requests password reset
**Recipient:** Client
**Content:** Password reset link (valid for 24 hours)

#### 3. Appointment Confirmation Email
```python
send_appointment_confirmation_email(
    client_email: str,
    client_name: str,
    appointment_time: datetime,
    notes: str = None
) -> bool
```
**Triggered when:** Client books an appointment
**Recipient:** Client
**Content:** Appointment details, duration, special requests

---

## Setup Instructions

### Step 1: Create `.env` File

Copy `.env.example` to `.env` and fill in your email credentials:

```bash
cp .env.example .env
```

### Step 2: Configure Gmail (Recommended)

#### Option A: Using Gmail App Password (Recommended)

1. **Enable 2-Factor Authentication:**
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password
   - Copy this password

3. **Update `.env` File:**
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=xxxx xxxx xxxx xxxx
   ```

#### Option B: Using Regular Gmail Password

If you don't want to use App Passwords:

1. **Enable "Less secure app access":**
   - Go to https://myaccount.google.com/lesssecureapps
   - Turn ON "Allow less secure apps"

2. **Update `.env` File:**
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-gmail-password
   ```

### Step 3: Test Email Configuration

Run this Python script to test your email setup:

```python
from email_service import send_password_reset_email

# Test sending an email
success = send_password_reset_email(
    email="test@example.com",
    reset_link="http://localhost:8000/reset-password?token=test123"
)

if success:
    print("Email sent successfully!")
else:
    print("Failed to send email")
```

### Step 4: Restart the Server

```bash
python -m uvicorn main:app --reload
```

---

## API Endpoints for Email Features

### 1. Forgot Password
**Endpoint:** `POST /api/auth/forgot-password`

**Request:**
```json
{
    "email": "client@example.com"
}
```

**Response:**
```json
{
    "message": "Password reset link sent to your email",
    "email": "client@example.com"
}
```

### 2. Reset Password
**Endpoint:** `POST /api/auth/reset-password`

**Request:**
```json
{
    "token": "reset-token-from-email",
    "new_password": "new-password-123"
}
```

**Response:**
```json
{
    "message": "Password reset successfully",
    "email": "client@example.com"
}
```

### 3. Cancel Appointment (Sends Email)
**Endpoint:** `PUT /api/appointments/{appointment_id}/cancel`

**Request:**
```json
{
    "cancellation_reason": "Consultant is unavailable",
    "client_email": "client@example.com",
    "client_name": "John Doe"
}
```

**Response:**
```json
{
    "message": "Appointment cancelled successfully"
}
```

---

## Email Templates

### Appointment Cancellation Email
```
Subject: 🌾 Appointment Cancellation - EcoHarvest Farm

Dear [Client Name],

We regret to inform you that your consultation appointment has been cancelled.

Appointment Details:
📅 Date & Time: [Appointment Date and Time]
❌ Status: Cancelled

Reason for Cancellation:
[Cancellation Reason]

Refund Policy:
✅ You will receive a full refund as per our terms and conditions.

Next Steps:
Please visit our website to book a new consultation at your convenience.
We look forward to serving you soon!

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
```

### Password Reset Email
```
Subject: 🌾 Password Reset - EcoHarvest Farm

Dear Client,

We received a request to reset your password for your EcoHarvest Farm account.

Click the link below to reset your password (valid for 24 hours):
[Reset Link]

If you didn't request this, please ignore this email.

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
```

### Appointment Confirmation Email
```
Subject: 🌾 Appointment Confirmation - EcoHarvest Farm

Dear [Client Name],

Thank you for booking a consultation with EcoHarvest Farm!

Appointment Details:
📅 Date & Time: [Appointment Date and Time]
⏱️ Duration: 1 Hour
✅ Status: Confirmed
[Optional: Special Requests/Notes]

Important Information:
- Please arrive 5 minutes early
- If you need to reschedule, contact us at least 24 hours in advance
- 20% cancellation fee applies for client-initiated cancellations

We look forward to discussing your farming consultation needs!

Best regards,
EcoHarvest Farm Team
🌾 Sustainable Farming Consultation Services
```

---

## Troubleshooting

### Email Not Sending?

1. **Check `.env` file exists** in the project root
2. **Verify credentials** are correct in `.env`
3. **Check Gmail settings:**
   - 2FA enabled (if using App Password)
   - App Password generated correctly
   - Less secure apps enabled (if not using App Password)
4. **Check logs** - Look for error messages in console
5. **Test connection:**
   ```python
   import smtplib
   try:
       server = smtplib.SMTP("smtp.gmail.com", 587)
       server.starttls()
       server.login("your-email@gmail.com", "your-password")
       print("Connection successful!")
       server.quit()
   except Exception as e:
       print(f"Error: {e}")
   ```

### Common Errors

| Error | Solution |
|-------|----------|
| `SMTPAuthenticationError` | Check email/password in `.env` |
| `SMTPNotSupportedError` | Enable "Less secure apps" or use App Password |
| `ConnectionRefusedError` | Check SMTP_SERVER and SMTP_PORT in `.env` |
| `FileNotFoundError` | Create `.env` file from `.env.example` |

---

## Production Deployment

For production, consider:

1. **Use environment variables** instead of `.env` file
2. **Use a professional email service:**
   - SendGrid
   - Mailgun
   - AWS SES
   - Postmark

3. **Update `email_service.py`** to use your chosen service
4. **Add email templates** to database for easy management
5. **Implement email queue** for better performance
6. **Add email logging** for audit trail

---

## Security Best Practices

✅ **DO:**
- Use App Passwords for Gmail
- Store credentials in `.env` (never commit to git)
- Use HTTPS for password reset links
- Validate email addresses before sending
- Implement rate limiting on password reset

❌ **DON'T:**
- Commit `.env` file to version control
- Use plain text passwords in code
- Send sensitive data in email body
- Allow unlimited password reset requests
- Use personal email for business

---

## Support

For issues or questions about email setup, check:
- Gmail Help: https://support.google.com/mail
- Python SMTP Docs: https://docs.python.org/3/library/smtplib.html
- Project Issues: Check GitHub issues

