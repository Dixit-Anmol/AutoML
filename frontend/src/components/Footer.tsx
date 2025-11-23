import { Github, Twitter, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="border-t border-border bg-card/50 backdrop-blur-lg">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold gradient-text mb-4">ML Yantra</h3>
            <p className="text-muted-foreground text-sm">
              Automated dataset cleaning and ML model training platform.
              Transform your raw data into insights effortlessly.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a href="/" className="hover:text-primary transition-all duration-300 ease-out hover:translate-x-1 inline-block">
                  Home
                </a>
              </li>
              <li>
                <a href="/clean" className="hover:text-primary transition-all duration-300 ease-out hover:translate-x-1 inline-block">
                  Clean Data
                </a>
              </li>
              <li>
                <a href="/train" className="hover:text-primary transition-all duration-300 ease-out hover:translate-x-1 inline-block">
                  Train Model
                </a>
              </li>
              <li>
                <a href="/about" className="hover:text-primary transition-all duration-300 ease-out hover:translate-x-1 inline-block">
                  About
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4">Connect</h4>
            <div className="flex gap-4">
              <a
                href="#"
                className="w-10 h-10 rounded-lg bg-secondary/50 flex items-center justify-center hover:bg-primary/20 hover:text-primary transition-all duration-300 ease-out hover:scale-110 hover:shadow-lg glow-box-cyan"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-lg bg-secondary/50 flex items-center justify-center hover:bg-primary/20 hover:text-primary transition-all duration-300 ease-out hover:scale-110 hover:shadow-lg glow-box-cyan"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-lg bg-secondary/50 flex items-center justify-center hover:bg-primary/20 hover:text-primary transition-all duration-300 ease-out hover:scale-110 hover:shadow-lg glow-box-cyan"
              >
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
          <p>© 2025 ML Yantra. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
