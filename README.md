# VoiceShield

**Smart India Hackathon 2026 — Problem Statement SIH26104**
**Team:** Temperature Zero

VoiceShield is a browser-based prototype for demonstrating real-time voice-cloning impersonation detection and fraud-containment workflows. It pairs a microphone-enabled frontend with a FastAPI WebSocket backend that returns a simulated impersonation-risk assessment.

## What works today

- Live browser microphone access and frequency visualisation
- WebSocket connection between the frontend and FastAPI backend
- Simulated safe/threat risk scores and inference logs
- Threat-state UI with simulated transaction freeze, MFA, room-echo, vocal-tract, and acoustic-CAPTCHA flows
- FastAPI health endpoint at `/`

> This is a hackathon prototype. The backend receives JSON control payloads rather than raw audio and deliberately simulates model inference; it does not make real fraud, identity, or authentication decisions.

## Architecture

```text
Browser microphone + UI
        |
        | WebSocket: ws://localhost:8000/ws/stream
        v
FastAPI / Uvicorn backend
        |
        v
Simulated risk score + status + audit-style logs
        |
        v
Browser containment and CAPTCHA demonstration
```

## Tech stack

- **Frontend:** HTML5, Tailwind CSS (CDN), vanilla JavaScript, Web Audio API
- **Backend:** Python, FastAPI, Pydantic v2, Uvicorn
- **Streaming:** WebSockets served by Uvicorn

## Prerequisites

- Python 3.10 or later (the included virtual environment uses Python 3.14)
- A current Chrome or Edge browser with microphone permission

No FFmpeg, CUDA, PyTorch, database, or external API credentials are required for the current prototype. See [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md) for platform notes.

## Run locally

The project already includes a virtual environment. Activate and use it; do not recreate it.

### 1. Start the backend

From the project root:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
uvicorn main:app --reload
```

The API will be available at <http://127.0.0.1:8000>. Opening that address should return:

```json
{"message":"VoiceShield AI Agent API is running"}
```

### 2. Start the frontend

Open `frontend/index.html` in Chrome or Edge. For the most reliable microphone support, serve the project through a local development server (for example, VS Code Live Server) so it runs on `localhost`.

### 3. Try the demo

1. Select **Live Audio Call Monitoring** and allow microphone access.
2. Speak normally to receive the simulated **SAFE** response.
3. Hold the `Shift` key while the call is active to trigger the simulated **THREAT** response and containment flow.
4. Use the acoustic CAPTCHA control to display the challenge outcome.

## API reference

### `GET /`

Returns an application health message.

### `WS /ws/stream`

Accepts a text JSON message. The prototype recognizes `is_scam`:

```json
{"is_scam": true}
```

It responds with a JSON object containing `status`, `risk_score`, `stage`, and `logs`. A threat response has a score above 75; a safe response is below 20.

## Configuration

The current source code does not read environment variables or require secrets. [.env.example](.env.example) is intentionally empty of credentials and is ready for future integrations.

## Planned SIH architecture (not implemented yet)

The SIH concept presentation describes the following future components. They are not part of the current source code or dependency set:

- 2-second rolling, 16 kHz raw-audio buffers
- DSP feature extraction: Mel spectrograms, MFCCs, pitch, and acoustic features
- Wav2Vec 2.0 and CNN/ResNet deepfake inference
- Speech-to-text and scam/urgency/extortion keyword analysis
- Real Twilio or other step-up MFA integration
- SHA-256 audit evidence, database persistence, and blockchain integration
- Real transaction containment and production-grade fraud decisions

## Repository layout

```text
backend/
  main.py                 FastAPI application and WebSocket simulation
  requirements.txt        Backend runtime dependencies
frontend/
  index.html              Browser dashboard and microphone demo
SYSTEM_DEPENDENCIES.md    Non-Python prerequisites and future-component notes
.env.example              Credential template for future integrations
```

## Safety note

VoiceShield is a demonstration project, not a production fraud-prevention service. Validate models, security controls, data handling, authentication, consent, and accessibility before any real-world deployment.
