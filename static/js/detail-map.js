function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.related_links) {
        // Format the related_links array into a list of anchor tags
        var links = feature.properties.related_links.map(function(link) {
            return `<a href="${link}" target="_blank">${link}</a><br>`;
        }).join("");  // Join them into a single string with line breaks

        // Bind the formatted links to the popup
        layer.bindPopup(links);
    }
}

document.addEventListener("DOMContentLoaded", function () {

const gridSquare =  JSON.parse(document.getElementById("geo-data").textContent);
var map = L.map('map').setView([51.505, -0.09], 13);
console
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
console.log(gridSquare)
var geojsonLayer = L.geoJSON(gridSquare, {
    onEachFeature: onEachFeature
}).addTo(map);

map.fitBounds(geojsonLayer.getBounds())
});