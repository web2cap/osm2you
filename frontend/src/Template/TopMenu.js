import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';
import { useStoreState, useStoreActions } from 'easy-peasy'

import AddMarkerForm from '../Map/AddMarkerForm';
import './TopMenu.css'

function TopMenu() {
    const user = useStoreState((state) => state.user)

    const showAddingMarker = useStoreState((state) => state.showAddingMarker)
    const addingMarker = useStoreState((state) => state.addingMarker)
    const setAddingMarker = useStoreActions((actions) => actions.setAddingMarker)
    
    const location = useLocation()
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand>
                <Nav className="ml-auto">
                    <Link to="/" className='nav-link'>
                        <img src="/img/app.svg" alt="App Logo" className='logo' />
                        OSM2YOU
                    </Link>
                </Nav>
            </Navbar.Brand>
            {addingMarker && location.pathname == "/" && <AddMarkerForm />}
            {!addingMarker && <>
                <Navbar.Toggle aria-controls="top-menu" />
                <Navbar.Collapse id="top-menu">
                    <Nav className="ml-auto">
                        {user ?
                            (
                                <>
                                    {showAddingMarker && location.pathname == "/" &&  <Link
                                        className='nav-link'
                                        onClick={() => { setAddingMarker(true) }}
                                    >Add place</Link>
                                    }
                                    <Link 
                                        to={`/markers/user/${user.username}/`}
                                        className='nav-link'
                                    >
                                        Hi, {user.first_name ? user.first_name : user.username}
                                    </Link>
                                    <Link to="/user/logout" className='nav-link'>Logout</Link>
                                </>
                            ) : (
                                <>
                                    <Link to="/user/registration" className='nav-link'>Registration</Link>
                                    <Link to="/user/login" className='nav-link'>Login</Link>
                                </>
                            )
                        }
                    </Nav>
                </Navbar.Collapse>
            </>}
        </Navbar>
    );
}

export default TopMenu;