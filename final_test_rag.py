import requests
import os
import time
import json
import sys

# Force UTF-8 for stdout to handle emojis on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"
TEST_FILE = "data/sample_policy.txt"

def print_separator():
    print("-" * 60)

def test_health():
    print("1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is Healthy")
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is the server running?")
        return False
    return True

def test_upload():
    print("\n2. Testing Document Upload...")
    if not os.path.exists(TEST_FILE):
        print(f"❌ Test file {TEST_FILE} not found!")
        return False
    
    with open(TEST_FILE, "rb") as f:
        files = {"file": ("sample_policy.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload Success! Doc ID: {data['doc_id']}")
        print(f"   Chunks created: {data['num_chunks']}")
        return True
    else:
        print(f"❌ Upload Failed: {response.text}")
        return False

def test_qa():
    print("\n3. Testing Question Answering (RAG)...")
    
    questions = [
        "What are the mandatory office days?",
        "How much PTO do employees get?",
        "What is the remote work policy?",
        "When are bonuses paid out?",
        "What is the budget for home office equipment?"
    ]
    
    for q in questions:
        print_separator()
        print(f"❓ Question: {q}")
        
        payload = {
            "question": q,
            "max_chunks": 3
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/ask", json=payload)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"💡 Answer ({duration:.2f}s):")
                print(data['answer'])
                print(f"\n📊 Confidence: {data['confidence']}")
                print("Sources used:")
                for src in data['sources']:
                    print(f" - {src['document']} (Score: {src['relevance_score']:.4f})")
            else:
                print(f"❌ Request Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error during QA request: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Final RAG Test using 'TechCorp Employee Handbook' Data\n")
    
    if test_health():
        if test_upload():
            test_qa()
    
    print("\n✅ Test Sequence Correctly Executed.")
