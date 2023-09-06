import { MapContainer, TileLayer, } from 'react-leaflet';
import { useStoreState } from 'easy-peasy'

import LocationMarker from './LocationMarker';
import Markers from './Markers';
import AddMarkerPoint from './AddMarkerPoint';
import './Map.css';

function Map() {

    const mapCenter = useStoreState((state) => state.mapCenter)
    const showAddingMarker = useStoreState((state) => state.showAddingMarker)
    const addingMarker = useStoreState((state) => state.addingMarker)

    return (
        <div className="map-container">
            <MapContainer center={mapCenter} zoom={7} className='MapContainer'>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Markers />
                <LocationMarker />
                {showAddingMarker && addingMarker && <AddMarkerPoint />}
            </MapContainer>
        </div>
    );
}

export default Map;
