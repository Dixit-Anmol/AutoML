import { useState, useEffect } from "react";
import { apiClient } from "@/lib/apiClient";
import type { DatasetPreview } from "@/types/api";
import { Slider } from "@/components/ui/slider";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface DataPreviewProps {
    sessionId: string;
    refreshTrigger?: number;
}

export const DataPreview = ({ sessionId, refreshTrigger = 0 }: DataPreviewProps) => {
    const [previewRowCount, setPreviewRowCount] = useState(5);
    const [previewData, setPreviewData] = useState<DatasetPreview | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchPreview = async () => {
            setIsLoading(true);
            try {
                const data = await apiClient.getDatasetPreview(sessionId, previewRowCount);
                setPreviewData(data);
            } catch (error) {
                console.error("Failed to fetch preview:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchPreview();
    }, [sessionId, previewRowCount, refreshTrigger]);

    if (!previewData || !previewData.head || previewData.head.length === 0) {
        return (
            <div className="text-center py-8 text-muted-foreground">
                {isLoading ? "Loading preview..." : "No preview available"}
            </div>
        );
    }

    const columns = Object.keys(previewData.head[0]);
    const rows = previewData.head;

    return (
        <div className="space-y-4 mt-6">
            <div className="bg-secondary/30 rounded-xl p-4">
                <div className="flex items-center justify-between mb-3">
                    <label className="text-sm font-medium">Preview Rows</label>
                    <span className="text-sm font-bold text-primary">{previewRowCount} rows</span>
                </div>
                <Slider
                    value={[previewRowCount]}
                    onValueChange={(value) => setPreviewRowCount(value[0])}
                    min={1}
                    max={50}
                    step={1}
                    className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-2">
                    <span>1</span>
                    <span>50</span>
                </div>
            </div>

            <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-br from-orange-500/10 to-pink-500/10 rounded-xl blur-lg" />
                <div className="relative bg-card/80 backdrop-blur-xl border border-border rounded-xl p-4">
                    <h4 className="text-lg font-semibold mb-3 gradient-text">📊 Data Preview</h4>
                    {isLoading ? (
                        <div className="text-center py-8 text-muted-foreground">Loading...</div>
                    ) : (
                        <div className="max-h-96 overflow-auto rounded-lg border border-border">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        {columns.map((col: string, idx: number) => (
                                            <TableHead key={idx} className="font-bold bg-secondary/50">
                                                {col}
                                            </TableHead>
                                        ))}
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {rows.map((row: Record<string, any>, rowIdx: number) => (
                                        <TableRow key={rowIdx}>
                                            {columns.map((col: string, cellIdx: number) => (
                                                <TableCell key={cellIdx} className="font-mono text-sm">
                                                    {row[col] === null || row[col] === undefined ? (
                                                        <span className="text-muted-foreground italic">null</span>
                                                    ) : (
                                                        String(row[col])
                                                    )}
                                                </TableCell>
                                            ))}
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
