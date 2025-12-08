"""
Simple test script to verify the API is working.
"""
import requests
import json

API_BASE = "http://localhost:5001"


def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_generate_reply():
    """Test generate reply endpoint."""
    print("\nTesting /generate-reply endpoint...")
    try:
        payload = {
            "clientSequence": ["What documents do I need for a tourist visa?"],
            "chatHistory": []
        }
        response = requests.post(f"{API_BASE}/generate-reply", json=payload)
        print(f"✓ Status: {response.status_code}")
        result = response.json()
        print(f"✓ AI Reply: {result.get('aiReply', 'N/A')[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("Visa AI Agent - API Test")
    print("=" * 60)
    print("\nMake sure the Flask server is running (python app.py)")
    print()
    
    health_ok = test_health()
    if not health_ok:
        print("\n✗ Server is not responding. Please start the server first.")
        return
    
    test_generate_reply()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

