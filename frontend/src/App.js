import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import RouteUpdates from './components/RouteUpdates';
import VehicleStatusUpdate from './components/VehicleStatusUpdates';
import axios from 'axios';

const App = () => {
  const [routes, setRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);

  useEffect(() => {
    // Fetch active routes from backend
    axios.get('http://127.0.0.1:3001/api/routes')
      .then(response => {
        if (response.data.message) {
          // Handle the case when there are no active routes
          console.log(response.data.message);  // Log the message
        }
        setRoutes(response.data);  // Set the response data (empty array or routes)
      })
      .catch(err => console.error("Error fetching routes", err));
  }, []);

  const handleRouteSelect = (route) => {
    setSelectedRoute(route);
  };

  return (
    <div>
      <h1>Asset Management</h1>
      <nav>
        <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
        <Link to="/route-updates" style={{ marginRight: '10px' }}>Route Updates</Link>
        <Link to="/vehicle-status" style={{ marginRight: '10px' }}>Vehicle Status</Link>
      </nav>
      <Routes>
        <Route path="/" element={
          <div>
            <h2>Select a Route</h2>
            {routes.length > 0 ? (
              <ul>
                {routes.map((route, index) => (
                  <li key={index} onClick={() => handleRouteSelect(route)}>
                    {route.route_name}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No active routes available.</p> 
            )}
            {selectedRoute && (
              <div>
                <h3>Selected Route: {selectedRoute.route_name}</h3>
                <p>Waypoints:</p>
                <ul>
                  {selectedRoute.waypoints.map((wp, index) => (
                    <li key={index}>Lat: {wp.lat}, Lon: {wp.lon}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        } />
        <Route path="/route-updates" element={<RouteUpdates />} />
        <Route path="/vehicle-status" element={<VehicleStatusUpdate />} />
      </Routes>
    </div>
  );
};

export default App;
