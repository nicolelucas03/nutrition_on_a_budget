# SmartCart

**Upload your grocery receipt, get a healthier shopping list for less.** 

A full-stack AI-powered application that analyzes grocery receipts, provides nutritional insights, and generates optimized shopping lists that are both healthier and more budget-friendly. 

![SmartCart Logo](/frontend/src/assets/smartcart_logo.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [How It Works](#how-it-works)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Overview

**The Problem:** Many people believe eating healthy is expensive and don't realize they're overspending on unhealthy processed foods.

**The Solution:** Nutrition on a Budget uses AI to analyze your current grocery shopping habits and generates a personalized, optimized shopping list that:
- Costs 15-30% less
- Has significantly better nutritional value (health score 70+)
- Provides specific, actionable food swaps
- Maintains variety and satisfaction

### Features

### Core Functionality
- **Receipt OCR**: Upload any grocery receipt photo, automatically extract items and prices
- **Nutrition Analysis**: AI-powered health scoring (0-100) for each item
- **Budget Optimization**: Generate cheaper alternatives while improving nutrition
- **Smart Swaps**: Specific recommendations (e.g., "Replace Doritos with Hummus + Carrots, save $1.49")
- **Visual Comparison**: Before/after view showing cost and health improvements
- **Printable Shopping List**: Take your optimized list to the store

### Technical Features
- Real-time processing with Claude AI (Anthropic)
- Responsive design (mobile + desktop)
- RESTful API architecture
- Type-safe TypeScript frontend
- Error handling and validation
- CORS-enabled for local development

## Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Styling with gradients and animations

### Backend
- **Python 3.9+** - Core language
- **FastAPI** - Modern Python web framework
- **Anthropic Claude API** - AI for OCR and analysis
- **Uvicorn** - ASGI server
- **Pillow** - Image processing
- **python-dotenv** - Environment management

### AI & Data
- **Claude Sonnet 4** - Vision model for receipt OCR
- **Claude Sonnet 4** - Text model for nutrition analysis and recommendations
- Custom health scoring algorithm
- Nutrition categorization (produce, protein, dairy, grains, etc.)

## 📁 Project Structure
```
nutrition_on_a_budget/
├── backend/
│   ├── services/
│   │   ├── claude_ocr.py          # Receipt image → items extraction
│   │   ├── nutrition.py           # Nutrition analysis & health scoring
│   │   └── list_generator.py     # Optimized list generation
│   ├── main.py                    # FastAPI application
│   ├── .env                       # Environment variables (API keys)
│   ├── requirements.txt           # Python dependencies
│   └── test_receipt.jpg           # Sample receipt for testing
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadReceipt.tsx  # Receipt upload interface
│   │   │   └── ComparisonView.tsx # Results display
│   │   ├── types.ts               # TypeScript type definitions
│   │   ├── App.tsx                # Main application component
│   │   ├── App.css                # Styling
│   │   └── main.tsx               # Entry point
│   ├── package.json               # Node dependencies
│   └── vite.config.ts             # Vite configuration
│
├── README.md
└── LICENSE
```

## Setup & Installation

### Prerequisites

- **Node.js** 20.19+ or 22.12+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/downloads/))
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))

### Backend Setup

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/nutrition-on-a-budget.git
   cd nutrition-on-a-budget/backend
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install fastapi uvicorn python-multipart anthropic pillow python-dotenv
```
4. **Configure environment variables**
   
   Create a `.env` file in the `backend/` directory:
```env
   ANTHROPIC_API_KEY=your_api_key_here
```

5. **Test the backend**
```bash
   # Test OCR
   python services/claude_ocr.py
   
   # Test nutrition analysis
   python services/nutrition.py
   
   # Test list generator
   python services/list_generator.py
```

6. **Start the server**
```bash
   uvicorn main:app --reload
```
   
   Server runs at: http://localhost:8000
   
   API docs at: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**
```bash
   cd ../frontend
```

2. **Install dependencies**
```bash
   npm install
   npm install axios
```

3. **Start development server**
```bash
   npm run dev
```
   
   App runs at: http://localhost:5173


## Usage

### Basic Workflow

1. **Start both servers** (backend and frontend)
   
   Terminal 1:
```bash
   cd backend
   uvicorn main:app --reload
```
   
   Terminal 2:
```bash
   cd frontend
   npm run dev
```

2. **Open the app** at http://localhost:5173

3. **Upload a receipt**
   - Click the upload area
   - Select a grocery receipt photo (JPG, PNG)
   - Optionally set a target budget
   - Click "Analyze Receipt"

4. **Review results**
   - See your current spending and health score
   - View the optimized shopping list
   - Review specific food swaps
   - Print or save your new list

### Tips for Best Results

- **Receipt quality**: Use clear, well-lit photos
- **Supported formats**: JPG, PNG (under 5MB)
- **Processing time**: Typically 30-60 seconds
- **Budget setting**: Leave blank to auto-calculate 20% savings


## API Documentation

### Endpoints

#### `POST /api/analyze`

Analyze a grocery receipt and generate optimized shopping list.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): Receipt image file
  - `budget` (optional): Target budget in dollars

**Response:**
```json
{
  "success": true,
  "current": {
    "items": [
      {
        "item": "Coca Cola",
        "price": 5.99,
        "healthScore": 25,
        "category": "beverages",
        "nutrients": {
          "protein": 0,
          "sugar": 39,
          "fiber": 0,
          "sodium": 45
        }
      }
    ],
    "totalCost": 75.50,
    "avgHealthScore": 42.3,
    "itemCount": 12
  },
  "optimized": {
    "optimizedList": [
      {
        "item": "Sparkling Water",
        "price": 3.99,
        "healthScore": 85,
        "category": "beverages",
        "reason": "Zero sugar, hydrating"
      }
    ],
    "swaps": [
      {
        "original": "Coca Cola",
        "originalPrice": 5.99,
        "replacement": "Sparkling Water",
        "replacementPrice": 3.99,
        "reason": "Eliminate sugar, save money",
        "savings": 2.00
      }
    ],
    "summary": {
      "totalCost": 55.75,
      "avgHealthScore": 73.5,
      "moneySaved": 19.75,
      "itemCount": 14
    }
  }
}
```

#### `GET /`
Health check endpoint. Returns API status.

#### `GET /health`
Returns `{"status": "healthy"}`

### Interactive API Docs

Visit http://localhost:8000/docs for Swagger UI with interactive API testing.


## How It Works

### Architecture Overview
```
User uploads receipt
        ↓
[Frontend] React app sends image to API
        ↓
[Backend] FastAPI receives request
        ↓
[Claude OCR] Extract items + prices from image
        ↓
[Nutrition Analysis] Score each item (0-100)
        ↓
[List Generator] Create optimized alternatives
        ↓
[Response] Send comparison data to frontend
        ↓
[Display] Show before/after + actionable swaps
```

### Health Scoring Algorithm

Items are scored 0-100 based on nutritional value:

- **80-100**: Very healthy (vegetables, fruits, lean proteins, whole grains)
- **60-79**: Moderately healthy (dairy, nuts, complex carbs)
- **40-59**: Less healthy (refined grains, some processed foods)
- **0-39**: Unhealthy (soda, candy, chips, highly processed items)

Scoring considers:
- Sugar content (negative impact)
- Sodium levels (negative impact)
- Protein content (positive impact)
- Fiber content (positive impact)
- Processing level (whole foods preferred)

### Optimization Strategy

The list generator:
1. Analyzes current shopping patterns
2. Identifies unhealthy/expensive items
3. Suggests affordable healthy swaps
4. Ensures nutritional variety (protein, produce, grains, fats)
5. Stays within budget (default: 80% of current spending)
6. Aims for health score of 70+

## Contact

Author: Nicole Lucas 

Email: nicoleclucas003@gmail.com

---