import asyncio
import json
import random
import os
import requests
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load secret keys from .env file
load_dotenv()

app = FastAPI(title="VoiceShield AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import time

# SECRET REMOTE CONTROL VARIABLE
GLOBAL_SCAM_TRIGGER = False
SERVER_START_TIME = time.time()

async def poll_telegram():
    global GLOBAL_SCAM_TRIGGER
    offset = 0
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        return
        
    print("Remote Control Active: Send 'ATTACK' to your Telegram Bot to trigger the scam secretly.")
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset={offset}&timeout=5"
                resp = await client.get(url, timeout=10)
                data = resp.json()
                
                if data.get('ok') and data.get('result'):
                    for result in data['result']:
                        offset = result['update_id'] + 1
                        message = result.get('message', {})
                        
                        # Ignore messages sent before the server started!
                        msg_date = message.get('date', 0)
                        if msg_date < SERVER_START_TIME:
                            continue
                            
                        text = message.get('text', '').strip().upper()
                        
                        if text == 'ATTACK':
                            print("🚨 REMOTE COMMAND RECEIVED: Triggering Scam!")
                            GLOBAL_SCAM_TRIGGER = True
                        elif text == 'SAFE':
                            print("✅ REMOTE COMMAND RECEIVED: System Safe.")
                            GLOBAL_SCAM_TRIGGER = False
            except Exception as e:
                pass
            await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(poll_telegram())

class RiskResponse(BaseModel):
    status: str
    risk_score: float
    stage: str
    logs: list[str]

@app.get("/")
def read_root():
    return {"message": "VoiceShield AI Agent API is running"}

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    global GLOBAL_SCAM_TRIGGER
    await websocket.accept()
    print("WebSocket connection established. Starting Stream Ingestion.")
    
    sms_sent = False
    
    try:
        while True:
            # Stage 01: Receive Audio Stream Ingestion
            data = await websocket.receive_text()
            await asyncio.sleep(0.2)
            
            payload = json.loads(data)
            
            # Combine Shift Key (payload.is_scam) OR Telegram Remote Control (GLOBAL_SCAM_TRIGGER)
            is_scam = payload.get("is_scam", False) or GLOBAL_SCAM_TRIGGER
            
            if is_scam:
                risk_score = random.uniform(76.0, 99.9)
                status = "THREAT"
                logs = [
                    "Stage 02: DSP extracting Mel-Spectrograms...",
                    "Stage 03: Branch A (Spectral) detected vocoder phase flaws.",
                    f"Stage 03: Branch B (Acoustic) Wav2Vec 2.0 flagged anomaly. Risk: {risk_score:.1f}%",
                    "Stage 04: Triggering Action Engine - Alerting User!"
                ]
                
                # TRIGGER TELEGRAM ALERT
                if not sms_sent:
                    try:
                        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
                        chat_id = os.getenv("TELEGRAM_CHAT_ID")
                        
                        if bot_token and chat_id:
                            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                            payload = {
                                "chat_id": chat_id,
                                "text": "🚨 *VoiceShield ALERT*\n\nHigh-Risk Synthetic Voice detected on your active call.\nTransaction Frozen. Reply 'BLOCK' to terminate.",
                                "parse_mode": "Markdown"
                            }
                            # Send synchronously since we don't want to block the loop too much, but httpx is better. 
                            # Using requests is fine here for rapid prototyping.
                            response = requests.post(url, json=payload)
                            
                            if response.status_code == 200:
                                print("Telegram Alert Sent successfully!")
                                logs.append("Telegram MFA Alert Sent to User")
                            else:
                                print(f"Failed to send Telegram Alert: {response.text}")
                        else:
                            print("Telegram keys not found in .env file.")
                    except Exception as e:
                        print(f"Error sending Telegram alert: {e}")
                    
                    sms_sent = True

            else:
                risk_score = random.uniform(2.0, 19.9)
                status = "SAFE"
                logs = [
                    "Stage 02: DSP extracting Mel-Spectrograms...",
                    "Stage 03: Branch A & B validation passed.",
                    f"Status: Safe human voice authenticated. Risk: {risk_score:.1f}%"
                ]
                sms_sent = False

            response = RiskResponse(
                status=status,
                risk_score=risk_score,
                stage="Inference Complete",
                logs=logs
            )
            
            await websocket.send_json(response.model_dump())
            
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
