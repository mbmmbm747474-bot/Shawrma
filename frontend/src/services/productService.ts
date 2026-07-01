import { api } from "@/services/apiClient";
import type { Product, ProductCreateInput, ProductUpdateInput } from "@/types/api";

export async function listProducts(categoryId?: string): Promise<Product[]> {
  const res = await api.get<Product[]>("/products/", {
    params: categoryId ? { category_id: categoryId } : undefined,
  });
  return res.data;
}

export async function createProduct(input: ProductCreateInput): Promise<Product> {
  const res = await api.post<Product>("/products/", input);
  return res.data;
}

export async function updateProduct(id: string, input: ProductUpdateInput): Promise<Product> {
  const res = await api.put<Product>(`/products/${id}`, input);
  return res.data;
}

export async function deleteProduct(id: string): Promise<void> {
  await api.delete(`/products/${id}`);
}
