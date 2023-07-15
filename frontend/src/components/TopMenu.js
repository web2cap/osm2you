import React, { useState, useEffect } from 'react';
import { Navbar, Nav, Modal, Button, Form, Alert } from 'react-bootstrap';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';
import UserEditForm from './UserEditForm';

function TopMenu() {
    const [showLogin, setShowLogin] = useState(false);
    const [showRegistration, setShowRegistration] = useState(false);
    const [showUserInfo, setShowUserInfo] = useState(false);
    const [showEditForm, setShowEditForm] = useState(false);
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
                console.log(data);
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
                    setRegistrationSuccess(true);
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
        setShowUserInfo(false);
    };

    const handleUserInfoClick = () => {
        setShowUserInfo(true);
    };

    const handleCloseUserInfo = () => {
        setShowUserInfo(false);
    };

    const handleEditClick = () => {
        setShowEditForm(true);
    };

    const handleCloseEditForm = () => {
        setShowEditForm(false);
    };

    const handleEditSubmit = (updatedUserData) => {
        fetch('http://127.0.0.1:8000/api/v1/auth/users/me/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify(updatedUserData),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Update user failed');
                }
            })
            .then((data) => {
                console.log(data);
                setUser(data);
                setShowEditForm(false);
            })
            .catch((error) => {
                console.error(error);
            });
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

    useEffect(() => {
        if (registrationSuccess) {
            handleCloseRegistration();
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
                            <Nav.Link onClick={handleUserInfoClick}>{user?.username}</Nav.Link>
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

            <Modal show={showUserInfo} onHide={handleCloseUserInfo} centered>
                <Modal.Header closeButton>
                    <Modal.Title>User Information</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Username: {user?.username}</p>
                    <p>First Name: {user?.first_name}</p>
                    <p>Last Name: {user?.last_name}</p>
                    <p>Bio: {user?.bio || 'N/A'}</p>
                    <p>Instagram: {user?.instagram || 'N/A'}</p>
                    <p>Telegram: {user?.telegram || 'N/A'}</p>
                    <p>Facebook: {user?.facebook || 'N/A'}</p>
                </Modal.Body>
                <Modal.Footer>
                    {accessToken && (
                        <>
                            <Button variant="secondary" onClick={handleEditClick}>
                                Edit
                            </Button>
                            <Button variant="danger" onClick={handleLogout}>
                                Logout
                            </Button>
                        </>
                    )}
                    <Button variant="primary" onClick={handleCloseUserInfo}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            <UserEditForm
                show={showEditForm}
                handleClose={handleCloseEditForm}
                handleEditSubmit={handleEditSubmit}
                user={user}
                formErrors={formErrors}
            />
        </>
    );
}

export default TopMenu;
