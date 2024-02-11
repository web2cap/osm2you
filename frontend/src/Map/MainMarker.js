import React, { useEffect } from 'react';
import { Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'

const MainMarker = ({marker}) => {
    const map = useMap();

    const icon = L.icon({
        iconSize: [75, 60],
        iconAnchor: [38, 60],
        popupAnchor: [0, -55],
        iconUrl: "/img/marker/red_marker.svg",
    })
    useEffect(() => {
        map.setView([marker.geometry.coordinates[1], marker.geometry.coordinates[0]],12);
    }, [marker, map]);

    return (
        <Marker position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]} icon={icon}>
            <Popup>
                {marker.properties.name}
            </Popup>
        </Marker>
    )
}

export default MainMarker
