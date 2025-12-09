"""
Gemini API client wrapper.
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from typing import List, Dict, Optional
import json


class GeminiClient:
    """Wrapper for Gemini API interactions."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Use the model from config, with fallback to gemini-pro
        # gemini-pro is the most stable and widely available model
        self.model_name = GEMINI_MODEL if GEMINI_MODEL else "gemini-pro"
        self.model = genai.GenerativeModel(self.model_name)


    def generate_reply(self, system_prompt: str, client_sequence: List[str],
                       chat_history: Optional[List[Dict]] = None) -> str:
        """
        Generate a reply using Gemini.
        """
        # Build the user message
        user_message_parts = []

        if chat_history:
            for msg in chat_history:
                role = "Client" if msg["direction"] == "in" else "Consultant"
                user_message_parts.append(f"{role}: {msg['text']}")

        # Add the current client sequence
        for client_msg in client_sequence:
            user_message_parts.append(f"Client: {client_msg}")

        user_message = "\n".join(user_message_parts)

        # Build full prompt
        full_prompt = f"{system_prompt}\n\nConversation:\n{user_message}\n\nConsultant Reply:"

        try:
            response = self.model.generate_content(full_prompt)
            reply_text = response.text.strip()

            # If model returns JSON
            if reply_text.startswith("{") and "reply" in reply_text:
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("reply", reply_text)
                except json.JSONDecodeError:
                    pass

            return reply_text

        except Exception as e:
            raise Exception(
                f"Error generating reply with Gemini ({self.model_name}): {str(e)}"
            )


    def improve_prompt(self, editor_prompt: str, existing_prompt: str,
                       client_sequence: List[str], chat_history: List[Dict],
                       real_consultant_reply: str, predicted_ai_reply: str) -> str:
        """
        Auto-improve the system prompt based on differences between real vs AI reply.
        """
        history_text = ""
        if chat_history:
            for msg in chat_history:
                role = "Client" if msg["direction"] == "in" else "Consultant"
                history_text += f"{role}: {msg['text']}\n"

        client_text = "\n".join([f"Client: {msg}" for msg in client_sequence])

        improvement_request = f"""Editor Prompt:
{editor_prompt}

Current System Prompt:
{existing_prompt}

Conversation Context:
Chat History:
{history_text if history_text else "No previous history"}

Client Sequence:
{client_text}

Real Consultant Reply:
{real_consultant_reply}

AI Predicted Reply:
{predicted_ai_reply}

Please analyze and improve the prompt. Output only JSON:
{{ "prompt": "<updated prompt>" }}
"""

        try:
            response = self.model.generate_content(improvement_request)
            reply_text = response.text.strip()

            if reply_text.startswith("{"):
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("prompt", existing_prompt)
                except:
                    pass

            return reply_text

        except Exception as e:
            raise Exception(
                f"Error improving prompt with Gemini ({self.model_name}): {str(e)}"
            )


    def manual_prompt_update(self, editor_prompt: str, existing_prompt: str,
                             instructions: str) -> str:
        """
        Developer manually updates the system prompt using the editor prompt.
        """
        update_request = f"""Editor Prompt:
{editor_prompt}

Current System Prompt:
{existing_prompt}

Developer Instructions:
{instructions}

Return only JSON:
{{ "prompt": "<updated prompt>" }}
"""

        try:
            response = self.model.generate_content(update_request)
            reply_text = response.text.strip()

            if reply_text.startswith("{"):
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("prompt", existing_prompt)
                except:
                    pass

            return reply_text

        except Exception as e:
            raise Exception(
                f"Error manually updating prompt with Gemini ({self.model_name}): {str(e)}"
            )



##old code from cursor
'''
###Gemini API client wrapper###

import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from typing import List, Dict, Optional
import json


class GeminiClient:
    ###Wrapper for Gemini API interactions.
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def generate_reply(self, system_prompt: str, client_sequence: List[str], 
                      chat_history: Optional[List[Dict]] = None) -> str:
        """
        Generate a reply using Gemini.
        
        Args:
            system_prompt: The system prompt from Supabase
            client_sequence: List of client messages to respond to
            chat_history: Optional chat history before the client sequence
            
        Returns:
            Generated reply text
        """
        # Build the user message from chat history and client sequence
        user_message_parts = []
        
        if chat_history:
            # Format chat history
            for msg in chat_history:
                role = "Client" if msg["direction"] == "in" else "Consultant"
                user_message_parts.append(f"{role}: {msg['text']}")
        
        # Add current client sequence
        for client_msg in client_sequence:
            user_message_parts.append(f"Client: {client_msg}")
        
        user_message = "\n".join(user_message_parts)
        
        # Construct full prompt
        full_prompt = f"{system_prompt}\n\nConversation:\n{user_message}\n\nConsultant Reply:"
        
        try:
            response = self.model.generate_content(full_prompt)
            
            # Try to parse JSON response if it's in JSON format
            reply_text = response.text.strip()
            
            # Check if response is JSON
            if reply_text.startswith("{") and "reply" in reply_text:
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("reply", reply_text)
                except json.JSONDecodeError:
                    pass
            
            return reply_text
        
        except Exception as e:
            raise Exception(f"Error generating reply with Gemini: {str(e)}")
    
    def improve_prompt(self, editor_prompt: str, existing_prompt: str, 
                      client_sequence: List[str], chat_history: List[Dict],
                      real_consultant_reply: str, predicted_ai_reply: str) -> str:
        """
        Use Gemini with editor prompt to improve the system prompt.
        
        Args:
            editor_prompt: The editor prompt from Supabase
            existing_prompt: Current system prompt
            client_sequence: Client messages that triggered the conversation
            chat_history: Chat history before client sequence
            real_consultant_reply: Human consultant's actual reply
            predicted_ai_reply: AI's predicted reply
            
        Returns:
            Updated prompt text
        """
        # Format chat history
        history_text = ""
        if chat_history:
            for msg in chat_history:
                role = "Client" if msg["direction"] == "in" else "Consultant"
                history_text += f"{role}: {msg['text']}\n"
        
        client_text = "\n".join([f"Client: {msg}" for msg in client_sequence])
        
        # Build the improvement request
        improvement_request = f"""Editor Prompt:
{editor_prompt}

Current System Prompt:
{existing_prompt}

Conversation Context:
Chat History:
{history_text if history_text else "No previous history"}

Client Sequence:
{client_text}

Real Consultant Reply:
{real_consultant_reply}

AI Predicted Reply:
{predicted_ai_reply}

Please analyze and improve the prompt. Output only the updated prompt in JSON format:
{{ "prompt": "<updated prompt>" }}"""
        
        try:
            response = self.model.generate_content(improvement_request)
            reply_text = response.text.strip()
            
            # Try to parse JSON response
            if reply_text.startswith("{"):
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("prompt", existing_prompt)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract prompt from text
                    if "prompt" in reply_text.lower():
                        # Try to find the prompt content
                        start_idx = reply_text.find('"prompt"')
                        if start_idx != -1:
                            # Extract the prompt value
                            start_quote = reply_text.find('"', start_idx + 8) + 1
                            end_quote = reply_text.find('"', start_quote)
                            if end_quote != -1:
                                return reply_text[start_quote:end_quote]
            
            # If all parsing fails, return the raw response
            return reply_text
        
        except Exception as e:
            raise Exception(f"Error improving prompt with Gemini: {str(e)}")
    
    def manual_prompt_update(self, editor_prompt: str, existing_prompt: str, 
                            instructions: str) -> str:
        """
        Manually update prompt based on developer instructions.
        
        Args:
            editor_prompt: The editor prompt from Supabase
            existing_prompt: Current system prompt
            instructions: Developer's instructions for changes
            
        Returns:
            Updated prompt text
        """
        update_request = f"""Editor Prompt:
{editor_prompt}

Current System Prompt:
{existing_prompt}

Developer Instructions:
{instructions}

Please update the prompt according to the instructions. Output only the updated prompt in JSON format:
{{ "prompt": "<updated prompt>" }}"""
        
        try:
            response = self.model.generate_content(update_request)
            reply_text = response.text.strip()
            
            # Try to parse JSON response
            if reply_text.startswith("{"):
                try:
                    parsed = json.loads(reply_text)
                    return parsed.get("prompt", existing_prompt)
                except json.JSONDecodeError:
                    pass
            
            return reply_text
        
        except Exception as e:
            raise Exception(f"Error manually updating prompt with Gemini: {str(e)}")

'''