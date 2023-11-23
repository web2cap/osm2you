import { useParams, useNavigate } from "react-router-dom"
import { MapContainer, TileLayer, } from 'react-leaflet';
import { useStoreState } from 'easy-peasy'

import LocationMarker from './LocationMarker';
import Markers from './Markers';
import './Map.css';



const MarkerUser = () => {

    const mapCenter = useStoreState((state) => state.mapCenter)
    const navigate = useNavigate()
    const { username } = useParams()

    
    return (
        <main>
            <div className="map-container">
            <MapContainer center={mapCenter} zoom={7} className='MapContainer'>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Markers backend_path={`user/${username}/`}/>
                <LocationMarker />
            </MapContainer>
        </div>
                    
           
        </main >
    )
}
export default MarkerUser