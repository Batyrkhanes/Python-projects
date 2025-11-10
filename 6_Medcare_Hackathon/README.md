# 🐍 My First Hackathon project

Greetings! This project represents my first collaborative hackathon experience. It was developed during Atyrau Youth Hackathon 3.0, held in Atyrau, Kazakhstan. The hackathon focused on healthcare-related challenges.

---

## 🗂️ Project Overview

This project is a comprehensive healthcare management system, combining a **web platform** and a **Telegram bot** to provide medical services, patient tracking, and administrative functionality.


### Telegram Bot Features
- **Appointment Booking:** select date and time, receive ticket number, check-in via QR code  
- **Health Insurance (OSMS):** check current status, view payment history, track outstanding debt  
- **Lab Tests:** view latest results, test history, real-time updates  
- **Prescriptions:** QR codes, history of medications, current prescriptions  
- **Medical Certificates:** obtain certificates, QR codes for documents, various types of certificates  
- **Doctor Information:** name, room number, work schedule, contact details  
- **Sick Leave Tracker (A51):** track current sick leave, history, validity period  
- **Activity Log:** full action history, last 10 actions, timestamps  

#### Admin Panel Features
- **Access Control:** password-protected login, admin ID-based special access.
- **Appointment Management:** view active appointments, check status, manage queue  
- **Schedule Management:** configure slots, update work schedule, synchronize with MIS (mock)  
- **Broadcasts:** send notifications to patients, system alerts  
- **Analytics (mock):** daily appointment stats, doctor-wise stats, insurance checks  

#### Technical Features
- **MIS Integration:** synchronize appointments, update schedule, confirm cancellations  
- **Medical API Integration:** access and manage medical services  
- **Database Storage:** `DB_USERS_LANG` (language), `DB_APPOINTMENTS` (appointments), `DB_LOGS` (logs)  
- **Localization:** supports Kazakh, Russian, English, full translation of messages and buttons, language switching  

#### Additional Functions
- **Patient Priority Assessment:** automatic evaluation based on vital signs (temperature, heart rate, breathing rate)  
- **QR Code Integration:** for appointments, prescriptions, certificates, lab results  
- **User Support:** contact info, phone/email support, informational messages  

<br>

### Web Platform Features
- **Authentication System:** registration (`/register`), login (`/login`), logout (`/logout`)  
- **User Dashboard:** view personal info, link Telegram, manage personal data  
- **Patient Management:** add, view, delete patients, automatic priority evaluation  
- **AI Functionality:** patient condition analysis, chat with AI assistant, symptom analysis  
- **Insurance Integration:** check status, calculate contributions, manage insurance  
- **Appointment Scheduling:** select specialist/date/time, Telegram notifications  
- **Health Monitoring:** track vitals, visit history, symptom analysis  
- **Smart Patient Sorting:** automatic priority scoring (1–9), categorize as Critical/Urgent/Planned  
- **Messaging Integration:** link with Telegram, automatic notifications, web-bot sync  
- **Chat System:** communicate with AI assistant, store chat history, get medical advice  
- **Localization:** supports Kazakh and Russian, full translation of messages and buttons, language switching.

<br>

### 📝 Note
We didn't implement all the features listed above, but many of them are included in the project.

---

## 👥 Team Members



- Batyrkhan Yessengali (Me) - Telegram Bot Developer - [Github](https://github.com/Batyrkhanes)
- Arsen - Backend Developer - [Github](https://github.com/Arsen44gnu)
- Bekarys - Team Leader - [Github](https://github.com/ZenitsuKimori)
- Abilmansur Aral - SQL Developer
- Tolegen Azen - Designer


---


## 📚 Used Libraries

### Telegram Bot

- [`logging`](https://docs.python.org/3/library/logging.html) — Python standard library for logging events, errors, and debug information; supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL
- [`qrcode`](https://pypi.org/project/qrcode/) — Library for generating QR codes (tickets, prescriptions, certificates); supports size, error correction, and format configuration
- [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) — Handles binary data in memory; allows working with in-memory files for QR codes
- [`python-telegram-bot`](https://python-telegram-bot.org/) library components:
  - `Update` — class to receive Telegram updates
  - `InlineKeyboardButton` — create inline buttons
  - `InlineKeyboardMarkup` — layout for inline keyboard
  - `ReplyKeyboardMarkup` — layout for standard keyboard
  - `KeyboardButton` — create standard keyboard buttons
  - `ReplyKeyboardRemove` — remove keyboard
  - `Application` — main class to run the bot
  - `CommandHandler` — handles commands (e.g., /start)
  - `CallbackQueryHandler` — handles inline button presses
  - `MessageHandler` — handles text messages
  - `filters` — filters for messages
- [`datetime`](https://docs.python.org/3/library/datetime.html) — standard Python library for dates and times; used for appointment dates, document deadlines, and log timestamps
- [`sys`](https://docs.python.org/3/library/sys.html) — standard Python library for system-related tasks; access to command-line arguments and program control

---

### 🌐 Web Platform

- [`os`](https://docs.python.org/3/library/os.html) — standard Python library for system operations
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — load environment variables from `.env` file
- [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) — built-in database for storing app data
- [`json`](https://docs.python.org/3/library/json.html) — standard library for JSON parsing and serialization
- [`datetime`](https://docs.python.org/3/library/datetime.html) — standard library for working with dates and times
- [`contextlib.contextmanager`](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) — manage resources with context managers
- [`Flask`](https://flask.palletsprojects.com/) and related modules:
  - `Flask`, `render_template`, `request`, `jsonify`, `session`, `redirect`, `url_for`
- [`werkzeug.security`](https://werkzeug.palletsprojects.com/) — 
  - `generate_password_hash` — secure password hashing
  - `check_password_hash` — verify hashed passwords
- Project modules:
  - `Database` — database access layer
  - `GitHubModelsAI` — AI service integration
  - `OSMSService` — health insurance functionality
  - `bot.API` — Telegram bot API interface
---

## ⚙️ How to Install

To run this program, you need to install this library below.  
Open your terminal and run the following command:
<br>
### Telegram Bot:
📦 ***python-telegram-bot***
```bash
pip install python-telegram-bot
```

📦 ***qrcode***
```bash
pip install qrcode
```
<br>

### Web Platform:
📦 ***flask***
```bash
pip install flask
```

📦 ***Werkzeug***
```bash
pip install Werkzeug
```

📦 ***python-dotenv***
```bash
pip install python-dotenv
```

## 🚀 How to Run the Project
After installing all required libraries, you can run the Telegram bot or the web platform.

### Telegram Bot
To start the bot, you need to provide the **Telegram Bot token** and set **doctor's name**, **support phone**, **support email**, **admin password**, **admin ID** in bot.py file:

BOT_TOKEN = "BOT_TOKEN_Here" 

PECIALIST_NAME = "Specialist Name Here" 

SUPPORT_PHONE = "Phone_Number_Here"

SUPPORT_EMAIL = "Email_Address_Here"

ADMIN_PASSWORD = "Create_Admin_password_Here" 

ADMIN_ID = "Create_Admin_ID_Here"














************

##  Thank you for your attention! 😊 Made with ❤️ using Python.

