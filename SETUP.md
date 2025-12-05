# Setup Guide - Appointment Booking System

Complete step-by-step guide to get the Appointment Booking System up and running.

## 📋 Prerequisites

Before you begin, ensure you have:
- Windows 10/11, macOS, or Linux
- Python 3.8 or higher
- pip (comes with Python)
- A modern web browser (Chrome, Firefox, Safari, Edge)
- At least 100MB of free disk space

## 🪟 Windows Setup

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### Step 2: Navigate to Project Directory

Open Command Prompt and navigate to the project:
```bash
cd "f:\Projects\appointment handling"
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install (this may take a few minutes).

### Step 6: Run the Application

**Option A: Using the startup script (recommended)**
```bash
run.bat
```

**Option B: Manual startup**
```bash
python main.py
```

### Step 7: Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

You should see the Appointment Booking System interface.

---

## 🍎 macOS Setup

### Step 1: Install Python

Using Homebrew (recommended):
```bash
brew install python@3.11
```

Or download from https://www.python.org/downloads/

Verify installation:
```bash
python3 --version
```

### Step 2: Navigate to Project Directory

```bash
cd /path/to/appointment\ handling
```

Or if using the exact path:
```bash
cd "f:/Projects/appointment handling"
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Make Script Executable (Optional)

```bash
chmod +x run.sh
```

### Step 7: Run the Application

**Option A: Using the startup script**
```bash
./run.sh
```

**Option B: Manual startup**
```bash
python main.py
```

### Step 8: Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

---

## 🐧 Linux Setup

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
```

Verify installation:
```bash
python3 --version
```

### Step 2: Navigate to Project Directory

```bash
cd ~/path/to/appointment\ handling
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Make Script Executable

```bash
chmod +x run.sh
```

### Step 7: Run the Application

**Option A: Using the startup script**
```bash
./run.sh
```

**Option B: Manual startup**
```bash
python main.py
```

### Step 8: Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

---

## 🧪 Verify Installation

After starting the application, verify everything is working:

### 1. Check Web Interface
- Navigate to http://localhost:8000
- You should see the appointment booking form
- The page should load without errors

### 2. Check API Documentation
- Navigate to http://localhost:8000/docs
- You should see the Swagger UI with all API endpoints
- Try the "Try it out" feature on any endpoint

### 3. Check Health Endpoint
Open a new terminal/command prompt and run:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00",
  "service": "Appointment Booking System"
}
```

### 4. Test Booking
1. Fill in the booking form with test data
2. Select a date and time
3. Click "Book Appointment"
4. You should see a success message
5. Check the Calendar tab to see the appointment

---

## 🔧 Configuration

### Change Server Port

If port 8000 is already in use, edit `main.py`:

Find this line (at the bottom):
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,  # Change this number
    reload=True,
)
```

Change `port=8000` to any available port (e.g., `port=8001`).

### Change Business Hours

Edit `services.py` and find the `AvailabilityService` class:

```python
BUSINESS_START = time(8, 0)   # Change to desired start time
BUSINESS_END = time(18, 0)    # Change to desired end time
LUNCH_START = time(12, 0)     # Change to desired lunch start
LUNCH_END = time(13, 0)       # Change to desired lunch end
```

### Change Session Duration

In `services.py`, find:
```python
SESSION_DURATION = 120  # Change to desired duration in minutes
BREAK_DURATION = 15     # Change to desired break duration
```

### Change Database Location

Edit `database.py`:
```python
DATABASE_URL = "sqlite+aiosqlite:///./appointments.db"
# Change the path as needed
```

---

## 🐛 Troubleshooting

### Issue: "Python not found" or "python: command not found"

**Solution:**
- Ensure Python is installed and added to PATH
- Try using `python3` instead of `python`
- Restart your terminal/command prompt after installing Python

### Issue: "Port 8000 already in use"

**Solution:**
1. Find what's using port 8000:
   - Windows: `netstat -ano | findstr :8000`
   - macOS/Linux: `lsof -i :8000`
2. Either stop that process or change the port in `main.py`

### Issue: "ModuleNotFoundError" when running

**Solution:**
- Ensure virtual environment is activated (you should see `(venv)` in prompt)
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: Database errors

**Solution:**
- Delete `appointments.db` file to reset database
- Restart the application

### Issue: WebSocket connection fails

**Solution:**
- Check firewall settings
- Ensure port 8000 is not blocked
- Try accessing from `localhost` instead of IP address

### Issue: Frontend not loading

**Solution:**
- Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
- Try a different browser
- Check browser console for errors (F12)

### Issue: Appointments not appearing in calendar

**Solution:**
- Refresh the page (F5)
- Check browser console for errors
- Ensure appointments are created successfully (check success message)

---

## 📊 Database Reset

To completely reset the system and start fresh:

1. Stop the application (Ctrl+C)
2. Delete the database file:
   - Windows: `del appointments.db`
   - macOS/Linux: `rm appointments.db`
3. Restart the application
4. A new database will be created automatically

---

## 🚀 Advanced Setup

### Running in Production

For production deployment:

1. Set `reload=False` in `main.py`
2. Use a production ASGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

### Using PostgreSQL

To use PostgreSQL instead of SQLite:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `database.py`:
   ```python
   DATABASE_URL = "postgresql+asyncpg://user:password@localhost/appointments"
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t appointment-system .
docker run -p 8000:8000 appointment-system
```

---

## 📞 Getting Help

If you encounter issues:

1. **Check the README.md** for API documentation and features
2. **Review error messages** carefully - they usually indicate the problem
3. **Check the browser console** (F12) for frontend errors
4. **Check terminal output** for backend errors
5. **Review the code comments** in the source files

---

## ✅ Checklist

Before considering setup complete:

- [ ] Python is installed and in PATH
- [ ] Virtual environment is created and activated
- [ ] Dependencies are installed
- [ ] Application starts without errors
- [ ] Web interface loads at http://localhost:8000
- [ ] API documentation loads at http://localhost:8000/docs
- [ ] Health check endpoint responds
- [ ] Can create an appointment
- [ ] Calendar displays appointments
- [ ] Notifications appear when booking

---

**Setup Complete!** 🎉

Your Appointment Booking System is ready to use. Start booking appointments!

For more information, see README.md
