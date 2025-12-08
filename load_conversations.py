"""
Utility script to load conversations.json and train the AI.
"""
import json
import requests
import sys
from pathlib import Path

API_BASE_URL = "http://localhost:5001"


def load_conversations_file(file_path: str) -> list:
    """Load conversations from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def train_from_conversations(conversations: list):
    """Send conversations to the /load-training-data endpoint."""
    url = f"{API_BASE_URL}/load-training-data"
    
    response = requests.post(url, json={"conversations": conversations})
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Processed {result['processed']} training examples")
        
        success_count = sum(1 for r in result['results'] if r['status'] == 'success')
        error_count = result['processed'] - success_count
        
        print(f"  - Successful: {success_count}")
        if error_count > 0:
            print(f"  - Errors: {error_count}")
            for r in result['results']:
                if r['status'] == 'error':
                    print(f"    Error: {r.get('error', 'Unknown error')}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python load_conversations.py <path_to_conversations.json>")
        print("\nExample:")
        print("  python load_conversations.py conversations.json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"✗ File not found: {file_path}")
        sys.exit(1)
    
    print(f"Loading conversations from {file_path}...")
    conversations = load_conversations_file(file_path)
    print(f"✓ Loaded {len(conversations)} conversations")
    
    print("\nTraining AI from conversations...")
    print("(Make sure the Flask server is running on http://localhost:5001)")
    train_from_conversations(conversations)
    
    print("\n✓ Training complete!")


if __name__ == "__main__":
    main()

