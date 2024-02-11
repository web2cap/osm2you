import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useStoreState, useStoreActions } from 'easy-peasy';
import { MapContainer, TileLayer } from 'react-leaflet';

import Missing from "../Template/Missing"
import './MarkerInstance.css'
import AddMarkerPoint from './AddMarkerPoint';
import AddStory from "../Story/AddStory";
import Stories from "../Story/Stories";
import StatusMessage from "../StatusMessage/StatusMessage";
import FormatDate from "../common/FormatDate";
import MainMarker from "./MainMarker";
import RelatedMarkers from "./RelatedMarkers";

const MarkerInstance = () => {
    const { id } = useParams()

    const [errMissing, setErrMissing] = useState(false)

    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)
    const KINDS_URL = useStoreState((state) => state.KINDS_URL)
    const backend = useStoreState((state) => state.backend);

    const setErrMsg = useStoreActions((actions) => actions.setErrMsg)

    const addingMarkerPosition = useStoreState((state) => state.addingMarkerPosition)
    const setAddingMarkerPosition = useStoreActions((actions) => actions.setAddingMarkerPosition)


    const addingStory = useStoreState((state) => state.addingStory)
    const setAddingStory = useStoreActions((actions) => actions.setAddingStory)

    const editingStory = useStoreState((state) => state.editingStory)

    const marker = useStoreState((state) => state.marker)
    const setMarker = useStoreActions((actions) => actions.setMarker)
    
    const markerUpdated = useStoreState((state) => state.markerUpdated)
    const setMarkerUpdated = useStoreActions((actions) => actions.setMarkerUpdated)

    const [editMode, setEditMode] = useState(false)
    const [editName, setEditName] = useState('')

    const [kinds, setKinds] = useState([]);

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
        setErrMsg('')
        fetchMarker(id)
    }, [id])
    useEffect(() => {
        if (markerUpdated){
            fetchMarker(id)
            setMarkerUpdated(false)
        }
    }, [markerUpdated])

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
        }

        setAddingMarkerPosition(null);
        setEditName(null)
        fetchMarker(id)
        setEditMode(false)
    }
    // fetch kinds
    useEffect(() => {
        async function fetchKinds() {
            try {
                const response = await backend.get(KINDS_URL);
                if (response.status !== 200) {
                    throw new Error("Failed to fetch kinds");
                }
                setKinds(response.data);
            } catch (err) {
                setErrMsg(`Error fetching kinds: ${err}`)
                setErrMissing(true)
                console.error("Error fetching kinds:", err);
            }
        }
    
        fetchKinds();
    }, []);
    return (
        <main>
            <StatusMessage />
            {errMissing
                ? <Missing />
                : marker && <div>
                    <div className="map-container">
                        <MapContainer center={[marker.geometry.coordinates[1], marker.geometry.coordinates[0]]} zoom={12} className='MapInstanceContainer'>
                            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                            {editMode
                                ? <AddMarkerPoint />
                                : <>
                                    <MainMarker marker={marker} />
                                    <RelatedMarkers markers={marker.properties.related.features} kinds={kinds} /> 
                                    
                                </>
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
                                <p className="marker-date">Added: {FormatDate(marker.properties.add_date)}</p>
                                {!addingStory && !editingStory && <div className="button-group">
                                    <button
                                        onClick={handleEditMode}
                                    >Edit</button>
                                    <button onClick={handleDelete} className="delete">Delete</button>
                                    <button
                                        onClick={() => {
                                            setAddingStory(true)
                                            setErrMsg('')
                                        }}
                                        className="add"
                                    >Add story</button>
                                </div>}
                            </>
                        }
                        {addingStory && <AddStory />}
                        
                            <ul className="tags-list">
                                {Object.entries(marker.properties.tags).map(([key, value]) => (
                                    <li key={key}>
                                        <strong>{key}: </strong>{value}
                                    </li>
                                ))}
                            </ul>
                        
                        <Stories stories_list={marker.properties.stories}  />
                    </div>
                </div>
            }
        </main >
    )
}
export default MarkerInstance
