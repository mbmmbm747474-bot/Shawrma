import { api } from "@/services/apiClient";
import type {
  ProductCategory,
  ProductCategoryCreateInput,
  ProductCategoryUpdateInput,
} from "@/types/api";

export async function listCategories(): Promise<ProductCategory[]> {
  const res = await api.get<ProductCategory[]>("/product-categories/");
  return res.data;
}

export async function createCategory(input: ProductCategoryCreateInput): Promise<ProductCategory> {
  const res = await api.post<ProductCategory>("/product-categories/", input);
  return res.data;
}

export async function updateCategory(
  id: string,
  input: ProductCategoryUpdateInput,
): Promise<ProductCategory> {
  const res = await api.put<ProductCategory>(`/product-categories/${id}`, input);
  return res.data;
}

export async function deleteCategory(id: string): Promise<void> {
  await api.delete(`/product-categories/${id}`);
}
