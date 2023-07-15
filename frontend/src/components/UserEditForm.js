import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

function UserEditForm({ show, handleClose, handleEditSubmit, user, formErrors }) {
    if (!show || !user) {
        return null;
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const updatedUserData = {
            username: event.target.formUsername.value,
            first_name: event.target.formFirstName.value,
            last_name: event.target.formLastName.value,
            bio: event.target.formBio.value,
            instagram: event.target.formInstagram.value,
            telegram: event.target.formTelegram.value,
            facebook: event.target.formFacebook.value,
        };
        handleEditSubmit(updatedUserData);
    };

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Edit User Information</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group controlId="formUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter username"
                            defaultValue={user.username}
                            isInvalid={formErrors.username && formErrors.username.length > 0}
                        />
                        {formErrors.username && formErrors.username.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.username[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formFirstName">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter first name"
                            defaultValue={user.first_name}
                            isInvalid={formErrors.first_name && formErrors.first_name.length > 0}
                        />
                        {formErrors.first_name && formErrors.first_name.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.first_name[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formLastName">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter last name"
                            defaultValue={user.last_name}
                            isInvalid={formErrors.last_name && formErrors.last_name.length > 0}
                        />
                        {formErrors.last_name && formErrors.last_name.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.last_name[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formBio">
                        <Form.Label>Bio</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            placeholder="Enter bio"
                            defaultValue={user.bio}
                            isInvalid={formErrors.bio && formErrors.bio.length > 0}
                        />
                        {formErrors.bio && formErrors.bio.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.bio[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formInstagram">
                        <Form.Label>Instagram</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter Instagram"
                            defaultValue={user.instagram}
                            isInvalid={formErrors.instagram && formErrors.instagram.length > 0}
                        />
                        {formErrors.instagram && formErrors.instagram.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.instagram[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formTelegram">
                        <Form.Label>Telegram</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter Telegram"
                            defaultValue={user.telegram}
                            isInvalid={formErrors.telegram && formErrors.telegram.length > 0}
                        />
                        {formErrors.telegram && formErrors.telegram.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.telegram[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Form.Group controlId="formFacebook">
                        <Form.Label>Facebook</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter Facebook"
                            defaultValue={user.facebook}
                            isInvalid={formErrors.facebook && formErrors.facebook.length > 0}
                        />
                        {formErrors.facebook && formErrors.facebook.length > 0 && (
                            <Form.Control.Feedback type="invalid">{formErrors.facebook[0]}</Form.Control.Feedback>
                        )}
                    </Form.Group>
                    <Button variant="primary" type="submit">
                        Save Changes
                    </Button>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default UserEditForm;
