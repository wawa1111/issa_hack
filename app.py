"""
Flask API server for the visa consultant AI agent.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase_client import SupabaseDB
from prompt_manager import PromptManager
from gemini_client import GeminiClient
from conversation_parser import ConversationParser
from typing import List, Dict
import traceback

app = Flask(__name__)
CORS(app)

# Initialize components
try:
    db = SupabaseDB()
    prompt_manager = PromptManager(db)
    gemini_client = GeminiClient()
    parser = ConversationParser()
except Exception as e:
    print(f"Error initializing components: {e}")
    print("Make sure SUPABASE_URL and SUPABASE_ANON_KEY are set as environment variables")
    raise


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "visa-consultant-ai"})


@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    """
    Generate an AI reply to a customer question.
    
    Request body:
    {
        "clientSequence": ["message1", "message2"],
        "chatHistory": [
            {"direction": "in", "text": "...", "message_id": 1, "timestamp": ...},
            ...
        ]
    }
    
    Response:
    {
        "aiReply": "<generated reply>"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        client_sequence = data.get("clientSequence", [])
        chat_history = data.get("chatHistory", [])
        
        if not client_sequence:
            return jsonify({"error": "clientSequence is required"}), 400
        
        # Get latest prompt from Supabase
        system_prompt = prompt_manager.get_system_prompt()
        
        # Generate reply using Gemini
        ai_reply = gemini_client.generate_reply(
            system_prompt=system_prompt,
            client_sequence=client_sequence,
            chat_history=chat_history if chat_history else None
        )
        
        return jsonify({
            "aiReply": ai_reply
        })
    
    except Exception as e:
        print(f"Error in /generate-reply: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/improve-ai", methods=["POST"])
def improve_ai():
    """
    Self-learning endpoint: Compare AI reply with human reply and improve the prompt.
    
    Request body:
    {
        "clientSequence": ["message1"],
        "chatHistory": [...],
        "consultantReply": "Human consultant's actual reply"
    }
    
    Response:
    {
        "predictedReply": "<AI's predicted reply>",
        "updatedPrompt": "<new improved prompt>"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        client_sequence = data.get("clientSequence", [])
        chat_history = data.get("chatHistory", [])
        consultant_reply = data.get("consultantReply", "")
        
        if not client_sequence:
            return jsonify({"error": "clientSequence is required"}), 400
        if not consultant_reply:
            return jsonify({"error": "consultantReply is required"}), 400
        
        # Get current prompts
        system_prompt = prompt_manager.get_system_prompt()
        editor_prompt = prompt_manager.get_editor_prompt()
        
        # Generate AI reply first
        predicted_reply = gemini_client.generate_reply(
            system_prompt=system_prompt,
            client_sequence=client_sequence,
            chat_history=chat_history if chat_history else None
        )
        
        # Use editor to improve the prompt
        updated_prompt = gemini_client.improve_prompt(
            editor_prompt=editor_prompt,
            existing_prompt=system_prompt,
            client_sequence=client_sequence,
            chat_history=chat_history,
            real_consultant_reply=consultant_reply,
            predicted_ai_reply=predicted_reply
        )
        
        # Save the updated prompt to Supabase
        prompt_manager.update_system_prompt(updated_prompt)
        
        # Save training example
        db.save_training_example(
            client_sequence=client_sequence,
            chat_history=chat_history,
            consultant_reply=consultant_reply,
            ai_reply=predicted_reply
        )
        
        return jsonify({
            "predictedReply": predicted_reply,
            "updatedPrompt": updated_prompt
        })
    
    except Exception as e:
        print(f"Error in /improve-ai: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/improve-ai-manually", methods=["POST"])
def improve_ai_manually():
    """
    Manually improve the prompt based on developer instructions.
    
    Request body:
    {
        "instructions": "Be more concise and mention processing time early."
    }
    
    Response:
    {
        "updatedPrompt": "<new improved prompt>"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        instructions = data.get("instructions", "")
        
        if not instructions:
            return jsonify({"error": "instructions is required"}), 400
        
        # Get current prompts
        system_prompt = prompt_manager.get_system_prompt()
        editor_prompt = prompt_manager.get_editor_prompt()
        
        # Use Gemini to update prompt based on instructions
        updated_prompt = gemini_client.manual_prompt_update(
            editor_prompt=editor_prompt,
            existing_prompt=system_prompt,
            instructions=instructions
        )
        
        # Save the updated prompt to Supabase
        prompt_manager.update_system_prompt(updated_prompt)
        
        return jsonify({
            "updatedPrompt": updated_prompt
        })
    
    except Exception as e:
        print(f"Error in /improve-ai-manually: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/parse-conversations", methods=["POST"])
def parse_conversations():
    """
    Parse conversations.json file and extract training examples.
    
    Request body:
    {
        "conversations": [
            {
                "contact_id": "...",
                "scenario": "...",
                "conversation": [...]
            },
            ...
        ]
    }
    
    Response:
    {
        "trainingExamples": [...],
        "count": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        conversations = data.get("conversations", [])
        
        if not conversations:
            return jsonify({"error": "conversations array is required"}), 400
        
        # Parse conversations
        training_examples = parser.parse_conversations_file(conversations)
        
        return jsonify({
            "trainingExamples": training_examples,
            "count": len(training_examples)
        })
    
    except Exception as e:
        print(f"Error in /parse-conversations: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/load-training-data", methods=["POST"])
def load_training_data():
    """
    Parse conversations and automatically call /improve-ai for each training example.
    This is a convenience endpoint for bulk training.
    
    Request body:
    {
        "conversations": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        conversations = data.get("conversations", [])
        
        if not conversations:
            return jsonify({"error": "conversations array is required"}), 400
        
        # Parse conversations
        training_examples = parser.parse_conversations_file(conversations)
        
        results = []
        for example in training_examples:
            try:
                # Simulate internal call to /improve-ai
                client_sequence = example["client_sequence"]
                chat_history = example["chat_history"]
                consultant_reply = example["consultant_reply"]
                
                # Get current prompts
                system_prompt = prompt_manager.get_system_prompt()
                editor_prompt = prompt_manager.get_editor_prompt()
                
                # Generate AI reply
                predicted_reply = gemini_client.generate_reply(
                    system_prompt=system_prompt,
                    client_sequence=client_sequence,
                    chat_history=chat_history if chat_history else None
                )
                
                # Improve prompt
                updated_prompt = gemini_client.improve_prompt(
                    editor_prompt=editor_prompt,
                    existing_prompt=system_prompt,
                    client_sequence=client_sequence,
                    chat_history=chat_history,
                    real_consultant_reply=consultant_reply,
                    predicted_ai_reply=predicted_reply
                )
                
                # Save updated prompt
                prompt_manager.update_system_prompt(updated_prompt)
                
                # Save training example
                db.save_training_example(
                    client_sequence=client_sequence,
                    chat_history=chat_history,
                    consultant_reply=consultant_reply,
                    ai_reply=predicted_reply
                )
                
                results.append({
                    "contact_id": example.get("contact_id"),
                    "status": "success"
                })
            
            except Exception as e:
                results.append({
                    "contact_id": example.get("contact_id"),
                    "status": "error",
                    "error": str(e)
                })
        
        return jsonify({
            "processed": len(results),
            "results": results
        })
    
    except Exception as e:
        print(f"Error in /load-training-data: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    from config import FLASK_DEBUG
    
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=FLASK_DEBUG)

