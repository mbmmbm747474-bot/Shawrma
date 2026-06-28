import { api } from "@/services/apiClient";
import type { User, UserCreateInput, UserUpdateInput } from "@/types/api";

export async function listUsers(): Promise<User[]> {
  const res = await api.get<User[]>("/users/");
  return res.data;
}

export async function getUser(id: string): Promise<User> {
  const res = await api.get<User>(`/users/${id}`);
  return res.data;
}

export async function createUser(input: UserCreateInput): Promise<User> {
  const res = await api.post<User>("/users/", input);
  return res.data;
}

export async function updateUser(id: string, input: UserUpdateInput): Promise<User> {
  const res = await api.put<User>(`/users/${id}`, input);
  return res.data;
}

export async function deleteUser(id: string): Promise<void> {
  await api.delete(`/users/${id}`);
}
