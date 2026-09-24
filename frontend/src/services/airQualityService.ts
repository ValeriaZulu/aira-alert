import type { AirQualityResponse } from "../types/airQuality";

const API_URL = "http://54.172.49.168:5000";

export async function measureAirQuality(
    latitude: number,
    longitude: number
): Promise<AirQualityResponse> {
    const response = await fetch(`${API_URL}/medir`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            latitud: latitude,
            longitud: longitude,
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
            errorData?.error || "No se pudo obtener la calidad del aire"
        );
    }

    return response.json();
}