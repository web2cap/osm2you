import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useStoreActions } from 'easy-peasy'
import './User.css'

const Logout = () => {
    const setAccessToken = useStoreActions((actions) => actions.setAccessToken)
    const setUser = useStoreActions((actions) => actions.setUser)
    const unsetBackendHeader = useStoreActions((actions) => actions.unsetBackendHeader)

    useEffect(() => {
        localStorage.removeItem("accessToken")
        setAccessToken(null)
        setUser(null)
        unsetBackendHeader(null)
    }, [setAccessToken])

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