import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="VoiceShield AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    await websocket.accept()
    print("WebSocket connection established. Starting Stream Ingestion.")
    
    try:
        while True:
            # Stage 01: Receive Audio Stream Ingestion (HTML5 Web Audio buffer)
            data = await websocket.receive_text()
            
            # Simulated Processing Delay (< 300ms budget)
            await asyncio.sleep(0.2)
            
            payload = json.loads(data)
            is_scam = payload.get("is_scam", False)
            
            if is_scam:
                # Stage 02 & 03: Feature Extraction & Ensemble AI Inference
                risk_score = random.uniform(76.0, 99.9) # >75% is Threat
                status = "THREAT"
                logs = [
                    "Stage 02: DSP extracting Mel-Spectrograms...",
                    "Stage 03: Branch A (Spectral) detected vocoder phase flaws.",
                    f"Stage 03: Branch B (Acoustic) Wav2Vec 2.0 flagged anomaly. Risk: {risk_score:.1f}%",
                    "Stage 04: Triggering Action Engine - Alerting User!"
                ]
            else:
                risk_score = random.uniform(2.0, 19.9) # <=20% is Safe
                status = "SAFE"
                logs = [
                    "Stage 02: DSP extracting Mel-Spectrograms...",
                    "Stage 03: Branch A & B validation passed.",
                    f"Status: Safe human voice authenticated. Risk: {risk_score:.1f}%"
                ]

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
