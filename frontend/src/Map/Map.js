import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

import './Map.css'

function Map() {
    const [markers, setMarkers] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/v1/markers/')
            .then(response => response.json())
            .then(data => {
                setMarkers(data.features);
            })
            .catch(error => {
                console.error('Error fetching markers:', error);
            });
    }, []);

    return (
        <div className="map-container">
            <MapContainer center={[51.505, -0.09]} zoom={13} className='MapContainer'>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                {markers.map(marker => (
                    <Marker
                        key={marker.id}
                        position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]}
                    >
                        <Popup>
                            <h3>{marker.properties.name}</h3>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
}

export default Map;
