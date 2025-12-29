from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.claude_ocr import parse_receipt_with_claude
from services.nutrition import get_nutrition_with_claude
from services.list_generator import generate_optimized_list
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Nutrition on a Budget API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "Nutrition on a Budget API is running",
        "version": "1.0",
        "endpoints": ["/api/analyze"]
    }

@app.post("/api/analyze")
async def analyze_receipt(
    file: UploadFile = File(...),
    budget: float = Form(None)
):
    """
    Main endpoint: Upload receipt, get optimized shopping list
    
    Returns:
    - current: your receipt items with health analysis
    - optimized: better shopping list for next week
    """
    try:
        print(f"\n{'='*50}")
        print("New request received")
        print(f"{'='*50}")
        
        contents = await file.read()
        print(f"Image uploaded ({len(contents)} bytes)")
        
        print("Step 1: Extracting items from receipt...")
        items = parse_receipt_with_claude(contents)
        
        if not items:
            return {
                "success": False,
                "error": "Could not extract items from receipt. Please try a clearer image."
            }
        
        print(f"✓ Extracted {len(items)} items")
        
        print("Step 2: Analyzing nutrition...")
        enriched_items = get_nutrition_with_claude(items)
        print(f"Nutrition analysis complete")
        
        print("Step 3: Generating optimized shopping list...")
        optimized_data = generate_optimized_list(enriched_items, budget)
        print(f"Optimized list generated")
        
        # Calculate current stats for comparison
        current_total = sum(item['price'] for item in enriched_items)
        current_avg_score = sum(item['healthScore'] for item in enriched_items) / len(enriched_items)
        
        print(f"\n{'='*50}")
        print("Analysis complete!")
        print(f"Current: ${current_total:.2f}, Health: {current_avg_score:.1f}")
        print(f"Optimized: ${optimized_data['summary']['totalCost']:.2f}, Health: {optimized_data['summary']['avgHealthScore']:.1f}")
        print(f"{'='*50}\n")
        
        return {
            "success": True,
            "current": {
                "items": enriched_items,
                "totalCost": round(current_total, 2),
                "avgHealthScore": round(current_avg_score, 1),
                "itemCount": len(enriched_items)
            },
            "optimized": optimized_data
        }
        
    except Exception as e:
        print(f"\n Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
