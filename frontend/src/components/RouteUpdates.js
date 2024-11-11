import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import axios from 'axios';

const RouteUpdates = () => {
  const [routeData, setRouteData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Connect to WebSocket server (Flask backend via Socket.IO)
    const socket = io('http://127.0.0.1:3001');

    socket.on('route_update', (data) => {
      console.log('New route update:', data);
      setRouteData(data);
    });

    socket.on('connect_error', (err) => {
      setError('Failed to connect to server');
      console.error('Socket.IO connection error:', err);
    });

    // Clean up the WebSocket connection when component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  const handleVehicleStatusUpdate = (vehicleId, statusData) => {
    axios.patch(`http://127.0.0.1:3001/api/vehicle/${vehicleId}/status`, statusData)
      .then(response => {
        console.log('Vehicle status updated');
      })
      .catch(error => {
        console.error('Failed to update vehicle status', error);
      });
  };

  return (
    <div>
      <h2>Route Updates</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {routeData ? (
        <div>
          <h3>Route Name: {routeData.route_name}</h3>
          <p>Waypoints:</p>
          <ul>
            {routeData.waypoints.map((wp, index) => (
              <li key={index}>Lat: {wp.lat}, Lon: {wp.lon}</li>
            ))}
          </ul>
          <button onClick={() => handleVehicleStatusUpdate(routeData.vehicle_id, { status: 'updated' })}>
            Update Vehicle Status
          </button>
        </div>
      ) : (
        <p>No route updates yet.</p>
      )}
    </div>
  );
};

export default RouteUpdates;
