import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

import './TopMenu.css'

function TopMenu() {
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Link href="/"><img src="/img/app.svg" alt="App Logo" className='logo' /> OSM2YOU</Nav.Link>
                </Nav>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="top-menu" />
            <Navbar.Collapse id="top-menu">
                <Nav className="ml-auto">
                    <Nav.Link href="#">Login</Nav.Link>
                    <Nav.Link href="#">Join</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default TopMenu;

