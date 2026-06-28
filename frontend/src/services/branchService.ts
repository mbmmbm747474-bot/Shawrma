import { api } from "@/services/apiClient";
import type { Branch, BranchCreateInput, BranchUpdateInput } from "@/types/api";

export async function listBranches(companyId?: string): Promise<Branch[]> {
  const res = await api.get<Branch[]>("/branches/", {
    params: companyId ? { company_id: companyId } : undefined,
  });
  return res.data;
}

export async function getBranch(id: string): Promise<Branch> {
  const res = await api.get<Branch>(`/branches/${id}`);
  return res.data;
}

export async function createBranch(input: BranchCreateInput): Promise<Branch> {
  const res = await api.post<Branch>("/branches/", input);
  return res.data;
}

export async function updateBranch(id: string, input: BranchUpdateInput): Promise<Branch> {
  const res = await api.put<Branch>(`/branches/${id}`, input);
  return res.data;
}

export async function deleteBranch(id: string): Promise<void> {
  await api.delete(`/branches/${id}`);
}
