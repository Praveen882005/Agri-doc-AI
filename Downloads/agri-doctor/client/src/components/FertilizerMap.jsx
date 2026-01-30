import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "../App.css";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

export default function FertilizerMap() {
  const [city, setCity] = useState("");
  const [shops, setShops] = useState([]);

  const locations = {
    Chennai: [
      { name: "GreenGrow Fertilizers", lat: 13.0827, lon: 80.2707 },
      { name: "AgriZone Supplies", lat: 13.05, lon: 80.25 },
    ],
    Bengaluru: [
      { name: "FarmBoost", lat: 12.9716, lon: 77.5946 },
      { name: "AgroMart", lat: 12.98, lon: 77.6 },
    ],
    Coimbatore: [
      { name: "Kovai Agro Center", lat: 11.0168, lon: 76.9558 },
      { name: "Farm Needs Store", lat: 11.02, lon: 76.96 },
    ],
  };

  const handleSearch = () => {
    if (locations[city]) setShops(locations[city]);
    else alert("City not found. Try Chennai, Bengaluru, or Coimbatore.");
  };

  return (
    <div>
      <h2>📍 Nearby Fertilizer Shops</h2>

      <input
        type="text"
        placeholder="Enter city (e.g., Chennai)"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        style={{ padding: "8px", borderRadius: "6px", marginRight: "8px" }}
      />
      <button className="button" onClick={handleSearch}>
        Search
      </button>

      <div className="map-container">
        <MapContainer
          center={[11.0, 77.0]}
          zoom={6}
          style={{ height: "300px", width: "100%", marginTop: "10px" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors"
          />
          {shops.map((shop, index) => (
            <Marker key={index} position={[shop.lat, shop.lon]}>
              <Popup>{shop.name}</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
