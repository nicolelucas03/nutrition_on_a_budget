import anthropic
import os
import json
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def get_nutrition_with_claude(items: List[Dict]) -> List[Dict]:
    """
    Use Claude to estimate nutrition for each item
    """
    
    item_names = [item['item'] for item in items]
    
    prompt = f"""For each grocery item below, provide a health score (0-100) and key nutrients.

Items: {', '.join(item_names)}

Return ONLY valid JSON in this format:
[
    {{
        "item": "Milk",
        "healthScore": 65,
        "nutrients": {{
            "protein": 8,
            "sugar": 12,
            "fiber": 0,
            "sodium": 100
        }},
        "category": "dairy"
    }}
]

Health scoring guide:
- 80-100: Very healthy (vegetables, fruits, lean protein, whole grains)
- 60-79: Moderately healthy (dairy, nuts, some carbs)
- 40-59: Less healthy (white bread, sugary cereals)
- 0-39: Unhealthy (soda, candy, chips, processed foods)

Categories: produce, protein, dairy, grains, snacks, beverages, frozen, other

Return ONLY the JSON array, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        text = message.content[0].text.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        
        nutrition_data = json.loads(text)
        
        # Merge with original items
        enriched_items = []
        for item in items:
            nutrition = next((n for n in nutrition_data if n['item'].lower() == item['item'].lower()), None)
            if nutrition:
                enriched_items.append({
                    **item,
                    'healthScore': nutrition['healthScore'],
                    'nutrients': nutrition['nutrients'],
                    'category': nutrition.get('category', 'other')
                })
            else:
                # Default if not found
                enriched_items.append({
                    **item,
                    'healthScore': 50,
                    'nutrients': {},
                    'category': 'other'
                })
        
        return enriched_items
        
    except Exception as e:
        print(f"Error in nutrition analysis: {e}")
        # Fallback: return items with the default scores
        return [{**item, 'healthScore': 50, 'nutrients': {}, 'category': 'other'} for item in items]

#FOR TESTING PURPOSES
def test_nutrition():
    """Test nutrition analysis"""
    sample_items = [
        {"item": "Coca Cola", "price": 5.99},
        {"item": "Bananas", "price": 2.50},
        {"item": "Chicken Breast", "price": 8.99}
    ]
    
    print("Testing nutrition analysis...")
    enriched = get_nutrition_with_claude(sample_items)
    print(json.dumps(enriched, indent=2))

if __name__ == "__main__":
    test_nutrition()