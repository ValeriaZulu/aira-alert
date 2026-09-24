import type { AirQualityResponse } from "../types/airQuality";

interface AirQualityCardProps {
    result: AirQualityResponse | null;
}

const colors = {
    verde: {
        background: "#E8F7EE",
        icon: "#2EAD63",
        text: "#207A48",
    },
    amarillo: {
        background: "#FFF7D6",
        icon: "#E5B800",
        text: "#A67C00",
    },
    naranja: {
        background: "#FFF0E1",
        icon: "#F28C28",
        text: "#C46600",
    },
    rojo: {
        background: "#FDE7E7",
        icon: "#E53935",
        text: "#B71C1C",
    },
    morado: {
        background: "#F0E8FA",
        icon: "#8E44AD",
        text: "#6A1B9A",
    },
};

export default function AirQualityCard({
    result,
}: AirQualityCardProps) {
    if (!result) {
        return (
            <div className="air-quality-card empty">
                <div className="status-icon">●</div>
                <h2>Sin medición</h2>
                <p>Presiona el botón para medir la contaminación.</p>
            </div>
        );
    }

    const theme = colors[result.color as keyof typeof colors];

    return (
        <div
            className="air-quality-card"
            style={{
                backgroundColor: theme.background,
            }}
        >
            <div
                className="status-icon"
                style={{ color: theme.icon }}
            >
                ●
            </div>

            <h2 style={{ color: theme.text }}>
                {result.categoria}
            </h2>

            <p className="aqi-value">
                AQI: <strong>{result.aqi}</strong>
            </p>

            <p className="pm25-value">
                PM2.5: <strong>{result.pm25}</strong> µg/m³
            </p>

            <p className="date-value">
                🕐 Datos históricos: {result.fecha}
            </p>
        </div>
    );
}