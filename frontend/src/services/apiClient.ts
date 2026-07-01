import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "@/store/authStore";
import type { ApiError, TokenResponse } from "@/types/api";

export const api = axios.create({
  baseURL: "/api/v1",
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});

let refreshPromise: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = useAuthStore.getState().refreshToken;
  if (!refreshToken) return null;

  try {
    const res = await axios.post<TokenResponse>("/api/v1/auth/refresh", null, {
      params: { refresh_token: refreshToken },
    });
    const { access_token, refresh_token } = res.data;
    useAuthStore.getState().setTokens(access_token, refresh_token);
    return access_token;
  } catch {
    useAuthStore.getState().logout();
    return null;
  }
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retried?: boolean };

    if (error.response?.status === 401 && original && !original._retried) {
      original._retried = true;

      if (!refreshPromise) {
        refreshPromise = refreshAccessToken().finally(() => {
          refreshPromise = null;
        });
      }

      const newToken = await refreshPromise;
      if (newToken) {
        original.headers.set("Authorization", `Bearer ${newToken}`);
        return api(original);
      }
    }

    return Promise.reject(error);
  },
);

/** Extracts a human-readable message from a FastAPI error response. */
export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError<ApiError>(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail.map((d) => d.msg).join("، ");
    }
  }
  return fallback;
}
