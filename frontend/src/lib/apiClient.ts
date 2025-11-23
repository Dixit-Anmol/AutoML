/**
 * API Client for AutoML Backend
 */
import type {
    UploadResponse,
    DatasetInfo,
    DatasetPreview,
    CleaningResponse,
    TrainingResponse,
    TrainingStatus,
    FillMethod,
    EncodingType,
    FilterType,
    ProblemType,
} from "@/types/api";
const API_BASE = "/api";
class APIClient {
    async uploadDataset(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${API_BASE}/upload/`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to upload file");
        }

        return response.json();
    }
    async getDatasetInfo(sessionId: string): Promise<DatasetInfo> {
        const response = await fetch(`${API_BASE}/upload/${sessionId}/info`);
        if (!response.ok) throw new Error("Failed to get dataset info");
        return response.json();
    }
    async getDatasetPreview(sessionId: string, rows: number = 10): Promise<DatasetPreview> {
        const response = await fetch(`${API_BASE}/upload/${sessionId}/preview?rows=${rows}`);
        if (!response.ok) throw new Error("Failed to get dataset preview");
        return response.json();
    }
    async downloadDataset(sessionId: string, cleaned: boolean = true): Promise<Blob> {
        const response = await fetch(`${API_BASE}/upload/${sessionId}/download?cleaned=${cleaned}`);
        if (!response.ok) throw new Error("Failed to download dataset");
        return response.blob();
    }
    async handleNulls(sessionId: string, operation: "remove" | "fill", columns?: string[], fillMethod?: FillMethod, customValue?: string): Promise<CleaningResponse> {
        const response = await fetch(`${API_BASE}/cleaning/nulls`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, operation, columns, fill_method: fillMethod, custom_value: customValue }),
        });
        if (!response.ok) throw new Error("Failed to handle nulls");
        return response.json();
    }
    async handleDuplicates(sessionId: string, columns?: string[]): Promise<CleaningResponse> {
        const response = await fetch(`${API_BASE}/cleaning/duplicates`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, operation: "remove", columns }),
        });
        if (!response.ok) throw new Error("Failed to handle duplicates");
        return response.json();
    }
    async encodeColumns(sessionId: string, columns: string[], encodingType: EncodingType): Promise<CleaningResponse> {
        const response = await fetch(`${API_BASE}/cleaning/encode`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, columns, encoding_type: encodingType }),
        });
        if (!response.ok) throw new Error("Failed to encode columns");
        return response.json();
    }
    async startTraining(sessionId: string, targetColumn: string, problemType: ProblemType, testSize: number = 0.2): Promise<TrainingStatus> {
        const response = await fetch(`${API_BASE}/training/train`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, target_column: targetColumn, problem_type: problemType, test_size: testSize }),
        });
        if (!response.ok) throw new Error("Failed to start training");
        return response.json();
    }
    async getTrainingStatus(sessionId: string): Promise<TrainingStatus> {
        const response = await fetch(`${API_BASE}/training/status/${sessionId}`);
        if (!response.ok) throw new Error("Failed to get training status");
        return response.json();
    }
    async getTrainingResults(sessionId: string): Promise<TrainingResponse> {
        const response = await fetch(`${API_BASE}/training/results/${sessionId}`);
        if (!response.ok) throw new Error("Failed to get training results");
        return response.json();
    }
}
export const apiClient = new APIClient();