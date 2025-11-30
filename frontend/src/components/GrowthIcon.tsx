import React from "react";

interface GrowthIconProps extends React.SVGProps<SVGSVGElement> {
    size?: number | string;
}

const GrowthIcon: React.FC<GrowthIconProps> = ({
    size = 24,
    className = "",
    ...props
}) => {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            stroke="#fb923c"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
            {...props}
        >
            <defs>
                <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#fb923c', stopOpacity: 1 }} />
                    <stop offset="50%" style={{ stopColor: '#fb7185', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#f472b6', stopOpacity: 1 }} />
                </linearGradient>
            </defs>

            {/* Bar chart bars with gradient */}
            <rect x="3" y="16" width="3" height="5" fill="url(#barGradient)" opacity="0.7" />
            <rect x="8" y="12" width="3" height="9" fill="url(#barGradient)" opacity="0.8" />
            <rect x="13" y="8" width="3" height="13" fill="url(#barGradient)" opacity="0.9" />
            <rect x="18" y="4" width="3" height="17" fill="url(#barGradient)" opacity="1" />

            {/* Upward trending line */}
            <polyline points="2 17 7 13 12 9 17 5 22 2" />

            {/* Arrow at the end */}
            <polyline points="18 2 22 2 22 6" />
        </svg>
    );
};

export default GrowthIcon;
