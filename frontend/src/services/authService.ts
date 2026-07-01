import { api } from "@/services/apiClient";
import type { TokenResponse, User } from "@/types/api";

/**
 * The backend's /auth/login endpoint uses FastAPI's OAuth2PasswordRequestForm,
 * which requires application/x-www-form-urlencoded, NOT JSON.
 */
export async function login(username: string, password: string): Promise<TokenResponse> {
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);

  const res = await api.post<TokenResponse>("/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
}

export async function fetchMe(): Promise<User> {
  const res = await api.get<User>("/users/me");
  return res.data;
}
