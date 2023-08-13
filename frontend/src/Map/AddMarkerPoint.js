import { Marker, useMapEvents } from 'react-leaflet';
import { useStoreState, useStoreActions } from 'easy-peasy'

function AddMarkerPoint() {
    const addingMarkerPosition = useStoreState((state) => state.addingMarkerPosition)
    const setAddingMarkerPosition = useStoreActions((actions) => actions.setAddingMarkerPosition)

    useMapEvents({
        click: (e) => {
            setAddingMarkerPosition(e.latlng);
        },
    });

    return (
        <>{addingMarkerPosition && <Marker position={addingMarkerPosition} />}</>
    );
}

export default AddMarkerPoint;
