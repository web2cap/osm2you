import { useRef, useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom';

import userLogin from './hooks/userLogin';
import './User.css'

const Login = () => {
    const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,24}$/
    const EMAIL_REGEX = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/

    const emailRef = useRef()
    const errRef = useRef()

    const [email, setEmail] = useState('')
    const [validEmail, setValidEmail] = useState(false)

    const [pwd, setPwd] = useState('')
    const [validPwd, setValidPwd] = useState(false)

    const [errMsg, setErrMsg] = useState('')

    const navigate = useNavigate()

    useEffect(() => {
        emailRef.current.focus()
    }, [])

    useEffect(() => {
        setValidEmail(EMAIL_REGEX.test(email))
    }, [email])

    useEffect(() => {
        setValidPwd(PWD_REGEX.test(pwd))
    }, [pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrMsg('');
        if (!EMAIL_REGEX.test(email) || !PWD_REGEX.test(pwd)) {
            setErrMsg("Invalid Entry");
            return;
        }
        const login = await userLogin(email, pwd)
        if (login.status == 200) {
            setEmail('')
            setPwd('')
            navigate('/')
        } else {
            setErrMsg(login?.data?.detail ? login.data.detail : 'Failed')
            errRef.current.focus();
        }
    }

    return (
        <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={handleSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Login</h3>
                    <div ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</div>
                    <div className="form-group mt-3">
                        <label>
                            Email address
                            <span className='Auth-form-requared'>*</span>
                        </label>
                        <input
                            type="email"
                            className="form-control mt-1"
                            placeholder="Enter email"
                            ref={emailRef}
                            onChange={(e) => setEmail(e.target.value)}
                            value={email}
                            required
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Password <span className='Auth-form-requared'>*</span></label>
                        <input
                            type="password"
                            onChange={(e) => setPwd(e.target.value)}
                            value={pwd}
                            required
                            className="form-control mt-1"
                            placeholder="Enter password"
                        />
                    </div>
                    <div className="form-group mt-3">
                        <Link to="/user/forgot" className='nav-link'>Forgot password</Link>
                    </div>

                    <div className="d-grid gap-2 mt-3">
                        <button
                            className="btn btn-primary"
                            disabled={!validEmail || !validPwd ? true : false}
                        >
                            Sign up
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}
export default Login