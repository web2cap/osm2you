import { Link } from 'react-router-dom';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import "leaflet-extra-markers";
import 'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css'; 
import "@fortawesome/fontawesome-free/css/all.css";

const RelatedMarker = ({ marker, kinds }) => {

  const findKind = (kindValue) => {
    return kinds.find((kind) => kind.kind === kindValue);
  };

  const createIcon = (kind) => {

    return L.ExtraMarkers.icon({
      icon: kind ? kind.icon : 'fa-leaf',
      iconColor: 'white',
      markerColor: kind ? kind.color : 'yellow',
      shape: 'circle',
      prefix: 'fa',
    });
  };

  const kind = findKind(marker.properties.kind);
  const icon = createIcon(kind)

  return (
    <Marker
        key={marker.id}
        position={[
           marker.geometry.coordinates[1],
           marker.geometry.coordinates[0],
        ]}
        icon={icon} 
    >
        <Popup>
          <Link to={`/markers/${marker.id}`}>
            {marker.properties.name ? <h5>{marker.properties.name}</h5> : <i>unnamed marker</i>}
          </Link>
        </Popup>
    </Marker>
  );
};

export default RelatedMarker;
