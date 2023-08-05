import { useRef, useState, useEffect } from 'react'

import axios from '../api/axios'
import './User.css'

const Registration = () => {
    const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,24}$/
    const EMAIL_REGEX = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
    const REGISTER_URL = '/api/v1/auth/users/'

    const emailRef = useRef()
    const errRef = useRef()

    const [email, setEmail] = useState('')
    const [validEmail, setValidEmail] = useState(false)

    const [firstName, setFirstName] = useState('')

    const [pwd, setPwd] = useState('')
    const [validPwd, setValidPwd] = useState(false)

    const [matchPwd, setMatchPwd] = useState('')
    const [validMatch, setValidMatch] = useState(false)


    const [errMsg, setErrMsg] = useState('')

    useEffect(() => {
        emailRef.current.focus()
    }, [])

    useEffect(() => {
        setValidEmail(EMAIL_REGEX.test(email))
    }, [email])

    useEffect(() => {
        setValidPwd(PWD_REGEX.test(pwd))
        setValidMatch(pwd === matchPwd)
    }, [pwd, matchPwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrMsg('');
        if (!EMAIL_REGEX.test(email) || !PWD_REGEX.test(pwd)) {
            setErrMsg("Invalid Entry");
            return;
        }
        try {
            const response = await axios.post(REGISTER_URL,
                JSON.stringify({ email, password: pwd, first_name: firstName }),
                { headers: { 'Content-Type': 'application/json' } }
            );
            if (response.status !== 201) {
                throw TypeError("Registration Failed")
            }

            // TODO: autologin

            setEmail('')
            setPwd('')
            setMatchPwd('')
            setFirstName('')
        } catch (err) {
            if (!err?.response) {
                setErrMsg(err.response?.data)
            } else if (err.response?.data) {
                const errorList = Object.entries(err.response.data).map(([key, value], index) => (
                    <li key={index}>
                        {key}: {value.join(' ')}
                    </li>
                ));
                setErrMsg(<ul>{errorList}</ul>)
            } else {
                setErrMsg('Registration Failed')
            }
            errRef.current.focus();
        }
    }

    return (
        <div className="Auth-form-container">
            <form className="Auth-form" onSubmit={handleSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Registration</h3>
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
                        <label>First name <span className='Auth-form-requared'>*</span></label>
                        <input
                            type="text"
                            onChange={(e) => setFirstName(e.target.value)}
                            value={firstName}
                            required
                            className="form-control mt-1"
                            placeholder="Enter First name"
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
                        <label>Confirm password <span className='Auth-form-requared'>*</span> </label>
                        <input
                            type="password"
                            onChange={(e) => setMatchPwd(e.target.value)}
                            value={matchPwd}
                            required
                            className="form-control mt-1"
                            placeholder="Enter password again"
                        />
                    </div>

                    <div className="d-grid gap-2 mt-3">
                        <button
                            className="btn btn-primary"
                            disabled={!validEmail || !validPwd || !validMatch || firstName === '' ? true : false}
                        >
                            Sign up
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}
export default Registration