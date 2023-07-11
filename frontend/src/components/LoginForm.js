import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';

function LoginForm({ show, handleClose, handleLoginSubmit, error }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!email || !password) {
            console.error('Please enter both email and password.');
            return;
        }

        handleLoginSubmit(email, password);
    };

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Login</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {error && <Alert variant="danger">{error}</Alert>}
                <Form onSubmit={handleSubmit}>
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
                    <Button variant="secondary" onClick={handleClose} className="mr-2 mt-3">
                        Close
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    );
}

export default LoginForm;
