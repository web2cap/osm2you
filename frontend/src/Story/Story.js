import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useStoreState, useStoreActions } from 'easy-peasy';

import './Story.css'

const Story = ({ story }) => {
    const STORIES_URL = useStoreState((state) => state.STORIES_URL) //
    const backend = useStoreState((state) => state.backend)

    const setErrMsg = useStoreActions((actions) => actions.setErrMsg)
    const setInfoMsg = useStoreActions((actions) => actions.setInfoMsg)

    const addingStory = useStoreState((state) => state.addingStory)
    
    const editingStory = useStoreState((state) => state.editingStory)
    const setEditingStory = useStoreActions((actions) => actions.setEditingStory)

    const setMarkerUpdated = useStoreActions((actions) => actions.setMarkerUpdated)

    const [editingThisStory, setEditingThisStory] = useState(false);
    const [editedText, setEditedText] = useState(story.text);

    const handleEditClick = () => {
        setEditingThisStory(true);
        setEditingStory(true);
    };

    const handleCancelClick = () => {
        setEditingThisStory(false);
        setEditingStory(false);
        setEditedText(story.text);
    };

    const handleSaveClick = async(e) => {
        e.preventDefault();
        setEditedText(editedText.trim())
        if (editedText.length < 10) {
            setErrMsg("Story must be longer");
            return
        }
        setErrMsg('')
        const editedStory = {
            text: editedText,
        }
        try {
            const response = await backend.patch(`${STORIES_URL}${story.id}/`,
                JSON.stringify(editedStory),
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 200) {
                const errorResponse = await response.json();
                console.log(errorResponse.message)
                throw new Error(errorResponse.message || 'Edited Failed');
            }
            setInfoMsg('Story edited successfully')

            // response.data contains the new story
            setMarkerUpdated(true)
            
        } catch (err) {
            setErrMsg(`${err.message} ${err?.response?.data?.detail ? err.response.data.detail : ''}`)
            console.log(err)
        }

        setEditingThisStory(false);
        setEditingStory(false);
        return
    };

    const handleDeleteClick = () => {
        // Handle delete logic
        return
    };

    return (
        <li key={story.id} className="story-item">
        {!editingThisStory ? (
            <>
            <Link className="story-author">{story.author.first_name ? story.author.first_name : story.author.username}</Link>
            <p className="story-text">{story.text}</p>
            {!addingStory && !editingStory && story.is_yours && (
                <div className="button-group">
                <button onClick={handleEditClick}>Edit</button>
                <button className="delete" onClick={handleDeleteClick}>
                    Delete
                </button>
                </div>
            )}
            </>
        ) : (
            // Edit mode
            <div>
            <textarea
                rows={10}
                value={editedText}
                onChange={(e) => setEditedText(e.target.value)}
                className='edit-story-item'
            ></textarea>
            <div>
                <button onClick={handleSaveClick}>Save</button>
                <button className="cancel" onClick={handleCancelClick}>
                Cancel
                </button>
            </div>
            </div>
        )}
        </li>
    );
};
export default Story