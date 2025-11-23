import { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";

interface Bubble {
  id: number;
  x: number;
  y: number;
  originalX: number;
  originalY: number;
  size: number;
  color: string;
  speedX: number;
  speedY: number;
}

const InteractiveBackground = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [bubbles, setBubbles] = useState<Bubble[]>([]);
  const bubblesRef = useRef<Bubble[]>([]);

  // Initialize bubbles
  useEffect(() => {
    const initialBubbles: Bubble[] = [];
    const cols = 5;
    const rows = 5;
    const zoneWidth = window.innerWidth / cols;
    const zoneHeight = window.innerHeight / rows;

    for (let i = 0; i < 25; i++) {
      const col = i % cols;
      const row = Math.floor(i / cols);

      // Place bubble randomly within its zone
      const x = col * zoneWidth + Math.random() * zoneWidth;
      const y = row * zoneHeight + Math.random() * zoneHeight;

      initialBubbles.push({
        id: i,
        x,
        y,
        originalX: x,
        originalY: y,
        size: Math.random() * 40 + 20,
        color: i % 3 === 0 ? "hsl(25 90% 65%)" : i % 3 === 1 ? "hsl(340 75% 75%)" : "hsl(10 85% 70%)",
        speedX: 0,
        speedY: 0,
      });
    }
    setBubbles(initialBubbles);
    bubblesRef.current = initialBubbles;
  }, []);

  // Track mouse movement
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Animate bubbles and make them avoid cursor
  useEffect(() => {
    const animationFrame = requestAnimationFrame(function animate() {
      const newBubbles = bubblesRef.current.map((bubble) => {
        let { x, y, speedX, speedY, originalX, originalY } = bubble;

        // Calculate distance from cursor
        const dx = mousePosition.x - x;
        const dy = mousePosition.y - y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const avoidanceRadius = 200;

        // Only affect bubbles near the cursor
        if (distance < avoidanceRadius && distance > 0) {
          // If cursor is near, push bubble away
          const force = (avoidanceRadius - distance) / avoidanceRadius;
          const angle = Math.atan2(dy, dx);
          speedX -= Math.cos(angle) * force * 1.5;
          speedY -= Math.sin(angle) * force * 1.5;
        }

        // Spring back to original position when cursor is far
        const homeX = originalX - x;
        const homeY = originalY - y;
        const homeDistance = Math.sqrt(homeX * homeX + homeY * homeY);

        // Only apply spring force if displaced from home
        if (homeDistance > 2) {
          const springForce = 0.03;
          speedX += homeX * springForce;
          speedY += homeY * springForce;
        } else {
          // Stop movement when very close to home
          speedX *= 0.8;
          speedY *= 0.8;
        }

        // Apply natural movement (slower speed)
        x += speedX * 0.5;
        y += speedY * 0.5;

        // Add stronger damping for slower movement
        speedX *= 0.96;
        speedY *= 0.96;

        return { ...bubble, x, y, speedX, speedY };
      });

      bubblesRef.current = newBubbles;
      setBubbles([...newBubbles]);

      requestAnimationFrame(animate);
    });

    return () => cancelAnimationFrame(animationFrame);
  }, [mousePosition]);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {/* Animated gradient mesh background */}
      <div className="absolute inset-0 opacity-30">
        <motion.div
          className="absolute top-0 left-0 w-full h-full"
          style={{
            background: `
              radial-gradient(circle at 20% 30%, hsl(25 90% 65% / 0.15) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, hsl(340 75% 75% / 0.15) 0%, transparent 50%),
              radial-gradient(circle at 50% 50%, hsl(10 85% 70% / 0.1) 0%, transparent 60%)
            `,
          }}
          animate={{
            opacity: [0.2, 0.4, 0.2],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Dynamic bubbles that avoid cursor */}
      {bubbles.map((bubble) => (
        <motion.div
          key={bubble.id}
          className="absolute rounded-full backdrop-blur-sm"
          style={{
            width: bubble.size,
            height: bubble.size,
            background: `radial-gradient(circle, ${bubble.color}, transparent)`,
            left: bubble.x - bubble.size / 2,
            top: bubble.y - bubble.size / 2,
            opacity: 0.3,
          }}
          animate={{
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 3 + Math.random() * 2,
            repeat: Infinity,
            ease: "easeInOut",
            delay: Math.random() * 2,
          }}
        />
      ))}

      {/* Subtle grid pattern - very light */}
      <motion.div
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `
            linear-gradient(hsl(25 90% 65% / 0.5) 1px, transparent 1px),
            linear-gradient(90deg, hsl(25 90% 65% / 0.5) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
        animate={{
          x: [0, 10, 0],
          y: [0, 10, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "linear",
        }}
      />
    </div>
  );
};

export default InteractiveBackground;
