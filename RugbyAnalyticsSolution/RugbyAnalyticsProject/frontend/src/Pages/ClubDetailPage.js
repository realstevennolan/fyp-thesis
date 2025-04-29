import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './ClubDetailPage.css';

import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const tabs = ['Overview', 'Players', 'Stats'];

const ClubDetailPage = () => {
  const { clubName } = useParams();
  const [activeTab, setActiveTab] = useState('Overview');
  const [players, setPlayers] = useState([]);
  const [stats, setStats] = useState([]);
  const [fixtures, setFixtures] = useState({ upcoming: [], results: [] });

  useEffect(() => {
    axios.get(`http://localhost:8000/api/clubs/${clubName}/fixtures/`)
      .then(res => setFixtures(res.data))
      .catch(err => console.error("Error fetching fixtures/results", err));
  }, [clubName]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/players/?q=${clubName}`)
      .then(res => setPlayers(res.data))
      .catch(err => console.error("Error fetching players", err));
  }, [clubName]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/teamstats/by-name/${clubName}`)
      .then(res => setStats(res.data))
      .catch(err => console.error("Error fetching team stats", err));
  }, [clubName]);

  const filteredStats = stats.length > 0
    ? Object.entries(stats[0]).filter(([key]) => key !== 'id' && key !== 'team')
    : [];

  const getStatValue = (key) => stats.length > 0 ? stats[0][key] : 0;

  const tacklesData = {
    labels: ['Tackles Made', 'Tackles Missed'],
    datasets: [{
      data: [getStatValue('tackles_made'), getStatValue('total_tackles_missed')],
      backgroundColor: ['#1b9e77', '#d95f02'],
    }]
  };

  const turnoversData = {
    labels: ['Turnovers Won', 'Turnovers Lost'],
    datasets: [{
      data: [getStatValue('turnovers_won'), getStatValue('turnovers_lost')],
      backgroundColor: ['#7570b3', '#e7298a'],
    }]
  };

  const lineoutsData = {
    labels: ['Lineouts Won', 'Lineouts Lost'],
    datasets: [{
      data: [getStatValue('lineouts_won'), getStatValue('lineouts_lost')],
      backgroundColor: ['#66c2a5', '#fc8d62'],
    }]
  };

  const scrumsData = {
    labels: ['Scrums Won', 'Scrums Lost'],
    datasets: [{
      data: [getStatValue('scrums_won'), getStatValue('scrums_lost')],
      backgroundColor: ['#8da0cb', '#e78ac3'],
    }]
  };

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

              <div className="fixtures-section">
                <h3>Upcoming Fixtures</h3>
                {fixtures.upcoming.length === 0 ? (
                  <p>No upcoming matches.</p>
                ) : (
                  <ul>
                    {fixtures.upcoming.map(match => (
                      <li key={match.id}>
                        <Link to={`/match/${match.id}`}>
                          {match.date} - {match.home_team} vs {match.away_team}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}

                <h3>Recent Results</h3>
                {fixtures.results.length === 0 ? (
                  <p>No recent results.</p>
                ) : (
                  <ul>
                    {fixtures.results.map(match => (
                      <li key={match.id}>
                        <Link to={`/match/${match.id}`}>
                          {match.date} - {match.home_team} {match.home_score} : {match.away_score} {match.away_team}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
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

          {activeTab === 'Stats' && (
            <div className="stats-section">
              {filteredStats.length === 0 ? (
                <p>No statistics available.</p>
              ) : (
                <>
                  <div className="stat-list">
                    {filteredStats.map(([key, value]) => (
                      <div className="stat-row" key={key}>
                        <span className="stat-key">{key.replace(/_/g, ' ')}:</span>
                        <span className="stat-value">{value}</span>
                      </div>
                    ))}
                  </div>

                  <div className="charts-grid">
                    <div className="chart-box">
                      <h4>Tackles</h4>
                      <Doughnut data={tacklesData} />
                    </div>
                    <div className="chart-box">
                      <h4>Turnovers</h4>
                      <Doughnut data={turnoversData} />
                    </div>
                    <div className="chart-box">
                      <h4>Lineouts</h4>
                      <Doughnut data={lineoutsData} />
                    </div>
                    <div className="chart-box">
                      <h4>Scrums</h4>
                      <Doughnut data={scrumsData} />
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default ClubDetailPage;
