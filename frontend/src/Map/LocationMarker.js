import React, { useEffect, useState } from 'react';
import { Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'

const LocationMarker = () => {
    const [position, setPosition] = useState(null);
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
            // setBbox(e.bounds.toBBoxString().split(","));
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
export default LocationMarker
