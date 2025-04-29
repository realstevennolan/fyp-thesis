import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import MatchDetail from './Pages/MatchDetail';
import PlayersPage from './Pages/PlayersPage';
import PlayerDetail from './Pages/PlayerDetail';
import ClubsPage from './Pages/ClubsPage';
import ClubDetailPage from './Pages/ClubDetailPage';


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/match/:id" element={<MatchDetail />} /> 
       
        <Route path="/players" element={<PlayersPage />} />
        <Route path="/players/:id" element={<PlayerDetail />} />

        <Route path="/clubs" element={<ClubsPage />} />
        <Route path="/clubs/:clubName" element={<ClubDetailPage />} />
      </Routes>
    </Router>
  );
};

export default App;
