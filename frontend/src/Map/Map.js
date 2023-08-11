import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'
import { useStoreState } from 'easy-peasy';

import './Map.css';

function Map() {
    const MARKERS_URL = '/api/v1/markers/';
    const backend = useStoreState((state) => state.backend);


    const [markers, setMarkers] = useState([]);
    const mapCenter = [51.505, -0.09]

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


    function LocationMarker() {
        const [position, setPosition] = useState(null);
        const [bbox, setBbox] = useState([]);

        const map = useMap();

        const icon = L.icon({
            iconSize: [50, 41],
            iconAnchor: [10, 41],
            popupAnchor: [2, -40],
            iconUrl: "/img/marker/flag.svg",
            shadowUrl: "https://unpkg.com/leaflet@1.6/dist/images/marker-shadow.png"
        })

        useEffect(() => {
            map.locate().on("locationfound", function (e) {
                setPosition(e.latlng);
                map.flyTo(e.latlng, map.getZoom());
                // const radius = e.accuracy;
                // const circle = L.circle(e.latlng, radius);
                //circle.addTo(map);
                setBbox(e.bounds.toBBoxString().split(","));
            });
        }, [map]);

        return position === null ? null : (
            <Marker position={position} icon={icon}>
                <Popup>
                    Your position.
                </Popup>
            </Marker>
        );
    }
    return (
        <div className="map-container">
            <MapContainer center={mapCenter} zoom={7} className='MapContainer'>
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
                <LocationMarker />
            </MapContainer>
        </div>
    );
}

export default Map;
