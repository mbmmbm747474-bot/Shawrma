import { api } from "@/services/apiClient";
import type { DashboardSummary } from "@/types/api";

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const res = await api.get<DashboardSummary>("/dashboard/summary");
  return res.data;
}
