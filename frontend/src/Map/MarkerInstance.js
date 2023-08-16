import { useEffect, useState } from "react"
import { Link, useParams, useNavigate } from "react-router-dom"
import { useStoreState, useStoreActions } from 'easy-peasy';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

import Missing from "../Template/Missing"
import './MarkerInstance.css'

const MarkerInstance = () => {
    const { id } = useParams()

    const [errMsg, setErrMsg] = useState('')
    const [errMissing, setErrMissing] = useState(false)

    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)
    const backend = useStoreState((state) => state.backend);

    const setShowAddingMarker = useStoreActions((actions) => actions.setShowAddingMarker)

    const [marker, setMarker] = useState(null)

    const navigate = useNavigate()

    // fetch marker
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
                setErrMissing(true)
                console.error(`Error fetching marker: ${err}`);
            }
        }
        fetchMarker(id)
    }, [])

    //delete
    const handleDelete = async () => {
        setErrMsg('');
        try {
            const response = await backend.delete(`${MARKERS_URL}${id}`,
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 204) {
                throw TypeError("Deletion filed")
            }
            navigate('/')
        } catch (err) {
            console.log(err)
            setErrMsg(err?.response?.data?.detail
                ? err.response.data.detail
                : "Deletion filed"
            )
        }
    }

    return (
        <main>
            {errMsg && <div className='errmsg' aria-live="assertive">{errMsg}</div>}
            {errMissing
                ? <Missing />
                : marker && <div>
                    <div className="map-container">
                        <MapContainer center={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]} zoom={12} className='MapInstanceContainer'>
                            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                            <Marker position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]}>
                                <Popup>
                                    {marker.properties.name}
                                </Popup>
                            </Marker>

                        </MapContainer>

                    </div>
                    <div className="MarkerInfo">
                        <h1 className="marker-name">{marker.properties.name}</h1>
                        <div className="button-group">
                            <button>Edit</button>
                            <button onClick={handleDelete} className="delete">Delete</button>
                            <button className="add">Add story</button>
                        </div>
                        <p className="description"></p>
                        <ul className="related-markers">
                            {/* marker.relatedMarkers.map(relatedMarker => (
                                <li key={relatedMarker.id}>
                                    <Link to={`/marker/${relatedMarker.id}`} className="related-marker-link">{relatedMarker.name}</Link>
                                </li>
                            )) */}
                        </ul>
                    </div>
                </div>
            }
        </main >
    )
}
export default MarkerInstance