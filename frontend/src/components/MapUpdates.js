import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet-draw';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';

// MapContent component to handle map interactions
const MapContent = ({ selectedRoute, isEditing, onRouteCreated, showDrawnRoute }) => {
  const map = useMap();
  const [drawControl, setDrawControl] = useState(null);
  const [polylines, setPolylines] = useState([]);
  const [drawnRoute, setDrawnRoute] = useState(null);

  // Clear existing polylines
  const clearPolylines = () => {
    polylines.forEach(polyline => polyline.remove());
    setPolylines([]);
  };

  // Add a new polyline to the map
  const addPolyline = (coordinates, color = 'red') => {
    const polyline = L.polyline(coordinates, { color }).addTo(map);
    setPolylines(prev => [...prev, polyline]);
    map.fitBounds(polyline.getBounds());
    return polyline;
  };

  // Initialize draw control
  useEffect(() => {
    if (isEditing && !drawControl) {
      try {
        const drawnItems = new L.FeatureGroup().addTo(map);
        
        const control = new L.Control.Draw({
          draw: {
            polyline: true,
            polygon: false,
            circle: false,
            rectangle: false,
            marker: false,
            circlemarker: false
          },
          edit: {
            featureGroup: drawnItems
          }
        });

        map.addControl(control);
        setDrawControl(control);

        const handleDrawCreated = (e) => {
          const layer = e.layer;
          
          // Clear previous drawn route if exists
          if (drawnRoute) {
            drawnRoute.remove();
          }
          
          // Add the new route to the map
          layer.addTo(map);
          setDrawnRoute(layer);
          
          const coordinates = layer.getLatLngs().map(latlng => ({
            lat: latlng.lat,
            lon: latlng.lng,
          }));

          onRouteCreated({
            route_name: 'New Route',
            waypoints: coordinates,
          });
        };

        map.on(L.Draw.Event.CREATED, handleDrawCreated);

        return () => {
          map.removeControl(control);
          map.off(L.Draw.Event.CREATED, handleDrawCreated);
          if (drawnRoute) {
            drawnRoute.remove();
          }
        };
      } catch (error) {
        console.error('Error initializing draw control:', error);
      }
    }
  }, [map, isEditing, onRouteCreated]);

  // Handle selected route display
  useEffect(() => {
    clearPolylines();
    
    if (selectedRoute?.waypoints) {
      const coordinates = selectedRoute.waypoints.map(wp => [wp.lat, wp.lon]);
      addPolyline(coordinates);
    }

    return () => clearPolylines();
  }, [selectedRoute]);

  return null;
};

const MapUpdates = ({ selectedRoute, isEditing, onRouteCreated }) => {
  const [showDrawnRoute, setShowDrawnRoute] = useState(true);

  return (
    <div style={{ height: '700px', width: '100%', position: 'relative', zIndex: 0 }}>
      <MapContainer
        center={[40.604431, -89.488347]}
        zoom={13}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapContent 
          selectedRoute={selectedRoute}
          isEditing={isEditing}
          onRouteCreated={onRouteCreated}
          showDrawnRoute={showDrawnRoute}
        />
      </MapContainer>
      <button
        onClick={() => setShowDrawnRoute(false)}
        style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          zIndex: 1000
        }}
      >
        Clear Drawn Route
      </button>
    </div>
  );
};

export default MapUpdates;
