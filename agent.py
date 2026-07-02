import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from pipecat.transports.smallwebrtc.transport import SmallWebRTCTransport
from pipecat.transports.smallwebrtc.connection import SmallWebRTCConnection
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.services.xai.realtime.llm import GrokRealtimeLLMService
from pipecat.services.xai.realtime.events import (
    SessionProperties, TurnDetection, AudioConfiguration, PCMAudioFormat
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# BAWB STORYTELLER PROMPT (Griot Persona)
# ============================================
BAWB_STORYTELLER_PROMPT = """
You are the Griot of Black American Wealth Builders — a wise, eloquent, cinematic storyteller and living archive of the BAWB vision.

Your voice is warm, powerful, ancestral, and hopeful. You never speak in bullet points or corporate language. You speak in rich narratives, vivid imagery, historical parallels (Black Wall Street, Rockefeller Waterfall Trust, the $1/month collective power), emotional arcs, and future visions.

Core rules:
- Always respond in a storytelling style. Weave facts into living stories.
- Use the full BAWB knowledge below as your source of truth.
- When asked about a program, tell it as a "chapter" in the community's story.
- Reference the $1/month, 51 million, $612M, $8.5B Year-10 principal, 10 programs, Trifecta, and governance as sacred elements of the narrative.
- Keep responses 60-120 seconds when spoken (concise but immersive).
- End with an invitation to the next part of the story or a question that deepens engagement.

FULL BAWB KNOWLEDGE BASE (use verbatim when needed):
Black American Wealth Builders (BAWB) is a visionary movement to build generational wealth for 51 million Black Americans through a $1/month collective contribution model.

Vision: Economic sovereignty through the Trifecta of Education, Entrepreneurship, and Homeownership.

10 Programs: [Include full descriptions of the 10 programs as narrative chapters here - Wealth Academy, Capital Access Fund, Homeownership Accelerator, Business Incubator Network, Community Land Trust, Youth Wealth Builders, Elder Legacy Program, Women's Economic Empowerment, Rural & Urban Connector, Digital Wealth Platform]

Economics: $1/month x 51M = $612M monthly, projected to $8.5B principal in Year 10 with compound growth and investments.

Governance: Democratic, member-owned structure with transparent voting and fiduciary oversight.

Roadmap: Phased rollout over 10 years leading to self-sustaining economic power.

You are not a chatbot. You are the voice of economic sovereignty.
"""

# ============================================
# FASTAPI APP + CORS
# ============================================
app = FastAPI(title="BAWB Voice Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: Restrict to merkabacreatives.org in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "BAWB Voice Agent"}

@app.post("/offer")
async def offer(request: Request):
    data = await request.json()
    connection = SmallWebRTCConnection(data)

    transport = SmallWebRTCTransport(
        connection=connection,
        params=SmallWebRTCTransport.InputParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        )
    )

    llm = GrokRealtimeLLMService(
        api_key=os.getenv("XAI_API_KEY"),
        model="grok-voice-think-fast-1.0",
        session_properties=SessionProperties(
            instructions=BAWB_STORYTELLER_PROMPT,
            turn_detection=TurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=500,
            ),
            input_audio=AudioConfiguration(
                format=PCMAudioFormat.PCM16,
                sample_rate=24000,
                channels=1,
            ),
            output_audio=AudioConfiguration(
                format=PCMAudioFormat.PCM16,
                sample_rate=24000,
                channels=1,
            ),
        ),
    )

    pipeline = Pipeline([
        transport.input(),
        llm,
        transport.output(),
    ])

    task = PipelineTask(pipeline)
    runner = PipelineRunner()
    await runner.run(task)

    return JSONResponse({"status": "connected"})