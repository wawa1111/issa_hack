"""
Manages prompts: loading, updating, and initializing base prompts.
"""
from supabase_client import SupabaseDB
from typing import Optional


class PromptManager:
    """Manages system prompts and editor prompts."""
    
    def __init__(self, db: SupabaseDB):
        self.db = db
        self._initialize_base_prompts()
    
    def _initialize_base_prompts(self):
        """Initialize base prompts if they don't exist."""
        # Check if we have a system prompt
        if not self.db.get_latest_prompt():
            base_prompt = """You are a warm, friendly visa consultant. Your role is to help customers with visa-related questions in a casual, human, and approachable manner.

Tone Guidelines:
- Be warm, friendly, and conversational
- Use casual language (but still professional)
- Show empathy and understanding
- Avoid robotic or formal phrasing
- Match the natural, human tone of real consultants
- Be helpful and patient

Response Guidelines:
- Provide general guidance only (no hallucination)
- If you're unsure about specific details, acknowledge it
- Keep responses clear and concise
- Address the customer's specific question directly

Output Format:
Always respond in JSON format:
{ "reply": "<your response text>" }"""
            
            self.db.save_prompt(base_prompt)
            print("✓ Initialized base system prompt")
        
        # Check if we have an editor prompt
        if not self.db.get_latest_editor_prompt():
            editor_prompt = """You are a prompt editor for a visa consultant AI system. Your job is to analyze conversations and improve the system prompt to make AI responses better match human consultant responses.

When analyzing:
1. Compare the real consultant reply vs AI reply
2. Identify tone differences (too formal? too casual? missing warmth?)
3. Identify missing details or information
4. Identify incorrect information or hallucinations
5. Note any structural differences in how information is presented

When updating the prompt:
- Make surgical, precise changes (don't rewrite everything)
- Preserve what's working well
- Add specific guidance for identified issues
- Maintain the warm, human-like tone requirement
- Update only the necessary sections

Output Format:
Always respond in JSON format:
{ "prompt": "<updated system prompt>" }"""
            
            self.db.save_editor_prompt(editor_prompt)
            print("✓ Initialized base editor prompt")
    
    def get_system_prompt(self) -> str:
        """Get the latest system prompt."""
        prompt = self.db.get_latest_prompt()
        if not prompt:
            raise ValueError("No system prompt found in database")
        return prompt
    
    def get_editor_prompt(self) -> str:
        """Get the latest editor prompt."""
        prompt = self.db.get_latest_editor_prompt()
        if not prompt:
            raise ValueError("No editor prompt found in database")
        return prompt
    
    def update_system_prompt(self, new_prompt: str) -> dict:
        """Update the system prompt with a new version."""
        return self.db.save_prompt(new_prompt)

