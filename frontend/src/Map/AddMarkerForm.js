import React, { useState } from 'react';
import { useStoreActions, useStoreState } from 'easy-peasy'

import './AddMarkerForm.css'

function AddMarkerForm() {
    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)
    const backend = useStoreState((state) => state.backend)

    const [name, setName] = useState('');
    const [errMsg, setErrMsg] = useState('');

    const setAddingMarker = useStoreActions((actions) => actions.setAddingMarker)
    const addingMarkerPosition = useStoreState((state) => state.addingMarkerPosition)
    const setAddingMarkerPosition = useStoreActions((actions) => actions.setAddingMarkerPosition)

    const handleMarkerAdd = async (e) => {
        e.preventDefault();
        if (!addingMarkerPosition || !name) {
            setErrMsg("Invalid Point");
            return
        }
        setErrMsg('')
        const newMarker = {
            name,
            location: {
                type: "Point",
                coordinates: [addingMarkerPosition.lng, addingMarkerPosition.lat],
            }
        };
        try {
            const response = await backend.post(MARKERS_URL,
                JSON.stringify(newMarker),
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 201) {
                throw TypeError("Add Failed")
            }
        } catch (err) {
            setErrMsg(err)
        }

        console.log(newMarker)
        setAddingMarkerPosition(null);
        setAddingMarker(false)
        setName('');
        return
    };

    const onCancel = () => {
        setAddingMarker(false)
        setAddingMarkerPosition(null)
    }

    return (
        <div className="add-marker-form">
            <form onSubmit={handleMarkerAdd}>
                <input
                    type="text"
                    placeholder="Enter name"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <button
                    type="submit"
                    disabled={!addingMarkerPosition || !name}
                >{addingMarkerPosition ? 'Add Marker' : 'Setup position'}</button>
                <button className="cancel"
                    onClick={onCancel}
                >Cancel</button>
                <div
                    className={errMsg ? "errmsg" : "offscreen"}
                    aria-live="assertive"
                >{errMsg}</div>
            </form>
        </div>
    );
}

export default AddMarkerForm;
