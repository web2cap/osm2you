import React, { useState, useEffect } from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import LoginForm from './LoginForm';

function TopMenu() {
    const [showLogin, setShowLogin] = useState(false);
    const [accessToken, setAccessToken] = useState('');
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const storedAccessToken = localStorage.getItem('accessToken');
        if (storedAccessToken) {
            setAccessToken(storedAccessToken);
        }
    }, []);

    const handleLoginClick = () => {
        setShowLogin(true);
    };

    const handleCloseLogin = () => {
        setShowLogin(false);
    };

    const handleLoginSubmit = async (email, password) => {
        const requestBody = {
            email,
            password,
        };

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/jwt/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (response.ok) {
                const data = await response.json();
                setAccessToken(data.access);
                localStorage.setItem('accessToken', data.access);
                setShowLogin(false);
                setError('');
            } else {
                throw new Error('Login failed');
            }
        } catch (error) {
            console.error(error);
            setError('Login failed. Please check your credentials.');
        }
    };

    const handleLogout = () => {
        setAccessToken('');
        localStorage.removeItem('accessToken');
    };

    useEffect(() => {
        if (accessToken) {
            fetch('http://localhost:8000/api/v1/auth/users/me', {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('User details fetch failed');
                    }
                })
                .then((data) => {
                    console.log(data);
                    setUser(data);
                })
                .catch((error) => {
                    console.error(error);
                    setUser(null);
                });
        }
    }, [accessToken]);

    return (
        <>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand>
                    <Nav className="ml-auto">
                        <Nav.Link href="#">
                            <img src="/img/app.svg" alt="App Logo" className="logo" /> OSM2YOU
                        </Nav.Link>
                    </Nav>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="top-menu" />
                <Navbar.Collapse id="top-menu">
                    <Nav className="ml-auto">
                        {accessToken ? (
                            <>
                                <Nav.Link>{user?.username}</Nav.Link>
                                <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
                            </>
                        ) : (
                            <>
                                <Nav.Link onClick={handleLoginClick}>Login</Nav.Link>
                                <Nav.Link href="#">Join</Nav.Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>

            <LoginForm show={showLogin} handleClose={handleCloseLogin} handleLoginSubmit={handleLoginSubmit} error={error} />
        </>
    );
}

export default TopMenu;
