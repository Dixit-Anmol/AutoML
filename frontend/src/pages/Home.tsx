import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { ArrowRight, Zap, Database } from "lucide-react";
import { Button } from "@/components/ui/button";
import FloatingOrbs from "@/components/FloatingOrbs";
import InteractiveBackground from "@/components/InteractiveBackground";
import SwastikaIcon from "@/components/SwastikaIcon";

const Home = () => {
  return (
    <div className="min-h-screen relative overflow-hidden">
      <InteractiveBackground />
      <FloatingOrbs />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6">
        <div className="container mx-auto text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-6"
          >
            <motion.div
              className="inline-block"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 5, repeat: Infinity }}
            >
              <SwastikaIcon className="w-16 h-16 mx-auto" />
            </motion.div>

            <h1 className="text-6xl md:text-8xl font-bold gradient-text bg-gradient-to-r from-orange-400 to-pink-400 leading-tight">
              Transform Data
              <br />
              Into Intelligence
            </h1>

            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto">
              Automated dataset cleaning and ML model training.
              <br />
              No code. No hassle. Just results.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link to="/clean">
              <Button
                size="lg"
                className="group relative bg-gradient-to-r from-orange-500 to-pink-500 text-background hover:scale-105 transition-all glow-box-cyan text-lg px-8 py-6"
              >
                Upload Dataset
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>

            <Link to="/train">
              <Button
                size="lg"
                variant="outline"
                className="border-neon-cyan text-neon-cyan hover:bg-neon-cyan/10 glow-box-cyan text-lg px-8 py-6"
              >
                Train Model
                <Zap className="ml-2" />
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative py-32 px-6">
        <div className="container mx-auto">
          <motion.h2
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-bold text-center mb-16 gradient-text"
          >
            Powered by AI
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Database,
                title: "Smart Cleaning",
                description: "Automatically handle missing values, duplicates, and outliers with AI-powered detection.",
                color: "neon-cyan",
              },
              {
                icon: Zap,
                title: "Instant Training",
                description: "Train state-of-the-art ML models in seconds. Choose from regression, classification, and more.",
                color: "neon-purple",
              },
              {
                icon: SwastikaIcon,
                title: "Visual Insights",
                description: "Beautiful visualizations and comprehensive metrics to understand your model's performance.",
                color: "neon-magenta",
              },
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.2 }}
                whileHover={{ y: -10 }}
                className="relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
                <div className="relative bg-card/80 backdrop-blur-sm border border-border rounded-2xl p-8 h-full">
                  <feature.icon className={`w-12 h-12 text-${feature.color} mb-6 glow-text-${feature.color}`} />
                  <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-32 px-6">
        <div className="container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative inline-block"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-neon-purple to-neon-cyan blur-3xl opacity-30" />
            <div className="relative bg-card/50 backdrop-blur-xl border border-border rounded-3xl p-12 md:p-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
                Ready to Get Started?
              </h2>
              <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                Join the future of data science. Upload your dataset and let AI do the heavy lifting.
              </p>
              <Link to="/clean">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-neon-purple to-neon-cyan text-background hover:scale-105 transition-all glow-box-cyan text-lg px-12 py-6"
                >
                  Get Started Now
                  <ArrowRight className="ml-2" />
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;
