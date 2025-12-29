export interface ReceiptItem { 
    item: string; 
    price: number;
    healthScore: number; 
    category: string; 
    nutrients?: { 
        protein?: number; 
        sugar?: number; 
        fiber?: number;
        sodium?: number; 
    };
}

export interface OptimizedItem { 
    item: string;
    price: number; 
    healthScore: number; 
    category: string; 
    reason: string;
}

export interface Swap { 
    original: string; 
    originalPrice: number; 
    replacement: string; 
    replacementPrice: number; 
    reason: string; 
    savings: number;
}

export interface CurrentData {
    items: ReceiptItem[]; 
    totalCost: number; 
    avgHealthScore: number; 
    itemCount: number;
}

export interface OptimizedData { 
    optimizedList: OptimizedItem[]; 
    swaps: Swap[]; 
    summary: { 
        totalCost: number; 
        avgHealthScore: number; 
        moneySaved: number; 
        itemCount: number; 
    };
}

export interface AnalysisResponse { 
    success: boolean;
    current: CurrentData; 
    optimized: OptimizedData;
    error?: string;
}