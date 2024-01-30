import { Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet'

import 'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css'; 
import 'leaflet-extra-markers/dist/js/leaflet.extra-markers.min'; 

const createClusterMarker = (number) => {        
    const createClustersNymber = (number) => {
        if (number < 1000) {
            return number.toString();
        } else if (number < 1000000) {
            return (number / 1000).toFixed((number < 2000)? 1 : 0) + 'K';
        }else if (number < 2000000) {
            return (number / 1000).toFixed(1) + 'K';
        } else {
            return (number / 1000000).toFixed((number < 2000000)? 1 : 0) + 'M';
        }
    }
    const getColorByCount = (count) => {
        if (count < 100) {
            return 'green';
        } else if (count < 1000) {
            return 'yellow';
        } else if (count < 5000) {
            return 'orange';
        } else if (count < 20000) {
            return 'red';
        } else {
            return 'purple';
        }
    }
    return L.ExtraMarkers.icon({
        number: createClustersNymber(number),
        icon: 'fa-number',
        markerColor: getColorByCount(number),
        shape: 'square',
        prefix: 'fa',
    });
};

const ClusterMarker = ({marker}) => {
    const map = useMap();
    
    const clusterTooltipContent = `${marker.properties.markers_count}`;
    const clusterCoordinates = [
        marker.geometry.coordinates[1],
        marker.geometry.coordinates[0],
    ]
    
    return (
        <Marker key={marker.id}
            position={clusterCoordinates}
            icon={
                createClusterMarker(clusterTooltipContent, clusterCoordinates)
            }
            eventHandlers={{
                click: () => {
                map.flyTo(
                    clusterCoordinates,
                    map.getZoom() + 2,
                    { duration: 0.5 }
                );
                },
            }}
        />
    )
}

export default ClusterMarker