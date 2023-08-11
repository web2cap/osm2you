import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useStoreState } from 'easy-peasy';

import './Map.css';

function Map() {
    const [markers, setMarkers] = useState([]);
    const [userPosition, setUserPosition] = useState(null); // State to hold user's position
    const MARKERS_URL = '/api/v1/markers/';
    const backend = useStoreState((state) => state.backend);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await backend.get(MARKERS_URL);
                if (response.status !== 200) {
                    throw TypeError("Failed");
                }
                setMarkers(response.data.features);
            } catch (err) {
                console.error('Error fetching markers:', err);
            }
        }
        fetchData();
    }, []);

    // Get user's position using geolocation API
    useEffect(() => {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setUserPosition([position.coords.latitude, position.coords.longitude]);
                },
                (error) => {
                    console.error('Error getting user position:', error);
                }
            );
        } else {
            console.warn('Geolocation is not available.');
        }
    }, []);

    return (
        <div className="map-container">
            <MapContainer center={[51.505, -0.09]} zoom={7} className='MapContainer'>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                {userPosition && ( // Render user's position marker if available
                    <Marker position={userPosition}>
                        <Popup>
                            <h3>Your Position</h3>
                        </Popup>
                    </Marker>
                )}
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
