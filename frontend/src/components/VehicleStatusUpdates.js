import React, { useState } from 'react';
import axios from 'axios';

const VehicleStatusUpdate = () => {
  const [vehicleId, setVehicleId] = useState('');
  const [status, setStatus] = useState('');

  const updateVehicleStatus = (vehicleId, statusData) => {
    axios.patch(`http://127.0.0.1:3001/api/vehicle/${vehicleId}/status`, statusData)
      .then(response => {
        console.log('Vehicle status updated');
      })
      .catch(error => {
        console.error('Failed to update vehicle status', error);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const statusData = { status };
    updateVehicleStatus(vehicleId, statusData);
  };

  return (
    <div>
      <h2>Update Vehicle Status</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Vehicle ID: </label>
          <input
            type="text"
            value={vehicleId}
            onChange={(e) => setVehicleId(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Status: </label>
          <input
            type="text" // TODO: this status needs to be updated from DDS, position, etc.
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          />
        </div>
        <button type="submit">Update Status</button>
      </form>
    </div>
  );
};

export default VehicleStatusUpdate;

