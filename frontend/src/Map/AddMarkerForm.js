import React, { useState } from 'react';
import { useStoreActions, useStoreState } from 'easy-peasy'

import './AddMarkerForm.css'

function AddMarkerForm() {
    const [name, setName] = useState('');

    const setAddingMarker = useStoreActions((actions) => actions.setAddingMarker)
    const addingMarkerPosition = useStoreState((state) => state.addingMarkerPosition)
    const setAddingMarkerPosition = useStoreActions((actions) => actions.setAddingMarkerPosition)

    const handleMarkerAdd = (e) => {
        e.preventDefault();
        if (addingMarkerPosition && name) {
            const newMarker = {
                position: [addingMarkerPosition.lat, addingMarkerPosition.lng],
                name: name,
            };
            // TODO: Add the new marker to your state or backend
            console.log(newMarker)
            setAddingMarkerPosition(null);
            setAddingMarker(false)
            setName('');
        }
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
            </form>
        </div>
    );
}

export default AddMarkerForm;
