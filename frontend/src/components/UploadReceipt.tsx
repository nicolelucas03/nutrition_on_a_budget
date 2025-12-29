import { useState } from 'react';
import axios from 'axios';
import { AnalysisResponse } from '../types';

interface Props {
  onAnalysisComplete: (data: AnalysisResponse) => void;
}

export default function UploadReceipt({ onAnalysisComplete }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [budget, setBudget] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    if (budget) {
      formData.append('budget', budget);
    }

    try {
      const response = await axios.post<AnalysisResponse>(
        'http://localhost:8000/api/analyze',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 120000
        }
      );
      
      if (response.data.success) {
        onAnalysisComplete(response.data);
      } else {
        alert(response.data.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to analyze receipt. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Grocery Receipt</h2>
      <p className="subtitle">We'll show you how to eat healthier for less</p>
      
      <div className="upload-area">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          id="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          {preview ? (
            <img src={preview} alt="Receipt preview" className="preview" />
          ) : (
            <div className="placeholder">
              <div className="icon">📷</div>
              <div>Click to upload a photo of your receipt</div>
            </div>
          )}
        </label>
      </div>

      <div className="budget-input">
        <label htmlFor="budget">Target Budget:</label>
        <input
          type="number"
          id="budget"
          placeholder="e.g., 50"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="analyze-btn"
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Analyzing...
          </>
        ) : (
          'Analyze Receipt'
        )}
      </button>

      {loading && (
        <div className="loading-message">
          This may take about 30-60 seconds...
        </div>
      )}
    </div>
  );
}