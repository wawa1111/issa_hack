# Visa Call Center AI Agent - Self-Learning System

A self-learning AI assistant that helps call center teams answer visa questions. The system uses Google's Gemini API combined with Supabase to store prompts and training data, continuously improving by learning from human consultant conversations.

## Features

- 🤖 **Gemini AI Integration**: Uses `gemini-2.0-flash-thinking-exp-01-21` model
- 🧠 **Self-Learning**: Automatically improves prompts by comparing AI vs human responses
- 📚 **Supabase Database**: Stores prompts, editor prompts, and training examples
- 💬 **Response Alignment**: Ensures AI responses match human consultant tone and style
- 🎯 **Warm, Human-like Tone**: Maintains casual, friendly, empathetic responses
- 🔄 **Prompt Editor System**: Uses AI to surgically improve prompts based on feedback
- 📊 **Conversation Parser**: Extracts training examples from conversation JSON format

## Architecture

```
┌─────────────────┐
│   Flask API     │
│   (app.py)      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌──▼────────┐
│Gemini │  │ Supabase  │
│  API  │  │  Database │
└───────┘  └───────────┘
```

## Project Structure

```
issa_hack/
├── app.py                  # Flask API server with all endpoints
├── config.py               # Configuration and environment variables
├── supabase_client.py      # Supabase database operations
├── prompt_manager.py       # Prompt loading and management
├── gemini_client.py        # Gemini API wrapper
├── conversation_parser.py  # Parse conversations.json format
├── init_supabase.sql       # SQL schema for Supabase tables
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Supabase

1. Create a project at [Supabase](https://app.supabase.com)
2. Go to SQL Editor
3. Run the SQL from `init_supabase.sql` to create the required tables:
   - `prompts` - System prompts (versioned)
   - `editor_prompt` - Editor prompts (versioned)
   - `training_examples` - Training data

### 3. Get Supabase Credentials

1. Go to your Supabase project
2. Navigate to Settings > API
3. Copy the **Project URL** and **anon/public key**

### 4. Configure Environment Variables

Set the following environment variables:

**For Local Development:**
```bash
export GEMINI_API_KEY=your_gemini_api_key_here
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_ANON_KEY=your_anon_key_here
export FLASK_DEBUG=False
```

**Important:** Never hardcode API keys in the code. Always use environment variables.

**For Render Deployment:**
Set these in the Render dashboard under Environment Variables (no .env file needed).

### 5. Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000` (or the port specified by PORT environment variable)

## API Endpoints

### 1. `/generate-reply` (POST)

Generate an AI reply to a customer question.

**Request:**
```json
{
  "clientSequence": ["I'm interested in the DTV visa for Thailand."],
  "chatHistory": [
    {
      "direction": "in",
      "text": "Hello, I work remotely as a software developer.",
      "message_id": 1,
      "timestamp": 1762500000000
    }
  ]
}
```

**Response:**
```json
{
  "aiReply": "Hi there! Thank you for reaching out. The DTV (Destination Thailand Visa) is perfect for remote workers like yourself..."
}
```

### 2. `/improve-ai` (POST)

Self-learning endpoint: Compare AI reply with human reply and automatically improve the prompt.

**Request:**
```json
{
  "clientSequence": ["I'm American and currently in Bali. Can I apply from Indonesia?"],
  "chatHistory": [...],
  "consultantReply": "Yes, you can apply from Indonesia! The DTV visa allows applications from various countries..."
}
```

**Response:**
```json
{
  "predictedReply": "Yes, you can apply from Indonesia...",
  "updatedPrompt": "You are a warm, friendly visa consultant... [improved version]"
}
```

### 3. `/improve-ai-manually` (POST)

Manually improve the prompt based on developer instructions.

**Request:**
```json
{
  "instructions": "Be more concise and mention processing time early in responses."
}
```

**Response:**
```json
{
  "updatedPrompt": "You are a warm, friendly visa consultant... [updated version]"
}
```

### 4. `/parse-conversations` (POST)

Parse conversations.json file and extract training examples.

**Request:**
```json
{
  "conversations": [
    {
      "contact_id": "SYNTH_001",
      "scenario": "First-time DTV applicant",
      "conversation": [...]
    }
  ]
}
```

**Response:**
```json
{
  "trainingExamples": [...],
  "count": 10
}
```

### 5. `/load-training-data` (POST)

Parse conversations and automatically train the AI (bulk training endpoint).

**Request:**
```json
{
  "conversations": [...]
}
```

**Response:**
```json
{
  "processed": 10,
  "results": [
    {"contact_id": "SYNTH_001", "status": "success"},
    ...
  ]
}
```

### 6. `/health` (GET)

Health check endpoint.

## Conversation Data Format

The system expects conversations in this JSON format:

```json
[
  {
    "contact_id": "SYNTH_001",
    "scenario": "First-time DTV applicant – Digital Nomad (Remote Worker)",
    "conversation": [
      {
        "message_id": 1,
        "direction": "in",
        "text": "Hello, I'm interested in the DTV visa for Thailand.",
        "timestamp": 1762500000000
      },
      {
        "message_id": 2,
        "direction": "out",
        "text": "Hi there! Thank you for reaching out...",
        "timestamp": 1762500000000
      }
    ]
  }
]
```

**Rules:**
- `"direction": "in"` = Client messages
- `"direction": "out"` = Consultant (human) messages
- The parser extracts training examples by finding client sequences followed by consultant replies

## Training the AI

### Method 1: Using the Load Script

```bash
python load_conversations.py conversations.json
```

This will:
1. Parse the conversations.json file
2. Extract training examples
3. Call `/improve-ai` for each example
4. Update the prompt iteratively

### Method 2: Using the API Directly

```bash
curl -X POST http://localhost:5001/load-training-data \
  -H "Content-Type: application/json" \
  -d @conversations.json
```

### Method 3: Individual Training

```bash
curl -X POST http://localhost:5001/improve-ai \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": ["Question here"],
    "chatHistory": [],
    "consultantReply": "Human reply here"
  }'
```

## How Self-Learning Works

1. **Generate Reply**: AI generates a reply using current prompt
2. **Compare**: System compares AI reply vs human consultant reply
3. **Analyze**: Editor prompt (also AI-powered) analyzes differences:
   - Tone differences
   - Missing details
   - Incorrect information
   - Structural differences
4. **Update**: Editor makes surgical improvements to the prompt
5. **Save**: Updated prompt is saved to Supabase
6. **Iterate**: Next requests use the improved prompt

## Database Schema

### `prompts` Table
- `id` (UUID): Primary key
- `content` (TEXT): Prompt content
- `created_at` (TIMESTAMP): Creation time

### `editor_prompt` Table
- `id` (UUID): Primary key
- `content` (TEXT): Editor prompt content
- `created_at` (TIMESTAMP): Creation time

### `training_examples` Table
- `id` (UUID): Primary key
- `client_sequence` (JSONB): Array of client messages
- `chat_history` (JSONB): Full chat history
- `consultant_reply` (TEXT): Human consultant's reply
- `ai_reply` (TEXT): AI's predicted reply
- `created_at` (TIMESTAMP): Creation time

## Example Usage

### Python Client Example

```python
import requests

# Generate a reply
response = requests.post("http://localhost:5001/generate-reply", json={
    "clientSequence": ["What documents do I need for a tourist visa?"],
    "chatHistory": []
})

print(response.json()["aiReply"])

# Improve AI from human feedback
response = requests.post("http://localhost:5001/improve-ai", json={
    "clientSequence": ["What documents do I need for a tourist visa?"],
    "chatHistory": [],
    "consultantReply": "Hello! For a tourist visa, you'll need..."
})

print(response.json()["updatedPrompt"])
```

## Requirements

- Python 3.8+
- Supabase account and project
- Google Gemini API key (provided)
- Internet connection (for API calls)

## Notes

- The system automatically initializes base prompts on first run
- Each prompt update creates a new version (full history maintained)
- The more training examples you provide, the better the AI becomes
- The editor prompt can be customized in Supabase for different improvement strategies

## Troubleshooting

### "SUPABASE_URL and SUPABASE_ANON_KEY must be set"
- Make sure environment variables are set (export them or set in Render dashboard)
- Check that the values are correct (no extra spaces)
- For Render: Set these in the dashboard under Environment Variables

### "No system prompt found in database"
- The system should auto-initialize prompts on first run
- If this fails, check Supabase connection and table creation

### API errors
- Check that the Flask server is running
- Verify Gemini API key is valid
- Check Supabase connection and permissions

## License

See LICENSE file for details.
