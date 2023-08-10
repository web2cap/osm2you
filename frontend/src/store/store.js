import { createStore, action } from "easy-peasy";
import axios from 'axios';

export default createStore({
    user: null,
    setUser: action((state, payload) => {
        state.user = payload
    }),

    accessToken: localStorage.getItem('accessToken'),
    setAccessToken: action((state, payload) => {
        state.accessToken = payload
    }),

    backend: axios.create({
        baseURL: 'http://localhost:8000'
    }),
    setBackendHeader: action((state) => {
        state.backend.defaults.headers.common['Authorization'] = `Bearer ${state.accessToken}`
    }),
    unsetBackendHeader: action((state) => {
        delete state.backend.defaults.headers.common['Authorization'];
    }),
})