import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './MatchDetail.css';  // Your custom CSS (create as needed)

const MatchDetail = () => {
  const { id } = useParams();
  const [match, setMatch] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/fixtures/${id}/`)
      .then(res => setMatch(res.data))
      .catch(err => console.error("Match Detail API error:", err));
  }, [id]);

  if (!match) return <div>Loading match details...</div>;

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content">
        <div className="section">
          <h2>Match Details</h2>
          <p><strong>Date:</strong> {match.date}</p>
          <p><strong>Home Team:</strong> {match.home_team}</p>
          <p><strong>Away Team:</strong> {match.away_team}</p>
          <p><strong>Home Score:</strong> {match.home_score}</p>
          <p><strong>Away Score:</strong> {match.away_score}</p>
          <p><strong>Stadium:</strong> {match.stadium}</p>
          <p><strong>City:</strong> {match.city}</p>
          <p><strong>Country:</strong> {match.country}</p>
          <p><strong>Referee:</strong> {match.referee}</p>
          <Link to="/" style={{ color: 'blue' }}>← Back to Home</Link>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default MatchDetail;
