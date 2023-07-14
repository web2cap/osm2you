import React, { useState, useEffect } from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';

function TopMenu() {
    const [showLogin, setShowLogin] = useState(false);
    const [showRegistration, setShowRegistration] = useState(false);
    const [accessToken, setAccessToken] = useState('');
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Check if access token is stored in localStorage
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

        // Make the API call to `/api/v1/auth/jwt/create` with the requestBody
        // Replace `YOUR_API_ENDPOINT` with the actual endpoint URL
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
                    throw new Error('Login failed'); // Throw an error if the login request fails
                }
            })
            .then((data) => {
                // Handle the successful response from the API
                console.log(data); // Display or process the response data as needed
                setShowLogin(false); // Close the login modal
                setAccessToken(data.access); // Store the access token in state
                localStorage.setItem('accessToken', data.access); // Store the access token in localStorage
                setEmail(''); // Reset the email field
                setPassword(''); // Reset the password field
            })
            .catch((error) => {
                // Handle the error from the login request
                console.error(error);
            });
    };

    const handleRegistrationSubmit = (userData) => {
        // Make the API call to `/api/v1/auth/users/` with the userData
        // Replace `YOUR_API_ENDPOINT` with the actual endpoint URL
        fetch('http://localhost:8000/api/v1/auth/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
            .then((response) => {
                if (response.status === 201) {
                    // Registration success, now perform login
                    handleLoginSubmit(userData.email, userData.password);
                } else {
                    return response.json().then((data) => {
                        console.log('Registration failed:', data); // Log the error response from the registration request
                    });
                }
            })
            .catch((error) => {
                // Handle the error from the registration request
                console.error(error);
            });
    };

    const handleLogout = () => {
        setAccessToken(''); // Clear the access token from state
        localStorage.removeItem('accessToken'); // Remove the access token from localStorage
    };

    useEffect(() => {
        // Fetch user details from `/api/v1/auth/users/me` if access token is available
        if (accessToken) {
            // Make the API call to `/api/v1/auth/users/me`
            // Replace `YOUR_API_ENDPOINT` with the actual endpoint URL
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
                        throw new Error('User details fetch failed'); // Throw an error if the user details fetch request fails
                    }
                })
                .then((data) => {
                    // Handle the successful response from the API
                    console.log(data); // Display or process the response data as needed
                    setUser(data); // Set the user details in state
                })
                .catch((error) => {
                    // Handle the error from the user details fetch request
                    console.error(error);
                    setUser(null); // Clear the user details in state
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
            />
        </>
    );
}

export default TopMenu;
