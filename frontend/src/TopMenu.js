// http://localhost:8000/api/v1/auth/jwt/create/
// http://localhost:8000/api/v1/auth/users/me
import React, { useState, useEffect } from 'react';
import { Navbar, Nav, Modal, Button, Form, Alert } from 'react-bootstrap';

function TopMenu() {
    const [showLogin, setShowLogin] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
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
        setErrorMessage('');
    };

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleLoginSubmit = (e) => {
        e.preventDefault();

        // Send the login request to the API
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
                setErrorMessage(''); // Reset the error message
                setShowLogin(false); // Close the login modal
                setAccessToken(data.access); // Store the access token in state
                localStorage.setItem('accessToken', data.access); // Store the access token in localStorage
            })
            .catch((error) => {
                // Handle the error from the login request
                console.error(error);
                setErrorMessage('Login failed. Please check your credentials.'); // Set the error message
            })
            .finally(() => {
                // Reset the form fields
                setEmail('');
                setPassword('');
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
                    'Authorization': `Bearer ${accessToken}`,
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
                            <Nav.Link>{user?.username}</Nav.Link>
                        ) : (
                            <>
                                <Nav.Link onClick={handleLoginClick}>Login</Nav.Link>
                                <Nav.Link href="#">Join</Nav.Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>

            <Modal show={showLogin} onHide={handleCloseLogin} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Login</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
                    <Form onSubmit={handleLoginSubmit}>
                        <Form.Group controlId="formEmail">
                            <Form.Label className="mr-0">Email</Form.Label>
                            <Form.Control type="email" placeholder="Enter email" value={email} onChange={handleEmailChange} />
                        </Form.Group>

                        <Form.Group controlId="formPassword">
                            <Form.Label className="mt-3 mr-0">Password</Form.Label>
                            <Form.Control type="password" placeholder="Enter password" value={password} onChange={handlePasswordChange} />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="mr-2 mt-3">
                            Login
                        </Button>
                        <Button variant="secondary" onClick={handleCloseLogin} className="mr-2 mt-3">
                            Close
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
}

export default TopMenu;
