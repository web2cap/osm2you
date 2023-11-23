import { useParams, useNavigate, Link } from "react-router-dom"
import { MapContainer, TileLayer, } from 'react-leaflet';
import { useStoreState } from 'easy-peasy'

import LocationMarker from './LocationMarker';
import Markers from './Markers';
import Stories from "../Story/Stories";

import Missing from "../Template/Missing"
import StatusMessage from "../StatusMessage/StatusMessage";

import './MarkerUser.css';



const MarkerUser = () => {

    const { username } = useParams()
    
    const mapCenter = useStoreState((state) => state.mapCenter)
    const markers = useStoreState((state) => state.markers)
    
    const errMsg = useStoreState((state) => state.errMsg)



    
    return (
        <main>
        <StatusMessage />
        {errMsg
            ? <Missing />
            :<>
                <div className="map-container">
                    <MapContainer center={mapCenter} zoom={2} className='MapUserContainer'>
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                        <Markers backend_path={`user/${username}/`}/>
                        <LocationMarker />
                    </MapContainer>
                </div>
                <div className="UserInfo">
                    <h1 className="marker-name">{username}</h1>
                    <>
                    {markers.map(marker => (
                    <div>
                        <Link to={`/markers/${marker.id}`} className="story-marker">
                            <h3>{marker.properties.name}</h3>
                        </Link>
                        <Stories stories_list={marker.properties.stories}  />
                    </div>      
                    ))}
                    </>
                    
                </div>     
            </>
        }
        </main >
    )
}
export default MarkerUser