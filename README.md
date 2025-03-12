# AI Voice Assistant - Setup Guide

<p align="center">
  <img src="./.github/assets/app-icon.png" alt="Voice Assistant App Icon" width="100" height="100">
</p>

## Dev Setup

To get started, follow these steps to set up both the backend and frontend components of the AI Technical Interview Voice Assistant.

### 1. Backend Setup (Python Agent)

Navigate to the backend directory (`voice-pipeline-agent-python-main`):

```bash
cd voice-pipeline-agent-python-main
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python3 agent.py download-files
```

**Environment Configuration:**

Create a `.env.local` file in the `voice-pipeline-agent-python-main` directory and add your API keys:

```env
LIVEKIT_URL="YOUR_LIVEKIT_URL"
LIVEKIT_API_KEY="YOUR_LIVEKIT_API_KEY"
LIVEKIT_API_SECRET="YOUR_LIVEKIT_API_SECRET"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
CARTESIA_API_KEY="YOUR_CARTESIA_API_KEY"  # Optional
DEEPGRAM_API_KEY="YOUR_DEEPGRAM_API_KEY"
```

*   **LiveKit Credentials:**  Obtain from [LiveKit Cloud](https://cloud.livekit.io).
*   **OpenAI API Key:** Get from [OpenAI Platform](https://platform.openai.com).
*   **Deepgram API Key:** Sign up at [Deepgram](https://deepgram.com).
*   **Cartesia API Key:** Optional; required if using Cartesia TTS from [Cartesia](https://cartesia.ai).

### 2. Frontend Setup (Next.js App)

Navigate to the frontend directory (`voice-assistant-frontend`):

```bash
cd voice-assistant-frontend
```

Install frontend dependencies using pnpm or npm:

```bash
pnpm install   # Or npm install
```

**Environment Configuration:**

Create a `.env.local` file in the `voice-assistant-frontend` directory and add your LiveKit project credentials:

```env
LIVEKIT_URL="YOUR_LIVEKIT_URL"
LIVEKIT_API_KEY="YOUR_LIVEKIT_API_KEY"
LIVEKIT_API_SECRET="YOUR_LIVEKIT_API_SECRET"
```

## License

[Apache-2.0](LICENSE)
```