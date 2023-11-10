import { Link } from "react-router-dom"
import { useStoreState } from 'easy-peasy';

import './Stories.css'

const Stories = ({stories_list}) => {
    const addingStory = useStoreState((state) => state.addingStory)
    return (
        <ul className="stories-list">
            {stories_list.map((story) => (
                <li key={story.id} className="story-item">
                    <Link className="story-author">
                        {story.author.first_name ? story.author.first_name : story.author.username}
                    </Link>
                    <p className="story-text">{story.text}</p>
                    {!addingStory && story.is_yours && (
                        <div className="button-group">
                            <button className="story-edit-button">Edit</button>
                            <button className="delete">Delete</button>
                        </div>
                    )}
                </li>
            ))}
        </ul>
    )
}

export default Stories