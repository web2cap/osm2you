import React, { useState } from 'react';
import { useParams } from "react-router-dom"
import { useStoreActions, useStoreState } from 'easy-peasy'


import './AddStory.css'

const AddStory = () => {
    const { id } = useParams()

    const STORIES_URL = useStoreState((state) => state.STORIES_URL) //
    const backend = useStoreState((state) => state.backend)

    const [storyText, setStoryText] = useState('');

    const setErrMsg = useStoreActions((actions) => actions.setErrMsg)
    const setInfoMsg = useStoreActions((actions) => actions.setInfoMsg)

    const setAddingStory = useStoreActions((actions) => actions.setAddingStory) 

    const handleStoryAdd = async (e) => {
        e.preventDefault();
        setStoryText(storyText.trim())
        if (storyText.length < 10) {
            setErrMsg("Story must be longer");
            return
        }
        setErrMsg('')
        const newStory = {
            text: storyText,
            marker: id
        }
        try {
            const response = await backend.post(STORIES_URL,
                JSON.stringify(newStory),
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 201) {
                const errorResponse = await response.json();
                console.log(errorResponse.message)
                throw new Error(errorResponse.message || 'Add Failed');
            }
            setInfoMsg('History added successfully')
        } catch (err) {
            setErrMsg(`${err.message} ${err?.response?.data?.detail ? err.response.data.detail : ''}`)
            console.log(err)
        }

        console.log(newStory)
        setAddingStory(false)
        setStoryText('');
        return
    }

    const onCancel = () => {
        setAddingStory(false)
    }

    return (
        <div className="add-story-form">
            <h3>Add story</h3>
            <form onSubmit={handleStoryAdd}>
                
                    <textarea
                        rows={10}
                        placeholder="Enter story text"
                        required
                        value={storyText}
                        onChange={(e) => setStoryText(e.target.value)}
                    ></textarea>
                
                <div>
                    <button
                        type="submit"
                        disabled={storyText.length < 10}
                    >Save</button>
                    <button className="cancel"
                        onClick={onCancel}
                    >Cancel</button>
                </div>
            </form>
        </div>
    )
}

export default AddStory