import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Building2,
  GitBranch,
  Users,
  Boxes,
  UtensilsCrossed,
  Calculator,
  ChefHat,
  Warehouse,
  FolderTree,
  Truck,
  ClipboardList,
} from "lucide-react";
import "./Sidebar.css";

const foundationLinks = [
  { to: "/", label: "الرئيسية", icon: LayoutDashboard },
  { to: "/companies", label: "الشركات", icon: Building2 },
  { to: "/branches", label: "الفروع", icon: GitBranch },
  { to: "/users", label: "المستخدمون", icon: Users },
];

const inventoryLinks = [
  { to: "/warehouses", label: "المخازن", icon: Warehouse },
  { to: "/categories", label: "تصنيفات المنتجات", icon: FolderTree },
  { to: "/products", label: "المنتجات", icon: Boxes },
];

const purchasingLinks = [
  { to: "/suppliers", label: "الموردون", icon: Truck },
  { to: "/purchase-orders", label: "أوامر الشراء", icon: ClipboardList },
];

const upcomingLinks = [
  { label: "نقاط البيع", icon: UtensilsCrossed },
  { label: "المحاسبة", icon: Calculator },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__brand-mark">
          <ChefHat size={20} />
        </span>
        <div>
          <p className="sidebar__brand-name">مدينة الشاورما</p>
          <p className="sidebar__brand-sub">إدارة المطاعم</p>
        </div>
      </div>

      <nav className="sidebar__nav">
        <p className="sidebar__section-label">الأساسيات</p>
        {foundationLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}

        <p className="sidebar__section-label sidebar__section-label--spaced">المخزون</p>
        {inventoryLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}

        <p className="sidebar__section-label sidebar__section-label--spaced">المشتريات</p>
        {purchasingLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}

        <p className="sidebar__section-label sidebar__section-label--spaced">قريبًا</p>
        {upcomingLinks.map(({ label, icon: Icon }) => (
          <div key={label} className="sidebar__link sidebar__link--disabled" title="هذا القسم غير متاح في هذه المرحلة">
            <Icon size={18} />
            <span>{label}</span>
            <span className="sidebar__badge">قريبًا</span>
          </div>
        ))}
      </nav>
    </aside>
  );
}
