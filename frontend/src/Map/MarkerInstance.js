import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useStoreState, useStoreActions } from 'easy-peasy';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

import Missing from "../Template/Missing"
import './MarkerInstance.css'
import AddMarkerPoint from './AddMarkerPoint';

const MarkerInstance = () => {
    const { id } = useParams()

    const [errMsg, setErrMsg] = useState('')
    const [errMissing, setErrMissing] = useState(false)

    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)
    const backend = useStoreState((state) => state.backend);

    const addingMarkerPosition = useStoreState((state) => state.addingMarkerPosition)
    const setAddingMarkerPosition = useStoreActions((actions) => actions.setAddingMarkerPosition)

    const [marker, setMarker] = useState(null)

    const [editMode, setEditMode] = useState(false)
    const [editName, setEditName] = useState('')


    const navigate = useNavigate()

    // fetch marker
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

    useEffect(() => {
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

    //edit
    const handleEditMode = () => {
        setErrMsg('');
        setEditMode(true)
        setEditName(marker.properties.name)
        setAddingMarkerPosition({
            lat: marker.geometry.coordinates[1],
            lng: marker.geometry.coordinates[0]
        })
    }

    const handleEdit = async () => {
        if (!addingMarkerPosition || !editName) {
            setErrMsg("Invalid Point");
            return
        }
        setErrMsg('')
        const newMarker = {
            name: editName,
            location: {
                type: "Point",
                coordinates: [addingMarkerPosition.lng, addingMarkerPosition.lat],
            }
        };
        try {
            const response = await backend.patch(`${MARKERS_URL}${id}/`,
                JSON.stringify(newMarker),
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 200) {
                throw TypeError("Edit Failed")
            }
        } catch (err) {
            setErrMsg(`${err.message} ${err?.response?.data?.detail ? err.response.data.detail : ''}`)
            console.log(err)
        }

        setAddingMarkerPosition(null);
        setEditName(null)
        fetchMarker(id)
        setEditMode(false)
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

                            {editMode
                                ? <AddMarkerPoint />
                                : <Marker position={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]}>
                                    <Popup>
                                        {marker.properties.name}
                                    </Popup>
                                </Marker>
                            }

                        </MapContainer>

                    </div>
                    <div className="MarkerInfo">

                        {editMode
                            ? <>
                                <input
                                    type="text"
                                    value={editName}
                                    onChange={(e) => setEditName(e.target.value)}
                                    required
                                />
                                <div className="button-group">
                                    <button onClick={handleEdit}>Save</button>
                                    <button
                                        onClick={() => {
                                            setEditMode(false)
                                            setEditName(marker.properties.name)
                                        }}
                                        className="cancel"
                                    >Cancel</button>
                                </div>
                            </>
                            : <>
                                <h1 className="marker-name">{marker.properties.name}</h1>
                                <div className="button-group">
                                    <button
                                        onClick={handleEditMode}
                                    >Edit</button>
                                    <button onClick={handleDelete} className="delete">Delete</button>
                                    <button className="add">Add story</button>
                                </div>
                            </>
                        }
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