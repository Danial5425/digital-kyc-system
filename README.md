# Digital KYC System

A simple multi-platform Digital KYC system consisting of:

- **FastAPI Backend**
- **React Web App**
- **React Native (Expo) Mobile App**

This README describes how to install and start each component.

---

##  1. Start the Backend (FastAPI)

### Step 1 — Create Virtual Environment
```bash
cd kyc_project
python3 -m venv venv
source venv/bin/activate

Step 2 — Install Requirements
pip install -r requirements.txt


Step 3 — Start Server
uvicorn main:app --reload

2. Start the Web App (React + Vite)
Step 1 — Install Node Packages
cd ../kyc_frontend
npm install

Step 2 — Start Web Dev Server
npm run dev


Web app runs at:

http://localhost:5173/

3. Start the Mobile App (React Native + Expo)
Install Node Packages
cd ../kyc_mobile
npm install

Run Expo Web
npm run web


Runs at:

http://localhost:19006/

OR run on Android Emulator
npm run android

OR run on physical phone (Expo Go)
npm start


Scan the QR code shown in terminal.

 API Base URL Configuration
For React Web

Use:

const API_BASE = "http://127.0.0.1:8000";

For Expo Web
const API_BASE = "http://127.0.0.1:8000";

For Android Emulator
const API_BASE = "http://10.0.2.2:8000";

For Real Device (Same WiFi)

Get laptop IP:

ip addr


Set:const API_BASE = "http://YOUR_LAPTOP_IP:8000";

 Folder Structure
HDFC_KYC/
├── kyc_project/      # FastAPI backend
├── kyc_frontend/     # React web app
└── kyc_mobile/       # React Native app
