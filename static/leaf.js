const TOPIC_NAME = 'testBusData';
const mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

// Marker storage
const mapMarkers = {
  '00001': [],
  '00002': [],
  '00003': []
};

// SSE connection
const source = new EventSource(`/topic/${TOPIC_NAME}`); // Replace TOPICNAME with your Kafka topic

source.addEventListener('message', function (e) {
  const obj = JSON.parse(e.data);
  console.log(obj);

  if (!obj.latitude || !obj.longitude || !obj.busline) return;

  const busline = obj.busline;
  if (!mapMarkers[busline]) return;

  // Remove old markers
  mapMarkers[busline].forEach(marker => mymap.removeLayer(marker));
  mapMarkers[busline] = [];

  // Add new marker
  const marker = L.marker([obj.latitude, obj.longitude]).addTo(mymap);
  mapMarkers[busline].push(marker);
}, false);
