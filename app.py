import logging
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import io
import torch
import soundfile as sf
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

synthesizer = pipeline("text-to-audio", "facebook/musicgen-stereo-large", device="cuda:0", torch_dtype=torch.float16)

def generate_audio(text: str):
    # Here you can implement your audio generation logic
    # For demonstration purposes, let's use your existing code
    logger.info("Generating audio for text: %s", text)
    try:
        music = synthesizer(text, forward_params={"max_new_tokens": 256})
        return music["audio"][0].T, music["sampling_rate"]
    except Exception as e:
        logger.error("Error generating audio for text: %s", text, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate audio")


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate_audio")
async def generate_audio_endpoint(request: Request):
    # Read the request body and decode it as JSON
    data = await request.json()
    text = data.get("text", "")

    logger.info("Received request to generate audio for text: %s", text)
    try:
        audio_data, sampling_rate = generate_audio(text)
        logger.info("Generated audio for text: %s", text)
    except HTTPException as e:
        logger.error("HTTP error generating audio for text: %s", text, exc_info=True)
        raise e
    except Exception as e:
        logger.error("Error generating audio for text: %s", text, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate audio")

    with io.BytesIO() as buffer:
        sf.write(buffer, audio_data, sampling_rate, format="WAV")
        buffer.seek(0)
        return Response(content=buffer.getvalue(), media_type="audio/wav")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
