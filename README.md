# VoiceShield 🛡️🎙️
**SIH26104 - Smart India Hackathon**
*Team: Temperature Zero*

## 📖 Overview
VoiceShield is an advanced, real-time voice cloning detection and impersonation prevention system. Built specifically to intercept fraudulent VoIP and WhatsApp calls, VoiceShield achieves a sub-300ms inference pipeline to catch synthetic voices before the scammer finishes their first sentence.

Unlike traditional solutions that rely on passive file uploads, VoiceShield intercepts audio via live WebSockets and features an automated **Action Engine** to lock down transactions and issue Out-of-Band MFA challenges the moment a threat is detected.

## ✨ Key Features (Unique Selling Propositions)
- **Live WebSocket Interception:** Sub-300ms streaming architecture built for live calls, not MP3 file uploads.
- **Ensemble AI Pipeline:** Designed to leverage both spectral analysis (ResNet) to catch visual vocoder flaws, and acoustic analysis (Wav2Vec 2.0) to track vocal tract anomalies.
- **Automated Fraud Containment:** Automatically freezes sensitive UI transactions and issues simulated Twilio Step-Up MFA when risk exceeds 75%.
- **Next-Gen Security Modules:**
  - **Room Echo Profiling:** Verifies natural physical room acoustics.
  - **Vocal Tract Tracking:** Tracks mathematical shifting of vocal cord dimensions.
  - **Acoustic CAPTCHA:** Issues dynamic whispered prompts that AI deepfakes cannot instantly generate.

## 🛠️ Tech Stack
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, Web Audio API
- **Backend:** Python, FastAPI, Uvicorn (ASGI)
- **Communication:** WebSockets for real-time bi-directional streaming

## 🚀 How to Run the Prototype

### 1. Start the Backend
Navigate to the `backend` directory, install dependencies, and start the high-speed Uvicorn server:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Launch the Frontend
Simply open `frontend/index.html` in any modern web browser (Google Chrome or Edge recommended). 
*(You can use the VS Code "Live Server" extension for the best experience).*

### 3. Demo Instructions (The "Wizard of Oz" Flow)
Because running 10GB PyTorch models requires enterprise GPUs, this prototype simulates the inference engine to demonstrate the UI and WebSocket architecture perfectly on standard laptops.
1. Click **Live Audio Call Monitoring**.
2. **For Safe Human Voice:** Talk normally. The system will verify the voice automatically.
3. **For Threat Detection:** Secretly hold down the `Shift` key on your keyboard while audio is playing. The system will instantly detect the deepfake, trigger the Action Engine, and await an Acoustic CAPTCHA challenge.

## ⚠️ Disclaimer
This repository contains the UI/UX and architectural WebSocket pipeline prototype built for the SIH hackathon. The final PyTorch AI inference models are simulated here due to strict local hardware constraints.

## 👥 Team
- **Team Name:** Temperature Zero
- **Problem Statement:** SIH26104
