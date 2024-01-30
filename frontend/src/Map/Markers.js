import { useState, useEffect, useRef } from 'react';
import { useStoreState, useStoreActions } from 'easy-peasy';

import { Marker, Popup, useMap } from 'react-leaflet';
import { Link } from 'react-router-dom';
import L from 'leaflet'

import 'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css'; 
import 'leaflet-extra-markers/dist/js/leaflet.extra-markers.min'; 

const Markers = ({backend_path = ''}) => {
    const MARKERS_URL = useStoreState((state) => state.MARKERS_URL)

    const DEBOUNCE_DELAY = useStoreState((state) => state.DEBOUNCE_DELAY);
    const backend = useStoreState((state) => state.backend);

    const markers = useStoreState((state) => state.markers)
    const setMarkers = useStoreActions((actions) => actions.setMarkers)
    const addingMarker = useStoreState((state) => state.addingMarker)

    const markersUser = useStoreState((state) => state.markersUser)
    const setMarkersUser = useStoreActions((actions) => actions.setMarkersUser)

    const setErrMsg = useStoreActions((actions) => actions.setErrMsg)

    const [bbox, setBbox] = useState(null)

    const isFirstCallRef = useRef(true);
    const debounceTimerRef = useRef(null);

    const map = useMap();
    
    const createClusterMarker = (number) => {
        const createClustersNymber = (number) => {
            if (number < 1000) {
                return number.toString();
            } else if (number < 1000000) {
                return (number / 1000).toFixed((number < 2000)? 1 : 0) + 'K';
            }else if (number < 2000000) {
                return (number / 1000).toFixed(1) + 'K';
            } else {
                return (number / 1000000).toFixed((number < 2000000)? 1 : 0) + 'M';
            }
        }
        const getColorByCount = (count) => {
            if (count < 100) {
                return 'green';
            } else if (count < 1000) {
                return 'yellow';
            } else if (count < 5000) {
                return 'orange';
            } else if (count < 20000) {
                return 'red';
            } else {
                return 'purple';
            }
        }
        return L.ExtraMarkers.icon({
            number: createClustersNymber(number),
            icon: 'fa-number',
            markerColor: getColorByCount(number),
            shape: 'square',
            prefix: 'fa',
        });
    };
    // fetch markers
    useEffect(() => {
        async function fetchData() {
            const url = bbox 
                ? `${MARKERS_URL}${backend_path}?in_bbox=${bbox}` 
                : `${MARKERS_URL}${backend_path}`
            try {
                const response = await backend.get(url);
                if (response.status !== 200) {
                    throw TypeError("Failed");
                }
                // store markers user info
                setMarkers(response.data.features);
                if(response.data?.user && !markersUser){
                    setMarkersUser(response.data.user)
                }
            } catch (err) {
                setErrMsg(`Error fetching marker: ${err}`)
                console.error('Error fetching markers:', err);
            }
        }
        console.log(map.getZoom())
        fetchData();
    }, [bbox, backend, addingMarker]);


    // set bbox
    const handleMapChange = () => {
        if (isFirstCallRef.current) {
            isFirstCallRef.current = false;
            callLogic();
            debounceSubsequentCalls();
        } else {
            clearTimeout(debounceTimerRef.current);
            debounceSubsequentCalls();
        }
    };

    const debounceSubsequentCalls = () => {
        debounceTimerRef.current = setTimeout(() => {
            callLogic();
            clearTimeout(debounceTimerRef.current);
        }, DEBOUNCE_DELAY);
    };

    const callLogic = () => {
        const bounds = map.getBounds();
        const bbox = bounds.toBBoxString();
        setBbox(bbox)
        // console.log('Set bbox:', bbox);
    };

    useEffect(() => {
        map.on('move', handleMapChange);
        map.on('zoom', handleMapChange);
        return () => {
            map.off('move', handleMapChange);
            map.off('zoom', handleMapChange);
            clearTimeout(debounceTimerRef.current);
        };
    }, [map]);


    return (
        <>
          {markers.map((marker) => {
            if (marker.properties.kind === 'cluster') {
                const clusterTooltipContent = `${marker.properties.markers_count}`;
                const clusterCoordinates = [
                    marker.geometry.coordinates[1],
                    marker.geometry.coordinates[0],
                ]

                return (
              
                        <Marker key={marker.id}
                            position={clusterCoordinates}
                            icon={
                                createClusterMarker(clusterTooltipContent, clusterCoordinates)
                            }
                            eventHandlers={{
                                click: () => {
                                  map.flyTo(
                                    clusterCoordinates,
                                    map.getZoom() + 2,
                                    { duration: 0.5 }
                                  );
                                },
                              }}
                        />
              
                );
            } else {
              return (
                <Marker
                  key={marker.id}
                  position={[
                    marker.geometry.coordinates[1],
                    marker.geometry.coordinates[0],
                  ]}
                >
                  <Popup>
                    <Link to={`/markers/${marker.id}`}>
                      <h3>{marker.properties.name}</h3>
                    </Link>
                  </Popup>
                </Marker>
              );
            }
          })}
        </>
      );
    };
    
    export default Markers;