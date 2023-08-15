import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useStoreState, useStoreActions } from 'easy-peasy';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

import Missing from "../Template/Missing"

const MarkerInstance = () => {
    const { id } = useParams()

    const [errMsg, setErrMsg] = useState('')

    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)
    const backend = useStoreState((state) => state.backend);

    const setShowAddingMarker = useStoreActions((actions) => actions.setShowAddingMarker)

    const [marker, setMarker] = useState(null)

    useEffect(() => {
        setShowAddingMarker(false)
        async function fetchMarker(id) {
            const url = `${MARKERS_URL}${id}`
            try {
                const response = await backend.get(url);
                if (response.status !== 200) {
                    throw TypeError("Failed load marker");
                }
                setMarker(response.data);
            } catch (err) {
                setErrMsg(`Error fetching marker: ${err}`)
                console.error(`Error fetching marker: ${err}`);
            }
        }
        fetchMarker(id)
    }, [])

    return (
        <main>
            {errMsg ? <>
                <div className='errmsg' aria-live="assertive">{errMsg}</div>
                <Missing />
            </> :
                <div className="map-container">
                    {marker && <MapContainer center={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]} zoom={12} className='MapContainer'>
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                        <Marker position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]}>
                            <Popup>
                                {marker.properties.name}
                            </Popup>
                        </Marker>

                    </MapContainer>
                    }
                </div>
            }
        </main >
    )
}
export default MarkerInstance