import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './HomePage.css'; 

const HomePage = () => {
  const [news, setNews] = useState([]);
  const [fixtures, setFixtures] = useState([]);
  const [standings, setStandings] = useState([]);
  const [fixtureView, setFixtureView] = useState('upcoming');  // Default: upcoming

  // Fetch news and standings on load
  useEffect(() => {
    axios.get(`https://newsapi.org/v2/everything?q=rugby+URC&apiKey=5a004098442c483ebae9301e55914921`)
      .then(res => setNews(res.data.articles.slice(0, 10)))  // Limit to 10 articles
      .catch(err => console.error("News API error:", err));
  
    axios.get('http://localhost:8000/api/standings/')
      .then(res => setStandings(res.data))
      .catch(err => console.error("Standings API error:", err));
  }, []);
  

  // Fetch fixtures when dropdown changes
  useEffect(() => {
    const endpoint = fixtureView === 'upcoming'
      ? 'http://localhost:8000/api/fixtures/'
      : 'http://localhost:8000/api/fixtures/all/';

    axios.get(endpoint)
      .then(res => setFixtures(res.data))
      .catch(err => console.error("Fixtures API error:", err));
  }, [fixtureView]);

  return (
    <div className="page-container">
      <Navbar />
      <main className="main-content">
        {/* Rugby News */}
        <div className="section">
          <h2>Rugby News</h2>
          {news.map((item, idx) => (
            <div key={idx} className="news-item">
              <a href={item.url} target="_blank" rel="noopener noreferrer">
                {item.title}
              </a>
            </div>
          ))}
        </div>

        {/* Fixtures with Dropdown */}
        <div className="section">
          <h2>Fixtures</h2>
          <select
            value={fixtureView}
            onChange={(e) => setFixtureView(e.target.value)}
            className="dropdown"
          >
            <option value="upcoming">Upcoming</option>
            <option value="all">All</option>
          </select>

          {fixtures.map((match, idx) => (
            <div key={idx} className="fixture-item">
              <Link to={`/match/${match.id}`} className="fixture-link">
                <p>{match.date} - <strong>{match.home_team}</strong> vs <strong>{match.away_team}</strong></p>
              </Link>
            </div>
          ))}
        </div>

        {/* Table Standings */}
        <div className="section">
          <h2>Table Standings</h2>
          <table className="standings-table">
            <thead>
              <tr>
                <th>Team</th>
                <th>Pts</th>
              </tr>
            </thead>
            <tbody>
              {standings.map((team, idx) => (
                <tr key={idx}>
                  <td>{team.team_name}</td>
                  <td>{team.points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default HomePage;
