import { useState } from "react";
import AirQualityCard from "./components/AirQualityCard";
import LocationInfo from "./components/LocationInfo";
import MeasureButton from "./components/MeasureButton";
import { measureAirQuality } from "./services/airQualityService";
import type { AirQualityResponse } from "./types/airQuality";

function App() {
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);

  const [result, setResult] =
    useState<AirQualityResponse | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const getLocation = (): Promise<GeolocationPosition> => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(
          new Error(
            "La geolocalización no está disponible en este navegador."
          )
        );
        return;
      }

      navigator.geolocation.getCurrentPosition(
        resolve,
        reject
      );
    });
  };

  const handleMeasure = async () => {
    setLoading(true);
    setError(null);

    try {
      const position = await getLocation();

      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      setLatitude(lat);
      setLongitude(lon);

      const data = await measureAirQuality(lat, lon);

      setResult(data);
    } catch (err) {
      console.error(err);

      if (err instanceof GeolocationPositionError) {
        setError(
          "No fue posible obtener tu ubicación. Verifica los permisos del navegador."
        );
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Ocurrió un error inesperado.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <h1>🍃 AiraAlert</h1>

      <p className="subtitle">
        Monitoreo de PM2.5 en tu ubicación
      </p>

      <AirQualityCard result={result} />

      <LocationInfo
        latitude={latitude}
        longitude={longitude}
      />

      <MeasureButton
        onClick={handleMeasure}
        loading={loading}
      />

      {error && (
        <p className="error-message">
          ⚠️ {error}
        </p>
      )}

      <p className="stations-info">
        Datos disponibles: 21 estaciones SIATA
      </p>
    </main>
  );
}

export default App;