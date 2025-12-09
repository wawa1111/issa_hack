"""
Supabase client setup and database operations.
"""
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY
from typing import Optional, Dict, List
from datetime import datetime


class SupabaseDB:
    """Wrapper for Supabase database operations."""
    
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set as environment variables")
        
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Initialize Supabase tables if they don't exist."""
        # Note: In production, tables should be created via Supabase dashboard or migrations
        # This is just a reference for the schema
        pass
    
    # ========== PROMPTS TABLE OPERATIONS ==========
    
    def get_latest_prompt(self) -> Optional[str]:
        """
        Get the most recent active prompt from the prompts table.
        
        Returns:
            The latest prompt content, or None if no prompts exist
        """
        try:
            response = self.client.table("prompts") \
                .select("content") \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["content"]
            return None
        except Exception as e:
            print(f"Error fetching latest prompt: {e}")
            return None
    
    def save_prompt(self, content: str) -> Dict:
        """
        Save a new prompt version to the prompts table.
        
        Args:
            content: The prompt content to save
            
        Returns:
            The saved prompt record
        """
        try:
            response = self.client.table("prompts") \
                .insert({
                    "content": content,
                    "created_at": datetime.utcnow().isoformat()
                }) \
                .execute()
            
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error saving prompt: {e}")
            raise
    
    def get_all_prompts(self, limit: int = 10) -> List[Dict]:
        """
        Get all prompts ordered by creation date.
        
        Args:
            limit: Maximum number of prompts to return
            
        Returns:
            List of prompt records
        """
        try:
            response = self.client.table("prompts") \
                .select("*") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching prompts: {e}")
            return []
    
    # ========== EDITOR PROMPT TABLE OPERATIONS ==========
    
    def get_latest_editor_prompt(self) -> Optional[str]:
        """
        Get the most recent editor prompt.
        
        Returns:
            The latest editor prompt content, or None if none exists
        """
        try:
            response = self.client.table("editor_prompt") \
                .select("content") \
                .order("created_at", desc=True) \
                .limit(1) \
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["content"]
            return None
        except Exception as e:
            print(f"Error fetching latest editor prompt: {e}")
            return None
    
    def save_editor_prompt(self, content: str) -> Dict:
        """
        Save a new editor prompt version.
        
        Args:
            content: The editor prompt content
            
        Returns:
            The saved editor prompt record
        """
        try:
            response = self.client.table("editor_prompt") \
                .insert({
                    "content": content,
                    "created_at": datetime.utcnow().isoformat()
                }) \
                .execute()
            
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error saving editor prompt: {e}")
            raise
    
    # ========== TRAINING EXAMPLES TABLE OPERATIONS ==========
    
    def save_training_example(self, client_sequence: List[str], chat_history: List[Dict], 
                            consultant_reply: str, ai_reply: Optional[str] = None) -> Dict:
        """
        Save a training example for future reference.
        
        Args:
            client_sequence: List of client messages
            chat_history: Full chat history before the client sequence
            consultant_reply: The human consultant's reply
            ai_reply: Optional AI-generated reply for comparison
            
        Returns:
            The saved training example record
        """
        try:
            response = self.client.table("training_examples") \
                .insert({
                    "client_sequence": client_sequence,
                    "chat_history": chat_history,
                    "consultant_reply": consultant_reply,
                    "ai_reply": ai_reply,
                    "created_at": datetime.utcnow().isoformat()
                }) \
                .execute()
            
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error saving training example: {e}")
            raise

