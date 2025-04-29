import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './ClubsPage.css';

const ClubsPage = () => {
  const [clubs, setClubs] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/clubs/')
      .then(res => setClubs(res.data))
      .catch(err => console.error('Clubs API error:', err));
  }, []);

  return (
    <div className="clubs-page">
      <Navbar />
      <main className="clubs-main">
        <h2>Clubs</h2>
        <div className="clubs-grid">
          {clubs.map((club, idx) => (
            <div key={idx} className="club-card">
              <Link to={`/clubs/${encodeURIComponent(club)}`}>
                {club}
              </Link>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default ClubsPage;
