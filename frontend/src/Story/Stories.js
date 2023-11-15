import Story from "./Story";
import './Stories.css'

const Stories = ({stories_list}) => {
    return (
        <ul className="stories-list">
            {stories_list.map((story) => (
                <Story story={story} />
            ))}
        </ul>
    )
}

export default Stories