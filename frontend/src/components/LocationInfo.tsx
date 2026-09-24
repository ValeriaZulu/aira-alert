interface LocationInfoProps {
    latitude: number | null;
    longitude: number | null;
}

export default function LocationInfo({
    latitude,
    longitude,
}: LocationInfoProps) {
    if (latitude === null || longitude === null) {
        return <p>📍 Ubicación no detectada</p>;
    }

    return (
        <p>
            📍 Ubicación: {latitude.toFixed(5)}, {longitude.toFixed(5)}
        </p>
    );
}