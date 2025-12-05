# Testing Guide - Appointment Booking System

Comprehensive guide for testing the Appointment Booking System.

## 🧪 Manual Testing

### Test 1: Book an Appointment

**Steps:**
1. Navigate to http://localhost:8000
2. Fill in the booking form:
   - Full Name: `John Doe`
   - Email: `john@example.com`
   - Phone: `+1234567890`
   - Date: Select tomorrow's date
   - Time: Select 8:00 AM
   - Notes: `First appointment`
3. Click "Book Appointment"

**Expected Result:**
- ✅ Success message appears
- ✅ Notification appears in bell icon
- ✅ Appointment appears in calendar

---

### Test 2: Conflict Detection

**Steps:**
1. Book an appointment at 8:00 AM on a specific date
2. Try to book another appointment at 8:00 AM on the same date
3. Try to book at 9:00 AM (should fail - overlaps with 2-hour session)

**Expected Result:**
- ✅ First appointment succeeds
- ✅ Second appointment fails with error: "This time slot is already booked"
- ✅ Third appointment fails with error: "This time slot is already booked"

---

### Test 3: Lunch Break Validation

**Steps:**
1. Try to book an appointment at 12:00 PM (noon)
2. Try to book an appointment at 12:30 PM
3. Try to book an appointment at 11:00 AM (should work - ends before lunch)

**Expected Result:**
- ✅ 12:00 PM booking fails
- ✅ 12:30 PM booking fails
- ✅ 11:00 AM booking succeeds (ends at 1:00 PM, but lunch is 12-1 PM, so this should fail)
- ✅ 10:00 AM booking succeeds (ends at 12:00 PM, before lunch)

---

### Test 4: Business Hours Validation

**Steps:**
1. Try to book at 7:00 AM (before business hours)
2. Try to book at 5:00 PM (should work - ends at 7:00 PM, which is after hours)
3. Try to book at 4:00 PM (should work - ends at 6:00 PM, exactly at closing)

**Expected Result:**
- ✅ 7:00 AM booking fails
- ✅ 5:00 PM booking fails (would end after 6:00 PM)
- ✅ 4:00 PM booking succeeds

---

### Test 5: Calendar View

**Steps:**
1. Book multiple appointments on different dates
2. Click "View Calendar" tab
3. Verify all appointments are displayed

**Expected Result:**
- ✅ All appointments appear grouped by date
- ✅ Client names and times are correct
- ✅ Status shows "confirmed"

---

### Test 6: Real-time Notifications

**Steps:**
1. Open the application in two browser windows
2. In window 1, click the notification bell
3. In window 2, book an appointment
4. Check window 1 for notification

**Expected Result:**
- ✅ Notification appears immediately in window 1
- ✅ Notification shows appointment details
- ✅ Notification badge shows unread count

---

### Test 7: Form Validation

**Steps:**
1. Try to submit form without name
2. Try to submit form with invalid email
3. Try to submit form without selecting time
4. Try to book in the past

**Expected Result:**
- ✅ Name field shows error (required)
- ✅ Email field shows error (invalid format)
- ✅ Time selection shows error (required)
- ✅ Past date cannot be selected

---

## 🔌 API Testing

### Test 1: Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00",
  "service": "Appointment Booking System"
}
```

---

### Test 2: Get Available Slots

```bash
curl "http://localhost:8000/api/available-slots?date=2024-01-15"
```

**Expected Response:**
```json
[
  {
    "time": "2024-01-15T08:00:00",
    "end_time": "2024-01-15T10:00:00",
    "is_available": true
  },
  {
    "time": "2024-01-15T10:15:00",
    "end_time": "2024-01-15T12:00:00",
    "is_available": true
  },
  {
    "time": "2024-01-15T13:00:00",
    "end_time": "2024-01-15T15:00:00",
    "is_available": true
  },
  {
    "time": "2024-01-15T15:15:00",
    "end_time": "2024-01-15T17:00:00",
    "is_available": true
  }
]
```

---

### Test 3: Create Appointment

```bash
curl -X POST "http://localhost:8000/api/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Jane Smith",
    "client_email": "jane@example.com",
    "client_phone": "+1987654321",
    "appointment_time": "2024-01-15T10:00:00",
    "notes": "Test appointment"
  }'
```

**Expected Response:** (201 Created)
```json
{
  "id": 1,
  "client_name": "Jane Smith",
  "client_email": "jane@example.com",
  "client_phone": "+1987654321",
  "appointment_time": "2024-01-15T10:00:00",
  "duration_minutes": 120,
  "status": "confirmed",
  "notes": "Test appointment",
  "created_at": "2024-01-15T09:00:00",
  "updated_at": "2024-01-15T09:00:00"
}
```

---

### Test 4: Get All Appointments

```bash
curl "http://localhost:8000/api/appointments"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "client_name": "Jane Smith",
    "client_email": "jane@example.com",
    ...
  }
]
```

---

### Test 5: Get Specific Appointment

```bash
curl "http://localhost:8000/api/appointments/1"
```

**Expected Response:**
```json
{
  "id": 1,
  "client_name": "Jane Smith",
  ...
}
```

---

### Test 6: Delete Appointment

```bash
curl -X DELETE "http://localhost:8000/api/appointments/1"
```

**Expected Response:** (204 No Content)

---

### Test 7: Get Calendar

```bash
curl "http://localhost:8000/api/calendar"
```

**Expected Response:**
```json
{
  "2024-01-15": [
    {
      "id": 1,
      "client_name": "Jane Smith",
      "client_email": "jane@example.com",
      "start_time": "2024-01-15T10:00:00",
      "end_time": "2024-01-15T12:00:00",
      "status": "confirmed"
    }
  ]
}
```

---

### Test 8: Get Notifications

```bash
curl "http://localhost:8000/api/notifications"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "appointment_id": 1,
    "notification_type": "new_appointment",
    "message": "New appointment from Jane Smith on 2024-01-15 10:00",
    "is_read": false,
    "created_at": "2024-01-15T09:00:00"
  }
]
```

---

### Test 9: Mark Notification as Read

```bash
curl -X PATCH "http://localhost:8000/api/notifications/1/read"
```

**Expected Response:**
```json
{
  "message": "Notification marked as read"
}
```

---

### Test 10: Conflict Detection API

```bash
# First appointment
curl -X POST "http://localhost:8000/api/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Client 1",
    "client_email": "client1@example.com",
    "appointment_time": "2024-01-15T10:00:00"
  }'

# Try to book overlapping appointment
curl -X POST "http://localhost:8000/api/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Client 2",
    "client_email": "client2@example.com",
    "appointment_time": "2024-01-15T10:00:00"
  }'
```

**Expected Result:**
- ✅ First appointment succeeds (201)
- ✅ Second appointment fails (409 Conflict)

---

## 🧬 Edge Case Testing

### Test 1: Minimum Time Slot

**Objective:** Verify 2-hour minimum duration

**Steps:**
1. Book at 8:00 AM (ends at 10:00 AM)
2. Try to book at 10:00 AM (should work - 15 min break)
3. Try to book at 9:00 AM (should fail - overlaps)

---

### Test 2: End of Day

**Objective:** Verify appointments must end by 6:00 PM

**Steps:**
1. Try to book at 4:30 PM (would end at 6:30 PM - should fail)
2. Try to book at 4:00 PM (ends at 6:00 PM - should succeed)

---

### Test 3: Lunch Break Boundaries

**Objective:** Verify lunch break is 12:00 PM - 1:00 PM

**Steps:**
1. Book at 10:00 AM (ends at 12:00 PM - should succeed)
2. Book at 1:00 PM (starts at 1:00 PM - should succeed)
3. Book at 11:00 AM (ends at 1:00 PM - should fail, overlaps lunch)

---

### Test 4: Past Dates

**Objective:** Verify cannot book in the past

**Steps:**
1. Try to select yesterday's date (should be disabled)
2. Try to select today's date (should be disabled)
3. Select tomorrow's date (should work)

---

### Test 5: Email Validation

**Objective:** Verify email validation

**Steps:**
1. Try: `invalid-email` (should fail)
2. Try: `test@` (should fail)
3. Try: `test@example.com` (should succeed)

---

## 📊 Performance Testing

### Test 1: Multiple Concurrent Bookings

**Objective:** Verify system handles concurrent requests

**Steps:**
1. Open 5 browser windows
2. Simultaneously book appointments in all windows
3. Verify no double-bookings occur

---

### Test 2: Large Calendar View

**Objective:** Verify performance with many appointments

**Steps:**
1. Create 50+ appointments
2. Load calendar view
3. Verify page loads quickly

---

## 🔍 Browser Console Testing

### Check for Errors

1. Open browser DevTools (F12)
2. Go to Console tab
3. Book an appointment
4. Verify no red errors appear

### Check Network Requests

1. Open browser DevTools (F12)
2. Go to Network tab
3. Book an appointment
4. Verify all requests return 2xx or 3xx status codes

### Check WebSocket Connection

1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter for "WS"
4. Verify WebSocket connection is established
5. Book an appointment
6. Verify WebSocket message is received

---

## ✅ Test Checklist

- [ ] Can book appointment successfully
- [ ] Conflict detection prevents double-booking
- [ ] Lunch break is respected
- [ ] Business hours are enforced
- [ ] Calendar displays all appointments
- [ ] Real-time notifications work
- [ ] Form validation works
- [ ] API endpoints respond correctly
- [ ] No console errors
- [ ] WebSocket connection works
- [ ] Appointments persist after refresh
- [ ] Can delete appointments
- [ ] Can mark notifications as read

---

## 🐛 Debugging Tips

### Enable SQL Logging

Edit `database.py`:
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True
    ...
)
```

### Check Database Directly

```bash
# Windows
sqlite3 appointments.db

# macOS/Linux
sqlite3 appointments.db
```

Then run SQL queries:
```sql
SELECT * FROM appointments;
SELECT * FROM notifications;
```

### Monitor Server Logs

Watch the terminal where you started the server for any errors or warnings.

---

## 📝 Test Report Template

```
Test Date: ___________
Tester: ___________
Version: 1.0.0

Test Results:
- Manual Tests: PASS / FAIL
- API Tests: PASS / FAIL
- Edge Cases: PASS / FAIL
- Performance: PASS / FAIL

Issues Found:
1. ___________
2. ___________

Notes:
___________
```

---

**All tests passing?** System is ready for production! 🎉
