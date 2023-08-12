import { createStore, action } from "easy-peasy";
import axios from 'axios';

//TODO: Combine Store
export default createStore({
    // GENERAL
    // user
    user: null,
    setUser: action((state, payload) => {
        state.user = payload
    }),
    // user access token for backend
    accessToken: localStorage.getItem('accessToken'),
    setAccessToken: action((state, payload) => {
        state.accessToken = payload
    }),
    // backend api
    backend: axios.create({
        baseURL: 'http://localhost:8000'
    }),
    setBackendHeader: action((state) => {
        state.backend.defaults.headers.common['Authorization'] = `Bearer ${state.accessToken}`
    }),
    unsetBackendHeader: action((state) => {
        delete state.backend.defaults.headers.common['Authorization'];
    }),

    //MAP
    //markers
    markers: [],
    setMarkers: action((state, payload) => {
        state.markers = payload
    }),
    // adding marker
    addingMarker: false,
    setAddingMarker: action((state, payload) => {
        state.addingMarker = payload
    }),
    addingMarkerPosition: null,
    setAddingMarkerPosition: action((state, payload) => {
        state.addingMarkerPosition = payload
    }),
})