import { useState, useEffect } from "react";
import { apiClient } from "@/lib/apiClient";
import type { CleaningStats, DatasetInfo, DatasetPreview } from "@/types/api";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

type CleaningStep = "upload" | "nulls" | "duplicates" | "convert" | "encode" | "filter" | "columns" | "download";

const CleanPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState<CleaningStep>("upload");
  const [datasetInfo, setDatasetInfo] = useState<DatasetInfo | null>(null);
  const [datasetPreview, setDatasetPreview] = useState<DatasetPreview | null>(null);
  const { toast } = useToast();

  // Load session from localStorage on mount
  useEffect(() => {
    const savedSessionId = localStorage.getItem("automl_session_id");
    if (savedSessionId) {
      setSessionId(savedSessionId);
      loadDatasetInfo(savedSessionId);
    }
  }, []);

  const loadDatasetInfo = async (sid: string) => {
    try {
      const info = await apiClient.getDatasetInfo(sid);
      setDatasetInfo(info);
      const preview = await apiClient.getDatasetPreview(sid, 10);
      setDatasetPreview(preview);
    } catch (error: any) {
      console.error("Failed to load dataset info:", error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsProcessing(true);
    try {
      const uploadResult = await apiClient.uploadDataset(file);
      setSessionId(uploadResult.session_id);
      setDatasetInfo(uploadResult.dataset_info);
      localStorage.setItem("automl_session_id", uploadResult.session_id);

      const preview = await apiClient.getDatasetPreview(uploadResult.session_id, 10);
      setDatasetPreview(preview);

      toast({
        title: "Upload Successful!",
        description: `${uploadResult.filename} uploaded successfully`
      });
      setCurrentStep("nulls");
    } catch (error: any) {
      toast({
        title: "Upload Failed",
        description: error.message,
        variant: "destructive"
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = async () => {
    if (!sessionId) return;

    try {
      const blob = await apiClient.downloadDataset(sessionId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "cleaned_dataset.csv";
      a.click();
      window.URL.revokeObjectURL(url);

      toast({
        title: "Download Complete",
        description: "Cleaned dataset downloaded successfully"
      });
    } catch (error: any) {
      toast({
        title: "Download Failed",
        description: error.message,
        variant: "destructive"
      });
    }
  };

  const refreshDatasetInfo = async () => {
    if (sessionId) {
      await loadDatasetInfo(sessionId);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden pt-24 pb-16">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-4">
            Clean Your Dataset
          </h1>
          <p className="text-xl text-muted-foreground">
            Upload your data and apply professional cleaning operations
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          {/* Upload Section */}
          {!sessionId && (
            <div className="relative group mb-8">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-cyan-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all" />
              <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-3xl p-8">
                <label className="block">
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <div className="border-2 border-dashed border-border rounded-2xl p-12 cursor-pointer hover:border-cyan-500 transition-all text-center">
                    <div className="text-6xl mb-6">📊</div>
                    <h3 className="text-2xl font-bold mb-2">
                      {file ? file.name : "Drop your dataset here"}
                    </h3>
                    <p className="text-muted-foreground">
                      {file
                        ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                        : "or click to browse (CSV, Excel)"}
                    </p>
                  </div>
                </label>

                {file && (
                  <div className="mt-6 flex justify-center">
                    <Button
                      onClick={handleUpload}
                      disabled={isProcessing}
                      size="lg"
                      className="bg-gradient-to-r from-red-400 via-orange-400 to-pink-400 text-white px-8 py-6 text-lg"
                    >
                      {isProcessing ? "Uploading..." : "Upload & Start Cleaning"}
                    </Button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Dataset Info Card */}
          {sessionId && datasetInfo && (
            <div className="mb-8 relative">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-2xl blur-xl" />
              <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-bold">Dataset Overview</h3>
                  <Button
                    onClick={refreshDatasetInfo}
                    variant="outline"
                    size="sm"
                  >
                    🔄 Refresh
                  </Button>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="bg-secondary/50 rounded-xl p-4 text-center">
                    <p className="text-3xl font-bold text-primary">{datasetInfo.rows}</p>
                    <p className="text-sm text-muted-foreground">Rows</p>
                  </div>
                  <div className="bg-secondary/50 rounded-xl p-4 text-center">
                    <p className="text-3xl font-bold text-primary">{datasetInfo.columns}</p>
                    <p className="text-sm text-muted-foreground">Columns</p>
                  </div>
                  <div className="bg-secondary/50 rounded-xl p-4 text-center">
                    <p className="text-3xl font-bold text-accent">{datasetInfo.total_nulls}</p>
                    <p className="text-sm text-muted-foreground">Null Values</p>
                  </div>
                  <div className="bg-secondary/50 rounded-xl p-4 text-center">
                    <p className="text-3xl font-bold text-accent">{datasetInfo.total_duplicates}</p>
                    <p className="text-sm text-muted-foreground">Duplicates</p>
                  </div>
                  <div className="bg-secondary/50 rounded-xl p-4 text-center">
                    <p className="text-3xl font-bold text-primary">{datasetInfo.memory_mb.toFixed(2)}</p>
                    <p className="text-sm text-muted-foreground">MB</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Cleaning Operations Tabs */}
          {sessionId && (
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-cyan-500/10 rounded-2xl blur-xl" />
              <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-2xl p-6">
                <Tabs value={currentStep} onValueChange={(v) => setCurrentStep(v as CleaningStep)}>
                  <TabsList className="grid grid-cols-7 w-full mb-6">
                    <TabsTrigger value="nulls">Nulls</TabsTrigger>
                    <TabsTrigger value="duplicates">Duplicates</TabsTrigger>
                    <TabsTrigger value="convert">Convert</TabsTrigger>
                    <TabsTrigger value="encode">Encode</TabsTrigger>
                    <TabsTrigger value="filter">Filter</TabsTrigger>
                    <TabsTrigger value="columns">Columns</TabsTrigger>
                    <TabsTrigger value="download">Download</TabsTrigger>
                  </TabsList>

                  <TabsContent value="nulls">
                    <NullsTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="duplicates">
                    <DuplicatesTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="convert">
                    <ConvertTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="encode">
                    <EncodeTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="filter">
                    <FilterTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="columns">
                    <ColumnsTab sessionId={sessionId} datasetInfo={datasetInfo} onUpdate={refreshDatasetInfo} />
                  </TabsContent>

                  <TabsContent value="download">
                    <DownloadTab sessionId={sessionId} onDownload={handleDownload} onReset={() => {
                      setSessionId(null);
                      setDatasetInfo(null);
                      setFile(null);
                      localStorage.removeItem("automl_session_id");
                    }} />
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Component for handling null values
const NullsTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [operation, setOperation] = useState<"remove" | "fill">("fill");
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [fillMethod, setFillMethod] = useState<"mean" | "median" | "mode" | "ffill" | "bfill" | "custom">("mean");
  const [customValue, setCustomValue] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleNulls = async () => {
    setIsProcessing(true);
    try {
      const result = await apiClient.handleNulls(
        sessionId,
        operation,
        selectedColumns.length > 0 ? selectedColumns : undefined,
        operation === "fill" ? fillMethod : undefined,
        fillMethod === "custom" ? customValue : undefined
      );

      toast({ title: "Success!", description: result.message });
      onUpdate();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  if (!datasetInfo || datasetInfo.total_nulls === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">✅</div>
        <h3 className="text-2xl font-bold">No Null Values Found!</h3>
        <p className="text-muted-foreground">Your dataset is clean</p>
      </div>
    );
  }

  const columnsWithNulls = Object.keys(datasetInfo.column_types); // Simplified - you may need more logic

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Operation</label>
        <Select value={operation} onValueChange={(v: any) => setOperation(v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="remove">Remove Rows with Nulls</SelectItem>
            <SelectItem value="fill">Fill Null Values</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {operation === "fill" && (
        <>
          <div>
            <label className="block text-sm font-medium mb-2">Fill Method</label>
            <Select value={fillMethod} onValueChange={(v: any) => setFillMethod(v)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="mean">Mean (numeric only)</SelectItem>
                <SelectItem value="median">Median (numeric only)</SelectItem>
                <SelectItem value="mode">Mode (most frequent)</SelectItem>
                <SelectItem value="ffill">Forward Fill</SelectItem>
                <SelectItem value="bfill">Backward Fill</SelectItem>
                <SelectItem value="custom">Custom Value</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {fillMethod === "custom" && (
            <div>
              <label className="block text-sm font-medium mb-2">Custom Value</label>
              <input
                type="text"
                value={customValue}
                onChange={(e) => setCustomValue(e.target.value)}
                className="w-full px-4 py-2 rounded-lg border border-border bg-background"
                placeholder="Enter custom value"
              />
            </div>
          )}
        </>
      )}

      <Button
        onClick={handleNulls}
        disabled={isProcessing}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Processing..." : `Apply ${operation === "remove" ? "Remove" : "Fill"}`}
      </Button>
    </div>
  );
};

// Component for handling duplicates
const DuplicatesTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleDuplicates = async () => {
    setIsProcessing(true);
    try {
      const result = await apiClient.handleDuplicates(sessionId);
      toast({ title: "Success!", description: result.message });
      onUpdate();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  if (!datasetInfo || datasetInfo.total_duplicates === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">✅</div>
        <h3 className="text-2xl font-bold">No Duplicates Found!</h3>
        <p className="text-muted-foreground">Your dataset is clean</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-secondary/50 rounded-xl p-6 text-center">
        <p className="text-4xl font-bold text-accent mb-2">{datasetInfo.total_duplicates}</p>
        <p className="text-muted-foreground">Duplicate rows found</p>
      </div>

      <Button
        onClick={handleDuplicates}
        disabled={isProcessing}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Removing..." : "Remove All Duplicates"}
      </Button>
    </div>
  );
};

// Component for data type conversion
const ConvertTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [selectedColumn, setSelectedColumn] = useState("");
  const [targetType, setTargetType] = useState<"int64" | "float64" | "object" | "bool" | "datetime64[ns]">("int64");
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleConvert = async () => {
    if (!selectedColumn) {
      toast({ title: "Error", description: "Please select a column", variant: "destructive" });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await apiClient.convertDataType(sessionId, selectedColumn, targetType);
      toast({ title: "Success!", description: result.message });
      onUpdate();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  const columns = datasetInfo ? Object.keys(datasetInfo.column_types) : [];

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Select Column</label>
        <Select value={selectedColumn} onValueChange={setSelectedColumn}>
          <SelectTrigger>
            <SelectValue placeholder="Choose a column" />
          </SelectTrigger>
          <SelectContent>
            {columns.map((col: string) => (
              <SelectItem key={col} value={col}>
                {col} ({datasetInfo.column_types[col]})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Target Data Type</label>
        <Select value={targetType} onValueChange={(v: any) => setTargetType(v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="int64">Integer</SelectItem>
            <SelectItem value="float64">Float</SelectItem>
            <SelectItem value="object">String</SelectItem>
            <SelectItem value="bool">Boolean</SelectItem>
            <SelectItem value="datetime64[ns]">DateTime</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button
        onClick={handleConvert}
        disabled={isProcessing}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Converting..." : "Convert Data Type"}
      </Button>
    </div>
  );
};

// Component for encoding columns
const EncodeTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [encodingType, setEncodingType] = useState<"label" | "onehot" | "ordinal">("label");
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleEncode = async () => {
    if (selectedColumns.length === 0) {
      toast({ title: "Error", description: "Please select at least one column", variant: "destructive" });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await apiClient.encodeColumns(sessionId, selectedColumns, encodingType);
      toast({ title: "Success!", description: result.message });
      onUpdate();
      setSelectedColumns([]);
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  const categoricalColumns = datasetInfo
    ? Object.keys(datasetInfo.column_types).filter((col: string) =>
      datasetInfo.column_types[col] === "object" || datasetInfo.column_types[col] === "string"
    )
    : [];

  if (categoricalColumns.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">ℹ️</div>
        <h3 className="text-2xl font-bold">No Categorical Columns</h3>
        <p className="text-muted-foreground">All columns are already numeric</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Encoding Type</label>
        <Select value={encodingType} onValueChange={(v: any) => setEncodingType(v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="label">Label Encoding (0, 1, 2...)</SelectItem>
            <SelectItem value="onehot">One-Hot Encoding (binary columns)</SelectItem>
            <SelectItem value="ordinal">Ordinal Encoding</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Categorical Columns</label>
        <div className="space-y-2 max-h-48 overflow-y-auto border border-border rounded-lg p-3">
          {categoricalColumns.map((col: string) => (
            <label key={col} className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={selectedColumns.includes(col)}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedColumns([...selectedColumns, col]);
                  } else {
                    setSelectedColumns(selectedColumns.filter(c => c !== col));
                  }
                }}
                className="w-4 h-4"
              />
              <span>{col}</span>
            </label>
          ))}
        </div>
      </div>

      <Button
        onClick={handleEncode}
        disabled={isProcessing || selectedColumns.length === 0}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Encoding..." : `Encode ${selectedColumns.length} Column(s)`}
      </Button>
    </div>
  );
};

// Component for filtering data
const FilterTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [selectedColumn, setSelectedColumn] = useState("");
  const [filterType, setFilterType] = useState<"range" | "gt" | "lt" | "eq" | "in">("range");
  const [minValue, setMinValue] = useState("");
  const [maxValue, setMaxValue] = useState("");
  const [value, setValue] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleFilter = async () => {
    if (!selectedColumn) {
      toast({ title: "Error", description: "Please select a column", variant: "destructive" });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await apiClient.filterData(
        sessionId,
        selectedColumn,
        filterType,
        value ? parseFloat(value) : undefined,
        minValue ? parseFloat(minValue) : undefined,
        maxValue ? parseFloat(maxValue) : undefined
      );
      toast({ title: "Success!", description: result.message });
      onUpdate();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  const numericColumns = datasetInfo
    ? Object.keys(datasetInfo.column_types).filter((col: string) =>
      datasetInfo.column_types[col].includes("int") || datasetInfo.column_types[col].includes("float")
    )
    : [];

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Select Column</label>
        <Select value={selectedColumn} onValueChange={setSelectedColumn}>
          <SelectTrigger>
            <SelectValue placeholder="Choose a numeric column" />
          </SelectTrigger>
          <SelectContent>
            {numericColumns.map((col: string) => (
              <SelectItem key={col} value={col}>
                {col}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Filter Type</label>
        <Select value={filterType} onValueChange={(v: any) => setFilterType(v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="range">Range (Min-Max)</SelectItem>
            <SelectItem value="gt">Greater Than</SelectItem>
            <SelectItem value="lt">Less Than</SelectItem>
            <SelectItem value="eq">Equal To</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {filterType === "range" && (
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Min Value</label>
            <input
              type="number"
              value={minValue}
              onChange={(e) => setMinValue(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-border bg-background"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Max Value</label>
            <input
              type="number"
              value={maxValue}
              onChange={(e) => setMaxValue(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-border bg-background"
            />
          </div>
        </div>
      )}

      {filterType !== "range" && (
        <div>
          <label className="block text-sm font-medium mb-2">Value</label>
          <input
            type="number"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            className="w-full px-4 py-2 rounded-lg border border-border bg-background"
          />
        </div>
      )}

      <Button
        onClick={handleFilter}
        disabled={isProcessing}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Filtering..." : "Apply Filter"}
      </Button>
    </div>
  );
};

// Component for column management
const ColumnsTab = ({ sessionId, datasetInfo, onUpdate }: any) => {
  const [operation, setOperation] = useState<"drop" | "rename">("drop");
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleColumnsOp = async () => {
    if (operation === "drop" && selectedColumns.length === 0) {
      toast({ title: "Error", description: "Please select columns to drop", variant: "destructive" });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await apiClient.manageColumns(
        sessionId,
        operation,
        operation === "drop" ? selectedColumns : undefined
      );
      toast({ title: "Success!", description: result.message });
      onUpdate();
      setSelectedColumns([]);
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setIsProcessing(false);
    }
  };

  const columns = datasetInfo ? Object.keys(datasetInfo.column_types) : [];

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">Operation</label>
        <Select value={operation} onValueChange={(v: any) => setOperation(v)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="drop">Drop Columns</SelectItem>
            <SelectItem value="rename">Rename Columns</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {operation === "drop" && (
        <div>
          <label className="block text-sm font-medium mb-2">Select Columns to Drop</label>
          <div className="space-y-2 max-h-48 overflow-y-auto border border-border rounded-lg p-3">
            {columns.map((col: string) => (
              <label key={col} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedColumns.includes(col)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedColumns([...selectedColumns, col]);
                    } else {
                      setSelectedColumns(selectedColumns.filter(c => c !== col));
                    }
                  }}
                  className="w-4 h-4"
                />
                <span>{col}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      <Button
        onClick={handleColumnsOp}
        disabled={isProcessing}
        className="w-full bg-gradient-to-r from-red-400 via-orange-400 to-pink-400"
      >
        {isProcessing ? "Processing..." : `${operation === "drop" ? "Drop" : "Rename"} Columns`}
      </Button>
    </div>
  );
};

// Component for download
const DownloadTab = ({ sessionId, onDownload, onReset }: any) => {
  return (
    <div className="space-y-6 text-center py-8">
      <div className="text-6xl mb-4">✨</div>
      <h3 className="text-3xl font-bold gradient-text">Dataset Cleaned!</h3>
      <p className="text-muted-foreground text-lg">Your dataset is ready for download or model training</p>

      <div className="flex gap-4 max-w-md mx-auto">
        <Button
          onClick={onDownload}
          className="flex-1 bg-gradient-to-r from-cyan-500 to-purple-500 text-white px-6 py-6 text-lg"
        >
          📥 Download Cleaned Data
        </Button>
        <Button
          onClick={onReset}
          variant="outline"
          className="border-2 border-cyan-500 text-cyan-500 px-6 py-6 text-lg"
        >
          Upload Another
        </Button>
      </div>
    </div>
  );
};

export default CleanPage;