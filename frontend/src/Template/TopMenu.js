import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';

import './TopMenu.css'

function TopMenu() {
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Link href="#">
                        <img src="/img/app.svg" alt="App Logo" className='logo' />
                        OSM2YOU
                    </Nav.Link>
                </Nav>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="top-menu" />
            <Navbar.Collapse id="top-menu">
                <Nav className="ml-auto">
                    <Link to="/user/registration" className='nav-link'>Registration</Link>
                    <Link to="/user/login" className='nav-link'>Login</Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default TopMenu;