import axios from "../../api/axios";

const userGetMe = async (accessToken, setAccessToken, setUser) => {
    const USER_ME_URL = '/api/v1/auth/users/me/'

    if (!accessToken) return
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    try {
        const response = await axios.get(USER_ME_URL);
        if (response.status !== 200 || !response?.data) {
            throw TypeError("Failed")
        }
        console.log('get me')
        console.log(response.data)
        setUser(response.data)
    } catch (err) {
        console.log(err)
        console.log('remove access token')
        localStorage.removeItem("accessToken");
        setAccessToken(null)
    }
}

export default userGetMe