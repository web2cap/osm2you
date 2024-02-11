import React from 'react'

import RelatedMarker from './RelatedMarker';

const RelatedMarkers = ({markers, kinds}) => {

  return (
    <>
    {markers.map((marker) => {
        return <RelatedMarker marker={marker} kinds={kinds} key={marker.id}/>
    })}
  </>
  )
}

export default RelatedMarkers