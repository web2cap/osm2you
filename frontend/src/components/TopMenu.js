import React, { useState, useEffect } from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';

function TopMenu() {
    const [showLogin, setShowLogin] = useState(false);
    const [showRegistration, setShowRegistration] = useState(false);
    const [accessToken, setAccessToken] = useState('');
    const [user, setUser] = useState(null);
    const [formErrors, setFormErrors] = useState({});
    const [registrationSuccess, setRegistrationSuccess] = useState(false);

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

    const handleRegistrationClick = () => {
        setShowRegistration(true);
    };

    const handleCloseRegistration = () => {
        setShowRegistration(false);
    };

    const handleLoginSubmit = (email, password) => {
        const requestBody = {
            email,
            password,
        };

        fetch('http://localhost:8000/api/v1/auth/jwt/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Login failed');
                }
            })
            .then((data) => {
                //console.log(data);
                setShowLogin(false);
                setAccessToken(data.access);
                localStorage.setItem('accessToken', data.access);
            })
            .catch((error) => {
                console.error(error);
            });
    };

    const handleRegistrationSubmit = (userData) => {
        fetch('http://localhost:8000/api/v1/auth/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
            .then((response) => {
                if (response.status === 201) {
                    handleLoginSubmit(userData.email, userData.password);
                    setRegistrationSuccess(true); // Set registration success state
                } else {
                    return response.json().then((data) => {
                        setFormErrors(data);
                    });
                }
            })
            .catch((error) => {
                console.error(error);
            });
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
                    //console.log(data);
                    setUser(data);
                })
                .catch((error) => {
                    console.error(error);
                    setUser(null);
                });
        }
    }, [accessToken]);

    useEffect(() => {
        if (registrationSuccess) {
            handleCloseRegistration(); // Close the registration form after successful registration
        }
    }, [registrationSuccess]);

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
                                <Nav.Link onClick={handleRegistrationClick}>Join</Nav.Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>

            <LoginForm show={showLogin} handleClose={handleCloseLogin} handleLoginSubmit={handleLoginSubmit} />
            <RegistrationForm
                show={showRegistration}
                handleClose={handleCloseRegistration}
                handleRegistrationSubmit={handleRegistrationSubmit}
                formErrors={formErrors}
            />
        </>
    );
}

export default TopMenu;
