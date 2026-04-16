# 🏥 SafeLink: IoT Worker Safety Helmet Monitoring System

**SafeLink** is a comprehensive, real-time safety monitoring platform designed for industrial environments. By integrating IoT helmet hardware with a powerful dashboard, SafeLink provides managers with critical telemetry data to ensure worker safety, track device health, and respond to emergencies instantly.

---

## 🌟 Key Features

### 📊 Safety Analytics
- **Live Trend Charts**: Visualize temperature and gas (ppm) levels over time using high-performance Chart.js integration.
- **Historical Insights**: Track data history for every worker to identify potential long-term exposure risks.

### 🔋 Device Health Monitoring
- **Connectivity Status**: Real-time "Online/Offline" monitoring using heartbeat logic.
- **Battery Tracking**: Monitor the power levels of all active helmets to ensure zero downtime.
- **Visual Indicators**: Live pulsing indicators for active devices.

### 🚑 Emergency Protocols
- **Worker Identity**: Instant access to worker Name, Blood Group, and Emergency Contact details.
- **Zone Tracking**: Identify the deployment zone/location of every worker at a glance.

### 🛡️ Admin Control & Security
- **Strict Access Control**: Administrators have exclusive rights to edit or delete worker profiles and helmet registrations.
- **Global Dashboard**: Workers can monitor site-wide safety data but cannot modify system settings.
- **User Management**: Admins can manage staff profiles, reset passwords, and update worker photos.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kirubeshvarman28/Project---SafeLink---SaverHelmet.git
   cd Project---SafeLink---SaverHelmet
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**:
   ```bash
   # Run the setup script to create a default admin
   python setup_admin.py
   ```
   *Default Admin Username: `admin` | Password: `admin123`*

4. **Run the Application**:
   ```bash
   python run_app.py
   ```
   The dashboard will be available at `http://127.0.0.1:5000`.

---

## 🤖 Testing with Simulation
To see the system in action without physical hardware, use our built-in ESP32 simulator:
1. Keep the main server running.
2. Open a new terminal and run:
   ```bash
   python simulate_esp32.py
   ```
3. Watch the "Online" status and data trends update in real-time on the dashboard!

---

## 📁 Project Structure
```text
Project---SafeLink/
├── app/
│   ├── api.py           # IoT Data Endpoints
│   ├── auth.py          # User Authentication
│   ├── models.py        # Database Schema (SQLAlchemy)
│   ├── routes.py        # Web Navigation & Logic
│   ├── static/          # CSS, JS, & Profile Uploads
│   └── templates/       # HTML Pages (Tailwind CSS)
├── app.db               # SQLite Database
├── run_app.py           # Server Entry Point
├── setup_admin.py       # Admin Setup Tool
└── simulate_esp32.py    # Hardware Data Simulator
```

---

## 🛠️ Hardware Integration (ESP32)
Update your ESP32 Arduino code to point to the local server:
```cpp
const char* serverUrl = "http://YOUR_LOCAL_IP:5000/api/data";
```

---
**SafeLink** — *Protecting what matters most.*