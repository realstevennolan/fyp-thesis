import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import MatchDetail from './Pages/MatchDetail';
import PlayersPage from './Pages/PlayersPage';
import PlayerDetail from './Pages/PlayerDetail';
// Import your other pages when ready
// import PlayersPage from './Pages/PlayersPage';
// import ClubsPage from './Pages/ClubsPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/match/:id" element={<MatchDetail />} /> 
       
        <Route path="/players" element={<PlayersPage />} />
        <Route path="/players/:id" element={<PlayerDetail />} />

        {/* <Route path="/clubs" element={<ClubsPage />} /> */}
      </Routes>
    </Router>
  );
};

export default App;
