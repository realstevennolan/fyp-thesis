import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './ClubDetailPage.css';

const tabs = ['Overview', 'Players', 'Stats'];

const ClubDetailPage = () => {
  const { clubName } = useParams();
  const [activeTab, setActiveTab] = useState('Overview');
  const [players, setPlayers] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const normalizedClub = clubName.toLowerCase().replace(/-/g, ' ');

    axios.get(`http://localhost:8000/api/players/?q=${normalizedClub}`)
      .then(res => setPlayers(res.data))
      .catch(err => console.error("Error fetching players", err));

    axios.get(`http://localhost:8000/api/clubs/${clubName}/stats/`)
      .then(res => setStats(res.data))
      .catch(err => console.error("Error fetching club stats", err));
  }, [clubName]);

  return (
    <div className="club-detail">
      <Navbar />
      <main>
        <h2>{clubName.toUpperCase()}</h2>

        <div className="tab-buttons">
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={activeTab === tab ? 'active' : ''}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="tab-content">
          {activeTab === 'Overview' && (
            <div>
              <p><strong>Founded:</strong> (placeholder year)</p>
              <p><strong>Country:</strong> (placeholder)</p>
            </div>
          )}

          {activeTab === 'Players' && (
            <div className="players-grid">
              {players.map(player => (
                <Link key={player.id} to={`/players/${player.id}`} className="player-box">
                  <h4>{player.first_name} {player.last_name}</h4>
                  <p>{player.position}</p>
                </Link>
              ))}
            </div>
          )}

          {activeTab === 'Stats' && stats && (
            <div className="stats-section">
              {Object.entries(stats[0] || {}).map(([key, value]) => (
                <div className="stat-row" key={key}>
                  <span className="stat-key">{key.replace(/_/g, ' ').toUpperCase()}:</span>
                  <span className="stat-value">{value}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default ClubDetailPage;
