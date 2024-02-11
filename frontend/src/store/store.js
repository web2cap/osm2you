import { createStore, action } from "easy-peasy";
import axios from 'axios';

const backendURL = process.env.REACT_APP_BACKEND_URL || '';

export default createStore({
    // GENERAL
    DEBUG: true,
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
        baseURL: backendURL
    }),
    setBackendHeader: action((state) => {
        state.backend.defaults.headers.common['Authorization'] = `Bearer ${state.accessToken}`
    }),
    unsetBackendHeader: action((state) => {
        delete state.backend.defaults.headers.common['Authorization'];
    }),

    //MAP
    mapCenter: [51.505, -0.09],
    DEBOUNCE_DELAY: 300,
    //markers
    MARKERS_URL: '/api/v1/markers/',
    markers: [],
    setMarkers: action((state, payload) => {
        state.markers = payload
    }),
    // adding marker
    showAddingMarker: true,
    setShowAddingMarker: action((state, payload) => {
        state.setShowAddingMarker = payload
    }),
    addingMarker: false,
    setAddingMarker: action((state, payload) => {
        state.addingMarker = payload
    }),
    addingMarkerPosition: null,
    setAddingMarkerPosition: action((state, payload) => {
        state.addingMarkerPosition = payload
    }),
    // marker instance
    marker: null,
    setMarker: action((state, payload) => {
        state.marker = payload
    }),
    markerUpdated: false,
    setMarkerUpdated: action((state, payload) => {
        state.markerUpdated = payload
    }),
    // user markers
    markersUser: null,
    setMarkersUser: action((state, payload) => {
        state.markersUser = payload
    }),
    //Status message
    errMsg: '',
    setErrMsg: action((state, payload) => {
        state.errMsg = payload
    }),
    infoMsg: '',
    setInfoMsg: action((state, payload) => {
        state.infoMsg = payload
    }),
    //stories
    STORIES_URL: '/api/v1/stories/',
    // adding story
    addingStory: false,
    setAddingStory: action((state, payload) => {
        state.addingStory = payload
    }),
    editingStory: false,
    setEditingStory: action((state, payload) => {
        state.editingStory = payload
    }),
    //kinds
    KINDS_URL: '/api/v1/kinds/',
    //kinds
    TAGS_URL: '/api/v1/tags/',
})