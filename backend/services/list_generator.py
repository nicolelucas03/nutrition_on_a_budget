import anthropic 
import os 
import json
from typing import List, Dict 
from dotenv import load_dotenv 

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def generate_optimized_list(current_items: List[Dict], budget: float = None) -> Dict:
    """
    Generate a better grocery list based on current shopping habits
    """
    
    # Calculate current stats
    current_total = sum(item['price'] for item in current_items)
    current_avg_score = sum(item['healthScore'] for item in current_items) / len(current_items) if current_items else 0
    
    # Set budget to 80% of current spending if not specified
    if budget is None:
        budget = current_total * 0.8
    
    current_list_str = json.dumps([{
        'item': item['item'],
        'price': item['price'],
        'healthScore': item['healthScore'],
        'category': item.get('category', 'other')
    } for item in current_items], indent=2)
    
    prompt = f"""You are a nutrition and budget expert. A person bought these groceries:

{current_list_str}

Current total: ${current_total:.2f}
Average health score: {current_avg_score:.1f}/100

Create a BETTER grocery list for next week with these goals:
1. Budget: ${budget:.2f} or less
2. Target health score: 70+ (significantly better than current)
3. Keep some items they like (if healthy)
4. Replace unhealthy items with affordable healthy alternatives
5. Ensure nutritional variety (protein, produce, whole grains, healthy fats)

Return ONLY valid JSON in this format:
{{
    "optimizedList": [
        {{"item": "Chicken Breast", "price": 8.99, "healthScore": 85, "category": "protein", "reason": "Lean protein source"}},
        {{"item": "Brown Rice", "price": 3.49, "healthScore": 75, "category": "grains", "reason": "Whole grain, filling"}}
    ],
    "swaps": [
        {{
            "original": "White Bread",
            "originalPrice": 2.50,
            "replacement": "Whole Wheat Bread",
            "replacementPrice": 3.49,
            "reason": "More fiber and nutrients",
            "savings": -0.99
        }}
    ],
    "summary": {{
        "totalCost": 58.50,
        "avgHealthScore": 72,
        "moneySaved": 15.50,
        "itemCount": 12
    }}
}}

Important:
- Prices should be realistic US grocery store prices
- Focus on common, affordable healthy foods (eggs, oats, beans, frozen veggies, bananas, chicken, rice)
- List should have 10-15 items
- Stay within budget
- Show 3-5 specific swaps from their current list
- Calculate accurate totals

Return ONLY the JSON, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        text = message.content[0].text.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(text)
        return result
        
    except Exception as e:
        print(f"Error generating optimized list: {e}")
        import traceback
        traceback.print_exc()
        return {
            "optimizedList": [],
            "swaps": [],
            "summary": {
                "totalCost": budget,
                "avgHealthScore": 70,
                "moneySaved": 0,
                "itemCount": 0
            }
        }

# FOR TESTING PURPOSES
def test_list_generator():
    """Test optimized list generation"""
    sample_items = [
        {"item": "Coca Cola", "price": 5.99, "healthScore": 25, "category": "beverages"},
        {"item": "White Bread", "price": 2.50, "healthScore": 40, "category": "grains"},
        {"item": "Doritos", "price": 4.99, "healthScore": 20, "category": "snacks"},
        {"item": "Ice Cream", "price": 6.99, "healthScore": 30, "category": "frozen"},
        {"item": "Frozen Pizza", "price": 8.99, "healthScore": 35, "category": "frozen"}
    ]
    
    print("Testing optimized list generation...")
    result = generate_optimized_list(sample_items, budget=25)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_list_generator()