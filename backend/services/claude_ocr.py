import anthropic
import os
import base64
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found. Check your .env file.")


client = anthropic.Anthropic(api_key=api_key)

def parse_receipt_with_claude(image_bytes: bytes) -> List[Dict]:
    """
    Extract items and prices from receipt using Claude
    """
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Extract all items and prices from this grocery receipt. 
                        Return ONLY a JSON array with this format:
                        [{"item": "Milk", "price": 3.99}, {"item": "Bread", "price": 2.50}]
                        
                        Do not include any other text, just the JSON array."""
                    }
                ],
            }],
        )
        
    
        response_text = message.content[0].text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        items = json.loads(response_text)
        return items
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response: {response_text}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_ocr():
    """Test with a sample receipt image"""
    print("=" * 50)
    print("Testing OCR with Claude...")
    print("=" * 50)
    
    if not os.path.exists("test_receipt.jpg"):
        print("ERROR: test_receipt.jpg not found!")
        return
    
    print("✓ Receipt file found")
    print("Reading image...")
    
    with open("test_receipt.jpg", "rb") as f:
        image_data = f.read()
        print(f"✓ Image loaded ({len(image_data)} bytes)")
        print("Sending to Claude API...")
        
        items = parse_receipt_with_claude(image_data)
        
        print("=" * 50)
        print("RESULTS:")
        print("=" * 50)
        if items:
            print(json.dumps(items, indent=2))
            print(f"\n✓ Found {len(items)} items")
        else:
            print("⚠ No items extracted")

if __name__ == "__main__":
    test_ocr()