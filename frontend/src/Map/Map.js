import { MapContainer, TileLayer } from 'react-leaflet';

import LocationMarker from './LocationMarker';
import Markers from './Markers';
import './Map.css';

function Map() {
    const mapCenter = [51.505, -0.09]

    return (
        <div className="map-container">
            <MapContainer center={mapCenter} zoom={7} className='MapContainer'>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Markers />
                <LocationMarker />
            </MapContainer>
        </div>
    );
}

export default Map;
