import { AnalysisResponse } from '../types';

interface Props {
  data: AnalysisResponse;
  onReset: () => void;
}

export default function ComparisonView({ data, onReset }: Props) {
  const { current, optimized } = data;

  const getScoreColor = (score: number) => {
    if (score >= 70) return '#10b981';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="comparison-container">
      <button onClick={onReset} className="back-btn">
        ← Upload New Receipt
      </button>

      <div className="hero-comparison">
        <div className="comparison-side current">
          <h2>Your Current Shopping</h2>
          <div className="big-stat">
            <span className="label">Total</span>
            <span className="value">${current.totalCost.toFixed(2)}</span>
          </div>
          <div className="big-stat">
            <span className="label">Health Score</span>
            <span className="value" style={{ color: getScoreColor(current.avgHealthScore) }}>
              {current.avgHealthScore}/100
            </span>
          </div>
        </div>

        <div className="arrow-divider">→</div>

        <div className="comparison-side optimized">
          <h2>Optimized List</h2>
          <div className="big-stat">
            <span className="label">Total</span>
            <span className="value savings">${optimized.summary.totalCost.toFixed(2)}</span>
          </div>
          <div className="big-stat">
            <span className="label">Health Score</span>
            <span className="value" style={{ color: getScoreColor(optimized.summary.avgHealthScore) }}>
              {optimized.summary.avgHealthScore}/100
            </span>
          </div>
        </div>
      </div>

      {optimized.summary.moneySaved > 0 && (
        <div className="savings-banner">
          💰 You could save <strong>${optimized.summary.moneySaved.toFixed(2)}</strong> per week
          = <strong>${(optimized.summary.moneySaved * 4).toFixed(2)}</strong> per month!
        </div>
      )}

      {optimized.swaps && optimized.swaps.length > 0 && (
        <section className="swaps-section">
          <h3>🔄 Recommended Swaps</h3>
          <div className="swaps-grid">
            {optimized.swaps.map((swap, idx) => (
              <div key={idx} className="swap-card">
                <div className="swap-comparison">
                  <div className="swap-from">
                    <span className="swap-label">Instead of:</span>
                    <div className="swap-item">{swap.original}</div>
                    <div className="swap-price">${swap.originalPrice.toFixed(2)}</div>
                  </div>
                  <div className="swap-arrow">→</div>
                  <div className="swap-to">
                    <span className="swap-label">Try:</span>
                    <div className="swap-item">{swap.replacement}</div>
                    <div className="swap-price">${swap.replacementPrice.toFixed(2)}</div>
                  </div>
                </div>
                <div className="swap-details">
                  <span className="swap-reason">{swap.reason}</span>
                  {swap.savings !== 0 && (
                    <span className={`swap-savings ${swap.savings > 0 ? 'positive' : 'negative'}`}>
                      {swap.savings > 0 ? 'Save' : 'Invest'} ${Math.abs(swap.savings).toFixed(2)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="shopping-list-section">
        <h3>🛒 Your Optimized Shopping List</h3>
        <p className="section-subtitle">
          {optimized.optimizedList.length} items · ${optimized.summary.totalCost.toFixed(2)} total
        </p>
        
        <div className="shopping-list">
          {optimized.optimizedList.map((item, idx) => (
            <div key={idx} className="list-item">
              <div className="item-main">
                <div className="item-name">{item.item}</div>
                <div className="item-price">${item.price.toFixed(2)}</div>
              </div>
              <div className="item-details">
                <span className="item-category">{item.category}</span>
                <span 
                  className="item-score"
                  style={{ color: getScoreColor(item.healthScore) }}
                >
                  {item.healthScore}/100
                </span>
              </div>
              {item.reason && (
                <div className="item-reason">{item.reason}</div>
              )}
            </div>
          ))}
        </div>

        <button className="print-btn" onClick={() => window.print()}>
          🖨️ Print Shopping List
        </button>
      </section>

      <section className="current-items-section">
        <details>
          <summary>View your original receipt ({current.itemCount} items)</summary>
          <div className="current-items-grid">
            {current.items.map((item, idx) => (
              <div key={idx} className="current-item">
                <span className="item-name">{item.item}</span>
                <span className="item-price">${item.price.toFixed(2)}</span>
                <span 
                  className="item-score"
                  style={{ color: getScoreColor(item.healthScore) }}
                >
                  {item.healthScore}
                </span>
              </div>
            ))}
          </div>
        </details>
      </section>
    </div>
  );
}