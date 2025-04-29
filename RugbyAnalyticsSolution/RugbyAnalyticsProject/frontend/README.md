
# Rugby Analytics Platform

## Overview
This project is a full-stack **rugby analytics platform** that collects, processes, and visualizes rugby match and player data. It allows users to explore detailed player profiles, team statistics, fixtures, and results through an interactive web interface.

The platform is built with:
- **Django** (backend / REST API)
- **React.js** (frontend)
- **SQLite** (database for local development)
- **Chart.js** (for interactive data visualization)

It was developed as part of a Final Year Project (FYP) focused on expanding analytics capabilities in rugby, an area often underserved compared to other major sports.

## Features

- **Player Profiles**: View player details, clubs, and physical stats.
- **Team Pages**: Explore club rosters, team statistics, and recent match results.
- **Data Visualizations**: Doughnut charts for turnovers, tackles, lineouts, and scrums.
- **Fixture and Result Listings**: Match information is organized by upcoming fixtures and past results.
- **Search and Filter**: Search players or filter by position.
- **API-Driven**: Data delivered dynamically from Django REST Framework endpoints.
- **Ethical Data Collection**: Designed with respect for scraping ethics and data integrity.

## Technologies Used

| Area          | Technology          |
|---------------|----------------------|
| Backend       | Python, Django REST Framework |
| Frontend      | React.js, Chart.js    |
| Database      | SQLite (development)  |
| Deployment    | Localhost (development) |
| Visualization | Chart.js Doughnut charts |
| Testing       | Django's Test Framework (unittest) |

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/rugby-analytics-platform.git
cd rugby-analytics-platform

cd RugbyAnalyticsProject
python -m venv venv
venv\\Scripts\\activate      # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

Backend will run at: http://localhost:8000/

3. Frontend Setup (React)

cd frontend
npm install
npm start


| Endpoint                                | Description                                  |
|-----------------------------------------|----------------------------------------------|
| /api/fixtures/                          | Get upcoming fixtures                       |
| /api/fixtures/all/                      | Get all fixtures                            |
| /api/fixtures/<id>/                     | Get fixture details by ID                   |
| /api/standings/                         | Get league standings                        |
| /api/players/                           | Get players list (with optional search query)|
| /api/players/<id>/                      | Get player details by ID                    |
| /api/clubs/                             | Get list of clubs                           |
| /api/clubs/<club_name>/                 | Get players of a specific club              |
| /api/clubs/<club_name>/standing/        | Get standing of a specific club             |
| /api/clubs/<club_name>/stats/           | Get stats for a specific club               |
| /api/clubs/<club_name>/matches/         | Get upcoming matches for a specific club    |
| /api/teamstats/by-name/<club_name>/     | Get team match stats for a specific club name|
