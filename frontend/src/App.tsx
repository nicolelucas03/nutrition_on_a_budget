import { useState } from 'react';
import UploadReceipt from './components/UploadReceipt';
import ComparisonView from './components/ComparisonView';
import { AnalysisResponse } from './types';
import './App.css';
import logo from './assets/smartcart_logo.png';

function App() {
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);

  const handleReset = () => {
    setAnalysisData(null);
  };

  return (
    <div className="app">
      <header className="header">
        <img src={logo} alt="SmartCart Logo" className="logo" />
        <p>Upload your receipt and get a healthier shopping list for less!</p>
      </header>

      <main className="main">
        {!analysisData ? (
          <UploadReceipt onAnalysisComplete={setAnalysisData} />
        ) : (
          <ComparisonView data={analysisData} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>Built with Python, TypeScript, and Claude API</p>
      </footer>
    </div>
  );
}

export default App;