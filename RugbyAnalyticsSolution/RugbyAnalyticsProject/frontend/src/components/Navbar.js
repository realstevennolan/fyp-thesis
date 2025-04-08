import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Players', path: '/players' },
    { name: 'Clubs', path: '/clubs' }
  ];

  return (
    <header className="navbar-container">
      <nav className="navbar">
        {navItems.map(item => (
          <Link
            key={item.name}
            to={item.path}
            style={{
              textDecoration: location.pathname === item.path ? 'underline' : 'none'
            }}
          >
            {item.name}
          </Link>
        ))}
      </nav>
    </header>
  );
};

export default Navbar;
