import React, { useState } from 'react';
import MapUpdates from './MapUpdates';

const RouteUpdates = ({ selectedRoute, onRouteCreated }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleRouteCreated = (newRoute) => {
    onRouteCreated(newRoute);
    setIsEditing(false);
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2>Route Updates</h2>
        <button 
          onClick={() => setIsEditing(!isEditing)}
          style={{ marginBottom: '10px' }}
        >
          {isEditing ? 'Cancel Editing' : 'Create/Edit Route'}
        </button>
      </div>

      <MapUpdates 
        selectedRoute={selectedRoute}
        isEditing={isEditing}
        onRouteCreated={handleRouteCreated}
      />

      {selectedRoute && !isEditing && (
        <div style={{ marginTop: '20px' }}>
          <h3>Current Route: {selectedRoute.route_name}</h3>
          <p>Waypoints:</p>
          <ul>
            {selectedRoute.waypoints.map((wp, index) => (
              <li key={index}>Lat: {wp.lat}, Lon: {wp.lon}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RouteUpdates;
