import React from "react";

interface PythonLogoProps extends React.SVGProps<SVGSVGElement> {
    size?: number | string;
    color?: string;
}

const PythonLogo: React.FC<PythonLogoProps> = ({ size, color, className, style, ...props }) => {
    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={className}
            style={{ ...style, color: color || style?.color }}
            {...props}
        >
            <defs>
                <linearGradient id="python-blue" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#3776AB" />
                    <stop offset="100%" stopColor="#285680" />
                </linearGradient>
                <linearGradient id="python-yellow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#FFD43B" />
                    <stop offset="100%" stopColor="#FFE873" />
                </linearGradient>
            </defs>
            <path
                d="M49.5,22.5 C58,22.5 61,23 64,24 C69,25.5 71,28 71,34 L71,38.5 L56,38.5 L56,40.5 L71,40.5 L71,46.5 C71,53.5 66.5,56.5 60,56.5 L56,56.5 L56,52.5 C56,46.5 53.5,43.5 46.5,43.5 L36,43.5 L36,33 C36,26 39.5,22.5 49.5,22.5 Z M59,28 C60.5,28 61.5,29 61.5,30.5 C61.5,32 60.5,33 59,33 C57.5,33 56.5,32 56.5,30.5 C56.5,29 57.5,28 59,28 Z"
                fill="url(#python-blue)"
                fillOpacity={color ? 0 : 1}
                stroke={color}
                strokeWidth={color ? "4" : "0"}
            />
            <path
                d="M50.5,77.5 C42,77.5 39,77 36,76 C31,74.5 29,72 29,66 L29,61.5 L44,61.5 L44,59.5 L29,59.5 L29,53.5 C29,46.5 33.5,43.5 40,43.5 L44,43.5 L44,47.5 C44,53.5 46.5,56.5 53.5,56.5 L64,56.5 L64,67 C64,74 60.5,77.5 50.5,77.5 Z M41,72 C39.5,72 38.5,71 38.5,69.5 C38.5,68 39.5,67 41,67 C42.5,67 43.5,68 43.5,69.5 C43.5,71 42.5,72 41,72 Z"
                fill="url(#python-yellow)"
                fillOpacity={color ? 0 : 1}
                stroke={color}
                strokeWidth={color ? "4" : "0"}
            />
        </svg>
    );
};

export default PythonLogo;
