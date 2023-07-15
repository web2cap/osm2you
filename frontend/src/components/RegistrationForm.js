import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';

function RegistrationForm({ show, handleClose, handleRegistrationSubmit, formErrors }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [username, setUsername] = useState('');
    const [bio, setBio] = useState('');
    const [instagram, setInstagram] = useState('');
    const [telegram, setTelegram] = useState('');
    const [facebook, setFacebook] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleFirstNameChange = (e) => {
        setFirstName(e.target.value);
    };

    const handleLastNameChange = (e) => {
        setLastName(e.target.value);
    };

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handleBioChange = (e) => {
        setBio(e.target.value);
    };

    const handleInstagramChange = (e) => {
        setInstagram(e.target.value);
    };

    const handleTelegramChange = (e) => {
        setTelegram(e.target.value);
    };

    const handleFacebookChange = (e) => {
        setFacebook(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!email || !password || !firstName) {
            return; // Don't proceed if required fields are empty
        }

        const userData = {
            email,
            password,
            username,
            first_name: firstName,
            last_name: lastName,
            bio,
            instagram,
            telegram,
            facebook,
        };

        handleRegistrationSubmit(userData);
    };

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Join</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {Object.keys(formErrors).length > 0 && (
                    <div className="mt-3">
                        <h4>Registration Errors:</h4>
                        <ul>
                            {Object.entries(formErrors).map(([field, errors]) =>
                                errors.map((error) => (
                                    <li key={`${field}-${error}`}>
                                        <strong>{field}:</strong> {error}
                                    </li>
                                ))
                            )}
                        </ul>
                    </div>
                )}
                <Form onSubmit={handleSubmit}>
                    <Form.Group controlId="formEmail">
                        <Form.Label className="mr-0">
                            Email<span className="required-field">*</span>
                        </Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={handleEmailChange}
                            isInvalid={formErrors.email !== undefined}
                        />
                        <Form.Control.Feedback type="invalid">{formErrors.email}</Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group controlId="formPassword">
                        <Form.Label className="mt-3 mr-0">
                            Password<span className="required-field">*</span>
                        </Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={handlePasswordChange}
                            isInvalid={formErrors.password !== ''}
                        />
                        <Form.Control.Feedback type="invalid">{formErrors.password}</Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group controlId="formFirstName">
                        <Form.Label className="mt-3 mr-0">
                            First Name<span className="required-field">*</span>
                        </Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter first name"
                            value={firstName}
                            onChange={handleFirstNameChange}
                            isInvalid={formErrors.firstName !== ''}
                        />
                        <Form.Control.Feedback type="invalid">{formErrors.firstName}</Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group controlId="formLastName">
                        <Form.Label className="mt-3 mr-0">Last Name</Form.Label>
                        <Form.Control type="text" placeholder="Enter last name" value={lastName} onChange={handleLastNameChange} />
                    </Form.Group>

                    <Form.Group controlId="formUsername">
                        <Form.Label className="mt-3 mr-0">Username</Form.Label>
                        <Form.Control type="text" placeholder="Enter username" value={username} onChange={handleUsernameChange} />
                    </Form.Group>

                    <Form.Group controlId="formBio">
                        <Form.Label className="mt-3 mr-0">Bio</Form.Label>
                        <Form.Control as="textarea" rows={3} placeholder="Enter bio" value={bio} onChange={handleBioChange} />
                    </Form.Group>

                    <Form.Group controlId="formInstagram">
                        <Form.Label className="mt-3 mr-0">Instagram</Form.Label>
                        <Form.Control type="text" placeholder="Enter Instagram" value={instagram} onChange={handleInstagramChange} />
                    </Form.Group>

                    <Form.Group controlId="formTelegram">
                        <Form.Label className="mt-3 mr-0">Telegram</Form.Label>
                        <Form.Control type="text" placeholder="Enter Telegram" value={telegram} onChange={handleTelegramChange} />
                    </Form.Group>

                    <Form.Group controlId="formFacebook">
                        <Form.Label className="mt-3 mr-0">Facebook</Form.Label>
                        <Form.Control type="text" placeholder="Enter Facebook" value={facebook} onChange={handleFacebookChange} />
                    </Form.Group>

                    <Button variant="primary" type="submit" className="mr-2 mt-3">
                        Register
                    </Button>
                    <Button variant="secondary" onClick={handleClose} className="mr-2 mt-3">
                        Close
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}

export default RegistrationForm;
