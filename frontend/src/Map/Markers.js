import { useState, useEffect } from 'react';
import { useStoreState } from 'easy-peasy';

import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';

const Markers = () => {
    const MARKERS_URL = '/api/v1/markers/';
    const backend = useStoreState((state) => state.backend);

    const [markers, setMarkers] = useState([]);

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

    return (
        <>
            {
                markers.map(marker => (
                    <Marker
                        key={marker.id}
                        position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]}
                    >
                        <Popup>
                            <h3>{marker.properties.name}</h3>
                        </Popup>
                    </Marker>
                ))
            }
        </>
    )
}
export default Markers