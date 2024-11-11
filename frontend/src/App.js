import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import RouteUpdates from './components/RouteUpdates';
import VehicleStatusUpdate from './components/VehicleStatusUpdates';
import axios from 'axios';
import MapUpdates from './components/MapUpdates';

const App = () => {
  const [routes, setRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [creatingNewRoute, setCreatingNewRoute] = useState(false);
  const [newRoute, setNewRoute] = useState(null);
  const [mapKey, setMapKey] = useState(0);

  useEffect(() => {
    // Fetch active routes from backend
    axios.get('http://127.0.0.1:3001/api/routes')
      .then(response => {
        if (response.data.message) {
          // Handle the case when there are no active routes
          console.log(response.data.message);
        }
        setRoutes(response.data);  // Set the response data (empty array or routes)
      })
      .catch(err => console.error("Error fetching routes", err));
  }, []);

  const handleRouteSelect = (route) => {
    setSelectedRoute(route);
  };

  const handleRouteCreated = (route) => {
    setNewRoute(route); // Store the new route in state
    setCreatingNewRoute(false);  // Reset the state of route creation
  };

  const handleCreateRouteClick = () => {
    setCreatingNewRoute(!creatingNewRoute);
    // Force map re-render when toggling route creation (in place to fix map rendering issues)
    // TODO: needs work
    setMapKey(prev => prev + 1);
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header>
        <h1>Quarry Crusade: Asset Management</h1>
        <nav>
          <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
          <Link to="/route-updates" style={{ marginRight: '10px' }}>Route Updates</Link>
          <Link to="/vehicle-status" style={{ marginRight: '10px' }}>Vehicle Status</Link>
        </nav>
      </header>
      {/* add the map to the main section and add route selection */}
      <main style={{ flex: 1, overflow: 'hidden' }}>
        <Routes>
          <Route path="/" element={
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <div style={{ padding: '20px' }}>
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
                <button 
                  onClick={handleCreateRouteClick}
                  style={{ marginTop: '20px', marginRight: '10px' }}
                >
                  {creatingNewRoute ? 'Stop Creating Route' : 'Create New Route'}
                </button>
                {newRoute && (
                  <button
                    onClick={() => setNewRoute(null)}
                    style={{ marginTop: '20px' }}
                  >
                    Clear New Route
                  </button>
                )}
              </div>
              <div style={{ flex: 1 }}>
                <MapUpdates
                  key={mapKey}
                  selectedRoute={selectedRoute}
                  isEditing={creatingNewRoute}
                  onRouteCreated={handleRouteCreated}
                />
              </div>
            </div>
          } />

          <Route 
            path="/route-updates" 
            element={<RouteUpdates selectedRoute={selectedRoute} onRouteCreated={handleRouteCreated} />} 
          />
          <Route path="/vehicle-status" element={<VehicleStatusUpdate />} />
        </Routes>
      </main>

      {/* Display the newly created route if it exists */}
      {newRoute && (
        <footer>
          <h3>New Route Created</h3>
          <p>Route Name: {newRoute.route_name}</p>
          <ul>
            {newRoute.waypoints.map((wp, index) => (
              <li key={index}>Lat: {wp.lat}, Lon: {wp.lon}</li>
            ))}
          </ul>
        </footer>
      )}
    </div>
  );
};

export default App;

