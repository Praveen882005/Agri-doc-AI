import React, { useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function FertilizerMap() {
  const [city, setCity] = useState("");
  const [shops, setShops] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8001/shops", { city });
      setShops(res.data.shops || []);
    } catch (err) {
      console.error(err);
      setShops([]);
    }
  };

  return (
    <div>
      <h2>Nearby Fertilizer Shops</h2>
      <input
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter city"
      />
      <button onClick={handleSearch}>Search</button>

      {shops.length > 0 && (
        <MapContainer
          center={[shops[0].lat, shops[0].lng]}
          zoom={12}
          style={{ height: "400px", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          {shops.map((shop, idx) => (
            <Marker key={idx} position={[shop.lat, shop.lng]}>
              <Popup>
                <b>{shop.name}</b>
                <br />
                {shop.address}
                <br />
                {shop.contact}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </div>
  );
}
