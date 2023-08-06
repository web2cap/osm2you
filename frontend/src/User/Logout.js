import { Link } from 'react-router-dom';

import './User.css'

const Logout = ({ setAccessToken }) => {
    localStorage.removeItem("accessToken");
    setAccessToken(null)
    return (
        <div className="Auth-form-container">
            <div className="Auth-form-content">
                <h3 className="Auth-form-title">Successfully logged out.</h3>
                <div aria-live="assertive">
                    <Link to='/'>Home</Link>
                </div>
            </div>
        </div>
    )
}
export default Logout