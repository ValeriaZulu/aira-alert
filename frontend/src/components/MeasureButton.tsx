interface MeasureButtonProps {
    onClick: () => void;
    loading: boolean;
}

export default function MeasureButton({
    onClick,
    loading,
}: MeasureButtonProps) {
    return (
        <button onClick={onClick} disabled={loading}>
            {loading ? "Midiendo..." : "📊 Medir contaminación"}
        </button>
    );
}