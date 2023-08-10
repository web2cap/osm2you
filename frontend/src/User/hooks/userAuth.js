const userAuth = async (accessToken, setAccessToken, setUser, backend, setBackendHeader, unsetBackendHeader) => {
    const USER_ME_URL = '/api/v1/auth/users/me/';

    if (!accessToken) {
        unsetBackendHeader();
        return;
    }

    try {
        setBackendHeader();
        const response = await backend.get(USER_ME_URL);
        if (response.status !== 200 || !response?.data) {
            throw TypeError("Failed");
        }

        setUser(response.data);
    } catch (err) {
        localStorage.removeItem("accessToken");
        setAccessToken(null);
        unsetBackendHeader();
    }
};

export default userAuth;
