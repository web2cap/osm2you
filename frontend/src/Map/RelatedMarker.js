
import { Link } from 'react-router-dom';
import { Marker, Popup } from 'react-leaflet';

const RelatedMarker = ({marker}) => {
  return (
    <Marker
        key={marker.id}
         position={[
           marker.geometry.coordinates[1],
           marker.geometry.coordinates[0],
         ]}
    >
        <Popup>
          <Link to={`/markers/${marker.id}`}>
            <h3>{marker.properties.name}</h3>
          </Link>
        </Popup>
    </Marker>
  )
}

export default RelatedMarker
