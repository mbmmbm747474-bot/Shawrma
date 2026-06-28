import { api } from "@/services/apiClient";
import type { Company, CompanyCreateInput, CompanyUpdateInput } from "@/types/api";

export async function listCompanies(): Promise<Company[]> {
  const res = await api.get<Company[]>("/companies/");
  return res.data;
}

export async function getCompany(id: string): Promise<Company> {
  const res = await api.get<Company>(`/companies/${id}`);
  return res.data;
}

export async function createCompany(input: CompanyCreateInput): Promise<Company> {
  const res = await api.post<Company>("/companies/", input);
  return res.data;
}

export async function updateCompany(id: string, input: CompanyUpdateInput): Promise<Company> {
  const res = await api.put<Company>(`/companies/${id}`, input);
  return res.data;
}

export async function deleteCompany(id: string): Promise<void> {
  await api.delete(`/companies/${id}`);
}
