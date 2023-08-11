import { useState, useEffect, useRef } from 'react';
import { useStoreState } from 'easy-peasy';

import { Marker, Popup, useMap } from 'react-leaflet';

const Markers = () => {
    const MARKERS_URL = '/api/v1/markers/';
    const DEBOUNCE_DELAY = 300
    const backend = useStoreState((state) => state.backend);

    const [markers, setMarkers] = useState([]);
    const [bbox, setBbox] = useState(null)

    const isFirstCallRef = useRef(true);
    const debounceTimerRef = useRef(null);

    const map = useMap();

    // fetch markers
    useEffect(() => {
        async function fetchData() {
            const url = bbox ? `${MARKERS_URL}?in_bbox=${bbox}` : MARKERS_URL
            try {
                const response = await backend.get(url);
                if (response.status !== 200) {
                    throw TypeError("Failed");
                }
                setMarkers(response.data.features);
            } catch (err) {
                console.error('Error fetching markers:', err);
            }
        }
        fetchData();
    }, [bbox, backend]);


    // set bbox
    const handleMapChange = () => {
        if (isFirstCallRef.current) {
            isFirstCallRef.current = false;
            callLogic();
            debounceSubsequentCalls();
        } else {
            clearTimeout(debounceTimerRef.current);
            debounceSubsequentCalls();
        }
    };

    const debounceSubsequentCalls = () => {
        debounceTimerRef.current = setTimeout(() => {
            callLogic();
            clearTimeout(debounceTimerRef.current);
        }, DEBOUNCE_DELAY);
    };

    const callLogic = () => {
        const bounds = map.getBounds();
        const bbox = bounds.toBBoxString();
        setBbox(bbox)
        console.log('Map bbox', bbox);
    };

    useEffect(() => {
        map.on('move', handleMapChange);
        map.on('zoom', handleMapChange);

        return () => {
            map.off('move', handleMapChange);
            map.off('zoom', handleMapChange);
            clearTimeout(debounceTimerRef.current);
        };
    }, [map]);


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