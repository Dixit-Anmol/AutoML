import { motion } from "framer-motion";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-background/80 border-b border-border"
    >
      <div className="container mx-auto px-6 py-2 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <img
            src="/favicon.ico"
            alt="ML Yantra Logo"
            className="w-24 h-24 transition-transform group-hover:scale-110"
          />
          <span className="text-4xl font-bold bg-gradient-to-r from-red-400 via-orange-400 to-pink-400 bg-clip-text text-transparent">ML Yantra</span>
        </Link>

        <div className="flex items-center gap-8">
          <Link
            to="/"
            className={`text-lg font-medium transition-all duration-300 ease-out hover:scale-110 ${isActive("/")
              ? "text-primary glow-text-cyan"
              : "text-foreground/70 hover:text-foreground"
              }`}
          >
            Home
          </Link>
          <Link
            to="/clean"
            className={`text-lg font-medium transition-all duration-300 ease-out hover:scale-110 ${isActive("/clean")
              ? "text-primary glow-text-cyan"
              : "text-foreground/70 hover:text-foreground"
              }`}
          >
            Clean Data
          </Link>
          <Link
            to="/train"
            className={`text-lg font-medium transition-all duration-300 ease-out hover:scale-110 ${isActive("/train")
              ? "text-primary glow-text-cyan"
              : "text-foreground/70 hover:text-foreground"
              }`}
          >
            Train Model
          </Link>
          <Link
            to="/about"
            className={`text-lg font-medium transition-all duration-300 ease-out hover:scale-110 ${isActive("/about")
              ? "text-primary glow-text-cyan"
              : "text-foreground/70 hover:text-foreground"
              }`}
          >
            About
          </Link>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
