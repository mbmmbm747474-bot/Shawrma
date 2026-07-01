import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import "./AppLayout.css";

const TITLES: Record<string, string> = {
  "/": "نظرة عامة",
  "/companies": "الشركات",
  "/branches": "الفروع",
  "/users": "المستخدمون",
  "/warehouses": "المخازن",
  "/categories": "تصنيفات المنتجات",
  "/products": "المنتجات",
  "/suppliers": "الموردون",
  "/purchase-orders": "أوامر الشراء",
};

function resolveTitle(pathname: string): string {
  if (TITLES[pathname]) return TITLES[pathname];
  const base = "/" + pathname.split("/")[1];
  return TITLES[base] ?? "مدينة الشاورما";
}

export function AppLayout() {
  const location = useLocation();

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="app-layout__main">
        <Topbar title={resolveTitle(location.pathname)} />
        <main className="app-layout__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
