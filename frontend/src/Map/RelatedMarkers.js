import React from 'react'

import RelatedMarker from './RelatedMarker';

const RelatedMarkers = ({markers}) => {

  return (
    <>
    {markers.map((marker) => {
        return <RelatedMarker marker={marker} />
    })}
  </>
  )
}

export default RelatedMarkers