import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import './PlayerDetail.css';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const PlayerDetail = () => {
  const { id } = useParams();
  const [player, setPlayer] = useState(null);

  const [expandedSections, setExpandedSections] = useState({
    Attack: true,
    Defense: true,
    Kicking: true,
    Discipline: true,
    'Set Pieces': true, // ✅ Fixed key with space
  });

  useEffect(() => {
    axios.get(`http://localhost:8000/api/players/${id}/`)
      .then(res => setPlayer(res.data))
      .catch(err => console.error("Player Detail API error:", err));
  }, [id]);

  if (!player) return <p>Loading...</p>;

  const { first_name, last_name, position, age, height, weight, club, stats } = player;

  const calculateAverage = (keys) => {
    const total = keys.reduce((sum, key) => {
      if (stats[key]) {
        if (key === 'meters_gained'|| key === 'kick_meters') {
          return sum + stats[key] / 1; // normalize this one
        }
        return sum + stats[key];
      }
      return sum;
    }, 0);
    return (total / keys.length).toFixed(2);
  };

  const radarData = {
    labels: ['Attack', 'Defense', 'Kicking', 'Discipline', 'Set Pieces'],
    datasets: [
      {
        label: `${first_name.toUpperCase()} ${last_name.toUpperCase()} Performance`,
        data: [
          calculateAverage(['points_scored', 'tries_scored', 'offloads', 'meters_gained', 'defenders_beaten', 'clean_breaks']),
          calculateAverage(['tackles_made', 'total_tackles_missed', 'turnovers_won']),
          calculateAverage(['conversions_scored', 'drop_goals_scored', 'kicks_from_hand', 'kicks_retained', 'tries_from_kicks', 'kick_meters']),
          calculateAverage(['yellow_cards', 'red_cards', 'penalties_conceded', 'scrum_offences', 'lineout_offences']),
          calculateAverage(['lineout_won', 'lineout_steals', 'scrum_won', 'scrum_lost', 'scrum_penalties_won']),
        ],
        backgroundColor: 'rgba(0, 123, 255, 0.2)',
        borderColor: 'rgba(0, 123, 255, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(0, 123, 255, 1)',
      }
    ]
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        angleLines: { display: true },
        suggestedMin: 0,
        suggestedMax: 100,
        ticks: { stepSize: 10 }
      }
    }
  };

  const renderStatsSection = (title, keys) => (
    <div className="collapsible-section">
      <h4 onClick={() =>
        setExpandedSections(prev => ({ ...prev, [title]: !prev[title] }))
      }>
        {title} {expandedSections[title] ? '▲' : '▼'}
      </h4>
      {expandedSections[title] && (
        <ul>
          {keys.map(key => (
            stats[key] !== undefined && (
              <li key={key}><strong>{key.replace(/_/g, ' ')}:</strong> {stats[key]}</li>
            )
          ))}
        </ul>
      )}
    </div>
  );

  return (
    <div className="player-detail">
      <Navbar />
      <main className="player-detail">
        <div className="player-detail-container">
          <div className="player-info">
            <h2>{first_name} {last_name}</h2>
            <p><strong>Position:</strong> {position}</p>
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Height:</strong> {height}</p>
            <p><strong>Weight:</strong> {weight}</p>
            <p><strong>Club:</strong> {club}</p>

            <div className="collapsible-stats">
              <h3>Stats</h3>
              {renderStatsSection('Attack', ['points_scored', 'tries_scored', 'offloads', 'meters_gained', 'defenders_beaten', 'clean_breaks'])}
              {renderStatsSection('Defense', ['tackles_made', 'total_tackles_missed', 'turnovers_won'])}
              {renderStatsSection('Kicking', ['conversions_scored', 'drop_goals_scored', 'kicks_from_hand', 'kicks_retained', 'tries_from_kicks', 'kick_meters'])}
              {renderStatsSection('Discipline', ['yellow_cards', 'red_cards', 'penalties_conceded', 'scrum_offences', 'lineout_offences'])}
              {renderStatsSection('Set Pieces', ['lineout_won', 'lineout_steals', 'scrum_won', 'scrum_lost', 'scrum_penalties_won'])}
            </div>
          </div>

          <div className="radar-chart">
            <Radar data={radarData} options={radarOptions} />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default PlayerDetail;
