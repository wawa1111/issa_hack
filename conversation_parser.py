"""
Parser for conversation JSON format to extract training examples.
"""
from typing import List, Dict, Tuple


class ConversationParser:
    """Parses conversation JSON into training examples."""
    
    @staticmethod
    def parse_conversation(conversation_data: Dict) -> List[Dict]:
        """
        Parse a single conversation into multiple training examples.
        
        Args:
            conversation_data: A conversation object with contact_id, scenario, and conversation array
            
        Returns:
            List of training examples, each containing:
            - client_sequence: List of consecutive client messages
            - chat_history: All messages before the client sequence
            - consultant_reply: The consultant's reply after the client sequence
        """
        conversation = conversation_data.get("conversation", [])
        if not conversation:
            return []
        
        training_examples = []
        i = 0
        
        while i < len(conversation):
            # Find the start of a client sequence (direction="in")
            if conversation[i]["direction"] != "in":
                i += 1
                continue
            
            # Collect consecutive client messages
            client_sequence = []
            client_start_idx = i
            
            while i < len(conversation) and conversation[i]["direction"] == "in":
                client_sequence.append(conversation[i]["text"])
                i += 1
            
            # If we have client messages, look for the consultant reply
            if client_sequence and i < len(conversation):
                # Collect consecutive consultant messages (direction="out")
                consultant_reply_parts = []
                
                while i < len(conversation) and conversation[i]["direction"] == "out":
                    consultant_reply_parts.append(conversation[i]["text"])
                    i += 1
                
                # Combine consultant reply parts
                consultant_reply = " ".join(consultant_reply_parts) if consultant_reply_parts else None
                
                if consultant_reply:
                    # Build chat history (all messages before the client sequence)
                    chat_history = []
                    for j in range(client_start_idx):
                        chat_history.append({
                            "message_id": conversation[j].get("message_id"),
                            "direction": conversation[j]["direction"],
                            "text": conversation[j]["text"],
                            "timestamp": conversation[j].get("timestamp")
                        })
                    
                    training_examples.append({
                        "client_sequence": client_sequence,
                        "chat_history": chat_history,
                        "consultant_reply": consultant_reply,
                        "scenario": conversation_data.get("scenario"),
                        "contact_id": conversation_data.get("contact_id")
                    })
            else:
                # No consultant reply found, skip this client sequence
                i += 1
        
        return training_examples
    
    @staticmethod
    def parse_conversations_file(conversations: List[Dict]) -> List[Dict]:
        """
        Parse multiple conversations from a conversations.json file.
        
        Args:
            conversations: List of conversation objects
            
        Returns:
            Flattened list of all training examples from all conversations
        """
        all_examples = []
        
        for conversation_data in conversations:
            examples = ConversationParser.parse_conversation(conversation_data)
            all_examples.extend(examples)
        
        return all_examples
    
    @staticmethod
    def format_chat_history_for_prompt(chat_history: List[Dict]) -> str:
        """
        Format chat history for use in prompts.
        
        Args:
            chat_history: List of message dictionaries
            
        Returns:
            Formatted string representation of chat history
        """
        if not chat_history:
            return "No previous conversation history."
        
        formatted = []
        for msg in chat_history:
            role = "Client" if msg["direction"] == "in" else "Consultant"
            formatted.append(f"{role}: {msg['text']}")
        
        return "\n".join(formatted)

