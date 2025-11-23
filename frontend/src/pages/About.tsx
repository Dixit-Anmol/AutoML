import { motion } from "framer-motion";
import { Zap, Target, Rocket } from "lucide-react";
import FloatingOrbs from "@/components/FloatingOrbs";
import InteractiveBackground from "@/components/InteractiveBackground";
import SwastikaIcon from "@/components/SwastikaIcon";

const About = () => {
  return (
    <div className="min-h-screen relative overflow-hidden pt-24 pb-16">
      <InteractiveBackground />
      <FloatingOrbs />

      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-4">
            About ML Yantra
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Democratizing machine learning through intelligent automation
          </p>
        </motion.div>

        <div className="max-w-5xl mx-auto space-y-16">
          {/* Mission */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-3xl blur-xl" />
            <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-3xl p-12">
              <div className="flex items-start gap-6">
                <Target className="w-12 h-12 text-neon-cyan flex-shrink-0 glow-text-cyan" />
                <div>
                  <h2 className="text-3xl font-bold mb-4 gradient-text">Our Mission</h2>
                  <p className="text-lg text-muted-foreground leading-relaxed">
                    ML Yantra was built with a simple yet powerful vision: to make machine learning
                    accessible to everyone. We believe that powerful AI shouldn't require a PhD in data
                    science or weeks of manual data preparation. Our platform automates the tedious parts
                    of the ML workflow, letting you focus on insights and results.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* What We Do */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/20 to-neon-magenta/20 rounded-3xl blur-xl" />
            <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-3xl p-12">
              <div className="flex items-start gap-6">
                <SwastikaIcon className="w-12 h-12 flex-shrink-0" />
                <div>
                  <h2 className="text-3xl font-bold mb-4 gradient-text">What We Do</h2>
                  <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                    ML Yantra combines cutting-edge artificial intelligence with beautiful, intuitive
                    design to solve two critical challenges in data science:
                  </p>
                  <ul className="space-y-4">
                    <li className="flex items-start gap-3">
                      <div className="w-2 h-2 rounded-full bg-neon-cyan mt-2.5" />
                      <div>
                        <strong className="text-foreground">Automated Data Cleaning:</strong>{" "}
                        <span className="text-muted-foreground">
                          Our AI engine intelligently detects and handles missing values, removes duplicates,
                          identifies outliers, and normalizes your data—all in seconds.
                        </span>
                      </div>
                    </li>
                    <li className="flex items-start gap-3">
                      <div className="w-2 h-2 rounded-full bg-neon-magenta mt-2.5" />
                      <div>
                        <strong className="text-foreground">One-Click Model Training:</strong>{" "}
                        <span className="text-muted-foreground">
                          Select your model type, and we'll handle the rest. From hyperparameter tuning
                          to validation, we optimize everything for peak performance.
                        </span>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Technology */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-neon-magenta/20 to-neon-purple/20 rounded-3xl blur-xl" />
            <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-3xl p-12">
              <div className="flex items-start gap-6">
                <Zap className="w-12 h-12 text-neon-purple flex-shrink-0 glow-text-purple" />
                <div>
                  <h2 className="text-3xl font-bold mb-4 gradient-text">Powered by AI</h2>
                  <p className="text-lg text-muted-foreground leading-relaxed">
                    Under the hood, ML Yantra leverages state-of-the-art machine learning algorithms
                    and deep learning models. Our platform is built on proven frameworks and libraries,
                    ensuring your models are not just fast, but also accurate and reliable. Every dataset
                    is analyzed using advanced statistical methods and neural networks trained on millions
                    of data points.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Vision */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-3xl blur-xl" />
            <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-3xl p-12">
              <div className="flex items-start gap-6">
                <Rocket className="w-12 h-12 text-neon-cyan flex-shrink-0 glow-text-cyan" />
                <div>
                  <h2 className="text-3xl font-bold mb-4 gradient-text">The Future</h2>
                  <p className="text-lg text-muted-foreground leading-relaxed">
                    We're just getting started. Our roadmap includes advanced model architectures,
                    automated feature engineering, real-time model monitoring, and collaborative workspaces.
                    ML Yantra will continue to evolve, bringing the latest AI research directly to your
                    fingertips—no expertise required.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default About;
