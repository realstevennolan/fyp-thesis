import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './PlayersPage.css';

const PlayersPage = () => {
  const [players, setPlayers] = useState([]);
  const [search, setSearch] = useState('');
  const [positionFilter, setPositionFilter] = useState('Position');
  const [paginated, setPaginated] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: null });

  const playersPerPage = 15;

  useEffect(() => {
    const cachedData = localStorage.getItem('cachedPlayers');
    const cachedTime = localStorage.getItem('cachedPlayersTime');
    const now = new Date().getTime();

    if (cachedData && cachedTime && now - cachedTime < 10 * 60 * 1000) {
      setPlayers(JSON.parse(cachedData));
    } else {
      axios.get('http://localhost:8000/api/players/')
        .then(res => {
          setPlayers(res.data);
          localStorage.setItem('cachedPlayers', JSON.stringify(res.data));
          localStorage.setItem('cachedPlayersTime', now);
        })
        .catch(err => console.error("Players API error:", err));
    }
  }, []);

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedPlayers = [...players].sort((a, b) => {
    if (!sortConfig.key) return 0;
    const aVal = (sortConfig.key === 'name')
      ? `${a.first_name} ${a.last_name}`.toLowerCase()
      : a[sortConfig.key];
    const bVal = (sortConfig.key === 'name')
      ? `${b.first_name} ${b.last_name}`.toLowerCase()
      : b[sortConfig.key];
    if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
    return 0;
  });

  const filteredPlayers = sortedPlayers.filter(player => {
    const nameMatch = `${player.first_name} ${player.last_name}`.toLowerCase().includes(search.toLowerCase());
    const clubMatch = player.club.toLowerCase().includes(search.toLowerCase());
    const positionMatch = positionFilter === 'Position' || player.position === positionFilter;
    return (nameMatch || clubMatch) && positionMatch;
  });

  const totalPages = Math.ceil(filteredPlayers.length / playersPerPage);
  const displayedPlayers = paginated
    ? filteredPlayers.slice((currentPage - 1) * playersPerPage, currentPage * playersPerPage)
    : filteredPlayers;

  const uniquePositions = [...new Set(players.map(p => p.position))];
  const positions = ['Position', ...uniquePositions];

  const renderPagination = () => {
    const pages = [];
    const range = 1;

    const createPageButton = (pageNum) => (
      <button
        key={pageNum}
        className={currentPage === pageNum ? 'active-page' : ''}
        onClick={() => setCurrentPage(pageNum)}
      >
        {pageNum}
      </button>
    );

    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(createPageButton(i));
      }
    } else {
      pages.push(createPageButton(1));

      if (currentPage > 3) pages.push(<span key="start-ellipsis">...</span>);

      for (let i = Math.max(2, currentPage - range); i <= Math.min(totalPages - 1, currentPage + range); i++) {
        pages.push(createPageButton(i));
      }

      if (currentPage < totalPages - 2) pages.push(<span key="end-ellipsis">...</span>);

      pages.push(createPageButton(totalPages));
    }

    return <div className="pagination-controls">{pages}</div>;
  };

  return (
    <div className="players-page">
      <Navbar />
      <main className="players-main">
        <h2>Players</h2>

        <input
          type="text"
          placeholder="Search by name or club"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />

        <label htmlFor="position-filter">Filter by position:</label>
        <select
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
          className="position-filter"
        >
          {positions.map((pos, i) => (
            <option key={i} value={pos}>{pos}</option>
          ))}
        </select>

        <div className="pagination-toggle">
          <label>
            <input
              type="radio"
              value="on"
              checked={paginated}
              onChange={() => setPaginated(true)}
            />
            Pagination On
          </label>
          <label>
            <input
              type="radio"
              value="off"
              checked={!paginated}
              onChange={() => setPaginated(false)}
            />
            Pagination Off
          </label>
        </div>

        <table className="players-table">
        <thead>
  <tr>
    <th style={{ width: '20%' }} onClick={() => handleSort('name')}>Name</th>
    <th>Club</th>
    <th>Position</th>
    <th onClick={() => handleSort('age')}>Age</th>
    <th onClick={() => handleSort('height')}>Height</th>
    <th onClick={() => handleSort('weight')}>Weight</th>
  </tr>
</thead>


<tbody>
  {displayedPlayers.map((player, idx) => (
    <tr key={idx}>
      <td style={{ width: '20%' }}>
        <Link to={`/players/${player.id}`}>
          {player.first_name} {player.last_name}
        </Link>
      </td>
      <td>{player.club.replace(/^team-/, '')}</td>
      <td>{player.position}</td>
      <td>{player.age}</td>
      <td>{player.height}</td>
      <td>{player.weight}</td>
    </tr>
  ))}
</tbody>
        </table>

        {paginated && renderPagination()}
      </main>
      <Footer />
    </div>
  );
};

export default PlayersPage;