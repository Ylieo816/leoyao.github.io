import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './InfringementCheck.css'; // Import CSS

function InfringementCheck() {
  // State variables
  const [patentId, setPatentId] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisCount, setAnalysisCount] = useState(0);
  const [analysisDate, setAnalysisDate] = useState('');

  // Load analysis count from local storage on component mount
  useEffect(() => {
    const storedCount = localStorage.getItem('analysisCount');
    if (storedCount) {
      setAnalysisCount(parseInt(storedCount, 10));
    }
  }, []);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    
    try {
      setLoading(true);
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/check-infringement`, {
        patent_id: patentId,
        company_name: companyName,
      });
      
      setResult(response.data.infringing_products);
      const newCount = analysisCount + 1;
      setAnalysisCount(newCount);
      localStorage.setItem('analysisCount', newCount.toString());
      setAnalysisDate(new Date().toLocaleString());
    } catch (error) {
      setError('An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="infringement-check-container">
      <h1 className="title">Patent Infringement Check</h1>
      <form onSubmit={handleSubmit} className="form">
        <div className="input-group">
          <input 
            value={patentId} 
            onChange={(e) => setPatentId(e.target.value)} 
            placeholder="Patent ID" 
            required 
            className="input"
          />
        </div>
        <br />
        <div className="input-group">
          <input 
            value={companyName} 
            onChange={(e) => setCompanyName(e.target.value)} 
            placeholder="Company Name" 
            required 
            className="input"
          />
        </div>
        <button type="submit" className="button">Check Infringement</button>
      </form>
      
      {loading && <div className="loader">Loading...</div>}
      
      {error && <p className="error">{error}</p>}
      
      {result && (
        <div className="results">
          <h2 className="subtitle">Infringement Analysis</h2>
          <div className="analysis-info">
            <p>Analysis Count: <span className="highlight">{analysisCount}</span></p>
            <p>Company: <span className="highlight">{companyName}</span></p>
            <p>Patent ID: <span className="highlight">{patentId}</span></p>
            <p>Analysis Date: <span className="highlight">{analysisDate}</span></p>
          </div>
          {result.map((item, index) => (
            <div key={index} className="result-item">
              <h3 className="product-name">{item.product_name}</h3>
              <p><strong>Infringement Likelihood:</strong> <span className={`likelihood ${item.infringement_likelihood.toLowerCase()}`}>{item.infringement_likelihood}</span></p>
              <p><strong>Relevant Claims:</strong> {item.relevant_claims.join(', ')}</p>
              <p><strong>Explanation:</strong> {item.explanation}</p>
            </div>
          ))}
        </div>
      )}
      
      {result && result.length === 0 && (
        <p className="no-results">No infringing products found.</p>
      )}
    </div>
  );
}

export default InfringementCheck;