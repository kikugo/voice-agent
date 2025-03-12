import logging

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import cartesia, openai, deepgram, silero, turn_detector


load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are an AI technical interviewer conducting a software engineering interview. "
            "Ask relevant questions about the candidate's experience, technical skills, and projects. "
            "Be professional and thorough in your evaluation. "
            "Start by asking the candidate to introduce themselves. "
            "After each response, analyze it and ask relevant follow-up questions. "
            "Focus on both technical depth and problem-solving abilities. "
            "At the end of the interview, provide a brief evaluation of the candidate."
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting interview for participant {participant.identity}")

    # Configure the agent with improved settings for interviews
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4"),  # Using GPT-4 for better interview capabilities
        tts=cartesia.TTS(),
        turn_detector=turn_detector.EOUModel(),
        min_endpointing_delay=1.0,  # Increased to allow for more thoughtful responses
        max_endpointing_delay=10.0,  # Increased to handle longer answers
        chat_ctx=initial_ctx,
    )

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)

    agent.start(ctx.room, participant)

    # Start the interview with a professional greeting
    await agent.say("Hello, I'll be conducting your technical interview today. Please introduce yourself and tell me about your background in software engineering.", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
