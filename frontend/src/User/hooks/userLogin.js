const userLogin = async (email, password, setAccessToken, backend) => {
    const LOGIN_URL = '/api/v1/auth/jwt/create'

    try {
        const response = await backend.post(LOGIN_URL,
            JSON.stringify({ email, password }),
            { headers: { 'Content-Type': 'application/json' } }
        );
        if (response.status !== 200 || !response.data?.access) {
            throw TypeError("Failed")
        }
        localStorage.setItem("accessToken", response.data.access)
        setAccessToken(response.data.access)
        return { status: response.status }
    } catch (err) {
        return {
            data: err?.response?.data ? err.response.data : null,
            status: err?.response?.status ? err.response.status : null
        }
    }
}
export default userLogin