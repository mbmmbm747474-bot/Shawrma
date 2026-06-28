import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LoginPage } from "@/pages/LoginPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { CompaniesPage } from "@/pages/companies/CompaniesPage";
import { BranchesPage } from "@/pages/branches/BranchesPage";
import { UsersPage } from "@/pages/users/UsersPage";
import { WarehousesPage } from "@/pages/warehouses/WarehousesPage";
import { CategoriesPage } from "@/pages/categories/CategoriesPage";
import { ProductsPage } from "@/pages/products/ProductsPage";
import { SuppliersPage } from "@/pages/suppliers/SuppliersPage";
import { PurchaseOrdersPage } from "@/pages/purchase-orders/PurchaseOrdersPage";
import { AppLayout } from "@/layouts/AppLayout";
import { ProtectedRoute } from "@/routes/ProtectedRoute";
import { ToastContainer } from "@/components/ui/ToastContainer";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/" element={<DashboardPage />} />
            <Route path="/companies" element={<CompaniesPage />} />
            <Route path="/branches" element={<BranchesPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/warehouses" element={<WarehousesPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/suppliers" element={<SuppliersPage />} />
            <Route path="/purchase-orders" element={<PurchaseOrdersPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>

      <ToastContainer />
    </QueryClientProvider>
  );
}
