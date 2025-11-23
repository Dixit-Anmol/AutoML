import React from "react";

interface SwastikaIconProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    size?: number | string;
}

const SwastikaIcon: React.FC<SwastikaIconProps> = ({ size, className, style, ...props }) => {
    return (
        <img
            src="/swastika_icon.png"
            alt="Swastika Icon"
            className={className}
            style={{
                width: size,
                height: size,
                objectFit: "contain",
                ...style,
            }}
            {...props}
        />
    );
};

export default SwastikaIcon;
