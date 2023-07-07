const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm], minZoom: 3 });
map.
    locate()
    .on("locationfound", (e) => map.setView(e.latlng, 8))
    .on("locationerror", () => map.setView([0, 0], 3));

async function load_markers() {
    const markers_url = `/api/markers/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(markers_url)
    const geojson = await response.json()
    return geojson
}

async function render_markers() {
    const markers = await load_markers();
    L.geoJSON(markers)
        .bindPopup((layer) => `<a href="/marker/${layer.feature.id}/">${layer.feature.properties.name}</a>`)
        .addTo(map);

    markers_list = ""
    for (x in markers.features) {
        markers_list += '<tr><td><a href="/marker/' + markers.features[x].id + '/">' + markers.features[x].properties.name + '<a/></td></tr>';
    }
    document.getElementById("markers_list").innerHTML = markers_list;
}

map.on("moveend", render_markers);