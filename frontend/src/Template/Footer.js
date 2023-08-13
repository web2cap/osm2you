import { Container, Row, Col } from 'react-bootstrap';
import './Footer.css';

function Footer() {
    return (
        <footer className="footer">
            <Container>
                <Row>
                    <Col md={5}>
                        <p>&copy; 2023 OSM2YOU</p>
                    </Col>
                    <Col md={7} className="text-md-right">
                        <div className="footer-content">
                            <span></span>
                            <a href='https://github.com/web2cap/osm2you' className='github-link'>
                                <div className="github-content">
                                    <img src="/img/github-mark.svg" alt="GitHub Logo" className='github' />
                                    <span>GitHub</span>
                                </div>
                            </a>
                        </div>
                    </Col>
                </Row>
            </Container>
        </footer>
    );
}

export default Footer;