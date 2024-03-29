import { Marker, Popup } from 'react-leaflet';
import { Link } from 'react-router-dom';

const PointMarker = ({marker}) => {
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
            <h4>{marker.properties.name ? marker.properties.name : <i>unnamed marker</i>}</h4>
          </Link>
        </Popup>
    </Marker>
  )
}

export default PointMarker
