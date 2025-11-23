import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Upload, Zap, BarChart, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import FloatingOrbs from "@/components/FloatingOrbs";
import InteractiveBackground from "@/components/InteractiveBackground";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { apiClient } from "@/lib/apiClient";
import type { DatasetInfo, ModelMetrics, TrainingResponse } from "@/types/api";

const Train = () => {
  const [file, setFile] = useState<File | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [datasetInfo, setDatasetInfo] = useState<DatasetInfo | null>(null);
  const [targetColumn, setTargetColumn] = useState<string>("");
  const [problemType, setProblemType] = useState<"classification" | "regression">("classification");
  const [testSize, setTestSize] = useState<number>(0.2);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [currentModel, setCurrentModel] = useState<string | null>(null);
  const [results, setResults] = useState<TrainingResponse | null>(null);
  const { toast } = useToast();

  // Check for existing session from Clean page
  useEffect(() => {
    const savedSessionId = localStorage.getItem("automl_session_id");
    if (savedSessionId) {
      loadExistingSession(savedSessionId);
    }
  }, []);

  const loadExistingSession = async (sid: string) => {
    try {
      const info = await apiClient.getDatasetInfo(sid);
      setDatasetInfo(info);
      setSessionId(sid);
      toast({
        title: "Dataset Loaded",
        description: "Using dataset from cleaning workflow",
      });
    } catch (error) {
      console.error("Failed to load existing session:", error);
      localStorage.removeItem("automl_session_id");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResults(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      const uploadResult = await apiClient.uploadDataset(file);
      setSessionId(uploadResult.session_id);
      setDatasetInfo(uploadResult.dataset_info);
      localStorage.setItem("automl_session_id", uploadResult.session_id);

      toast({
        title: "Upload Successful!",
        description: `${uploadResult.filename} uploaded successfully`,
      });
    } catch (error: any) {
      toast({
        title: "Upload Failed",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleTrain = async () => {
    if (!sessionId || !targetColumn) {
      toast({
        title: "Missing Information",
        description: "Please upload a dataset and select a target column.",
        variant: "destructive",
      });
      return;
    }

    setIsTraining(true);
    setTrainingProgress(0);
    setResults(null);

    try {
      // Start training
      await apiClient.startTraining(sessionId, targetColumn, problemType, testSize);

      // Poll for progress
      const pollInterval = setInterval(async () => {
        try {
          const status = await apiClient.getTrainingStatus(sessionId);

          setTrainingProgress(status.progress * 100);
          setCurrentModel(status.current_model || null);

          if (status.status === "completed") {
            clearInterval(pollInterval);

            // Get results
            const trainingResults = await apiClient.getTrainingResults(sessionId);
            setResults(trainingResults);
            setIsTraining(false);

            toast({
              title: "Training Complete! 🎉",
              description: `Best model: ${trainingResults.best_model}`,
            });
          } else if (status.status === "failed") {
            clearInterval(pollInterval);
            setIsTraining(false);

            toast({
              title: "Training Failed",
              description: status.message || "An error occurred during training",
              variant: "destructive",
            });
          }
        } catch (error: any) {
          clearInterval(pollInterval);
          setIsTraining(false);

          toast({
            title: "Error",
            description: error.message,
            variant: "destructive",
          });
        }
      }, 1000); // Poll every second

    } catch (error: any) {
      setIsTraining(false);
      toast({
        title: "Training Failed",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const columns = datasetInfo ? Object.keys(datasetInfo.column_types) : [];

  return (
    <div className="min-h-screen relative overflow-hidden pt-24 pb-16">
      <InteractiveBackground />
      <FloatingOrbs />

      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-4">
            Train Your Model
          </h1>
          <p className="text-xl text-muted-foreground">
            Upload your clean dataset and train state-of-the-art ML models
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Upload or Import Section */}
          {!sessionId && (
            <>
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all" />
                <label className="relative block">
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <div className="relative bg-card/50 backdrop-blur-xl border-2 border-dashed border-border rounded-3xl p-12 cursor-pointer hover:border-neon-cyan transition-all text-center">
                    {file ? (
                      <div className="flex items-center justify-center gap-4">
                        <BarChart className="w-12 h-12 text-neon-cyan" />
                        <div>
                          <h3 className="text-xl font-bold">{file.name}</h3>
                          <p className="text-sm text-muted-foreground">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                    ) : (
                      <>
                        <Upload className="w-16 h-16 mx-auto mb-6 text-neon-cyan glow-text-cyan" />
                        <h3 className="text-2xl font-bold mb-2">Upload Clean Dataset</h3>
                        <p className="text-muted-foreground">Click to browse or drag & drop</p>
                      </>
                    )}
                  </div>
                </label>
              </motion.div>

              {file && (
                <div className="flex justify-center">
                  <Button
                    onClick={handleUpload}
                    size="lg"
                    className="bg-gradient-to-r from-red-400 via-orange-400 to-pink-400 text-white hover:scale-105 transition-all text-lg px-8"
                  >
                    Upload Dataset
                  </Button>
                </div>
              )}
            </>
          )}

          {/* Dataset Info */}
          {sessionId && datasetInfo && !isTraining && !results && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Dataset Stats */}
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/20 to-neon-magenta/20 rounded-2xl blur-xl" />
                <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-6">
                  <h3 className="text-2xl font-bold mb-4">Dataset Overview</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-secondary/50 rounded-xl p-4 text-center">
                      <p className="text-3xl font-bold text-primary">{datasetInfo.rows}</p>
                      <p className="text-sm text-muted-foreground">Rows</p>
                    </div>
                    <div className="bg-secondary/50 rounded-xl p-4 text-center">
                      <p className="text-3xl font-bold text-primary">{datasetInfo.columns}</p>
                      <p className="text-sm text-muted-foreground">Columns</p>
                    </div>
                    <div className="bg-secondary/50 rounded-xl p-4 text-center">
                      <p className="text-3xl font-bold text-primary">{datasetInfo.memory_mb.toFixed(2)}</p>
                      <p className="text-sm text-muted-foreground">MB</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Training Configuration */}
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-2xl blur-xl" />
                <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-8">
                  <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                    <Zap className="text-neon-purple" />
                    Training Configuration
                  </h3>

                  <div className="space-y-6">
                    {/* Target Column */}
                    <div>
                      <label className="block text-sm font-medium mb-2">Target Column</label>
                      <Select value={targetColumn} onValueChange={setTargetColumn}>
                        <SelectTrigger className="w-full text-lg py-6 bg-secondary/50 border-border">
                          <SelectValue placeholder="Select target column..." />
                        </SelectTrigger>
                        <SelectContent>
                          {columns.map((col) => (
                            <SelectItem key={col} value={col}>
                              {col} ({datasetInfo.column_types[col]})
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Problem Type */}
                    <div>
                      <label className="block text-sm font-medium mb-2">Problem Type</label>
                      <Select value={problemType} onValueChange={(v: any) => setProblemType(v)}>
                        <SelectTrigger className="w-full text-lg py-6 bg-secondary/50 border-border">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="classification">Classification</SelectItem>
                          <SelectItem value="regression">Regression</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Test Size */}
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Test Set Size: {(testSize * 100).toFixed(0)}%
                      </label>
                      <input
                        type="range"
                        min="10"
                        max="50"
                        step="5"
                        value={testSize * 100}
                        onChange={(e) => setTestSize(parseInt(e.target.value) / 100)}
                        className="w-full"
                      />
                    </div>

                    <Button
                      onClick={handleTrain}
                      disabled={!targetColumn}
                      size="lg"
                      className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400 text-white hover:scale-105 transition-all text-lg py-6"
                    >
                      <Zap className="mr-2" />
                      Start Training
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Training Progress */}
          {isTraining && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-cyan/20 rounded-2xl blur-xl pulse-glow" />
              <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-12 text-center">
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="mb-6"
                >
                  <Zap className="w-20 h-20 mx-auto text-neon-purple glow-text-purple" />
                </motion.div>
                <h3 className="text-3xl font-bold mb-2 gradient-text">Training Models...</h3>
                <p className="text-muted-foreground text-lg mb-6">
                  {currentModel ? `Training ${currentModel}` : "Initializing training..."}
                </p>

                {/* Progress Bar */}
                <div className="w-full bg-secondary rounded-full h-4 mb-4 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${trainingProgress}%` }}
                    className="h-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <p className="text-sm text-muted-foreground">{trainingProgress.toFixed(0)}% Complete</p>
              </div>
            </motion.div>
          )}

          {/* Results */}
          {results && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/20 to-neon-magenta/20 rounded-2xl blur-xl" />
                <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-8">
                  <div className="flex items-center gap-4 mb-8">
                    <TrendingUp className="w-12 h-12 text-neon-cyan glow-text-cyan" />
                    <div>
                      <h3 className="text-3xl font-bold gradient-text">Training Complete!</h3>
                      <p className="text-muted-foreground">
                        {results.models_trained} models trained in {results.training_time_seconds}s
                      </p>
                    </div>
                  </div>

                  {/* Best Model */}
                  <div className="bg-gradient-to-r from-neon-purple/20 to-neon-cyan/20 rounded-xl p-6 mb-6 border-2 border-neon-cyan">
                    <p className="text-sm text-muted-foreground mb-1">Best Model</p>
                    <p className="text-2xl font-bold text-neon-cyan">{results.best_model}</p>
                  </div>

                  <h4 className="text-xl font-bold mb-4">Model Performance</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {results.results.map((model: ModelMetrics, idx: number) => (
                      <motion.div
                        key={idx}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className={`bg-secondary/50 rounded-xl p-6 ${model.model_name === results.best_model
                          ? "border-2 border-neon-cyan"
                          : ""
                          }`}
                      >
                        <h5 className="font-bold text-lg mb-3">{model.model_name}</h5>
                        {problemType === "classification" ? (
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Accuracy:</span>
                              <span className="font-bold">{(model.accuracy! * 100).toFixed(2)}%</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Precision:</span>
                              <span className="font-bold">{(model.precision! * 100).toFixed(2)}%</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">Recall:</span>
                              <span className="font-bold">{(model.recall! * 100).toFixed(2)}%</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">F1 Score:</span>
                              <span className="font-bold">{(model.f1_score! * 100).toFixed(2)}%</span>
                            </div>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">MSE:</span>
                              <span className="font-bold">{model.mse!.toFixed(4)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">RMSE:</span>
                              <span className="font-bold">{model.rmse!.toFixed(4)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">MAE:</span>
                              <span className="font-bold">{model.mae!.toFixed(4)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-muted-foreground">R² Score:</span>
                              <span className="font-bold">{model.r2_score!.toFixed(4)}</span>
                            </div>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </div>

                  <div className="flex gap-4">
                    <Button
                      onClick={() => {
                        setSessionId(null);
                        setDatasetInfo(null);
                        setFile(null);
                        setResults(null);
                        setTargetColumn("");
                        localStorage.removeItem("automl_session_id");
                      }}
                      size="lg"
                      variant="outline"
                      className="flex-1 border-neon-cyan text-neon-cyan hover:bg-neon-cyan/10"
                    >
                      Train Another Model
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Train;
