
# 🏦 Digital KYC System  
*A secure, scalable, multi-platform Digital KYC verification system built with FastAPI (Backend), React (Web), and React Native (Expo Mobile).*

---

## 📛 Badges

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-00cc99?logo=fastapi)
![React](https://img.shields.io/badge/React-Web-61dafb?logo=react)
![React Native](https://img.shields.io/badge/React%20Native-Mobile-0088cc?logo=react)
![Expo](https://img.shields.io/badge/Expo-Framework-black?logo=expo)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📘 Overview

The **Digital KYC System** is designed to provide an end-to-end workflow for digital identity verification similar to enterprise banking systems.  
It supports:

- Aadhaar, PAN, Passport validation  
- Checksum verification (Aadhaar Verhoeff, PAN checksum)  
- Passport validity check (minimum 6 months)  
- Duplicate document detection  
- Photo + selfie verification (placeholder for ML)  
- Multi-step KYC flow with retry limits  
- Web + Mobile App support  
- Secure backend built with FastAPI

This project demonstrates secure, modern, production-ready KYC architecture.

---

# 🧠 Key Features

### ✔ Document Validation
- Aadhaar → Verhoeff checksum  
- PAN → Structure + checksum  
- Passport → MRZ-style pattern + validity check  
- Duplicate detection (hashed fields)

### ✔ Photo Verification
- User uploads passport-size photo  
- User captures selfie  
- Face match (AI module placeholder)

### ✔ Stage-Based Workflow
1. Select Document Types  
2. Upload/Scan Documents  
3. Validate Inputs  
4. Upload Photo & Selfie  
5. Complete KYC  

### ✔ Multi-Platform Architecture
- **React Web App**  
- **Expo Mobile App**  
- **FastAPI Backend with SQLite / MySQL**

---


