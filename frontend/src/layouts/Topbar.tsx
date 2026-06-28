import { useState } from "react";
import { LogOut, ChevronDown, User as UserIcon } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import "./Topbar.css";

interface TopbarProps {
  title: string;
}

export function Topbar({ title }: TopbarProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <header className="topbar">
      <h1 className="topbar__title">{title}</h1>

      <div className="topbar__user">
        <button className="topbar__user-trigger" onClick={() => setMenuOpen((v) => !v)}>
          <span className="topbar__avatar">
            <UserIcon size={16} />
          </span>
          <span className="topbar__user-name">{user?.full_name ?? "—"}</span>
          <ChevronDown size={14} />
        </button>

        {menuOpen && (
          <>
            <div className="topbar__menu-backdrop" onClick={() => setMenuOpen(false)} />
            <div className="topbar__menu">
              <div className="topbar__menu-header">
                <p className="topbar__menu-name">{user?.full_name}</p>
                <p className="topbar__menu-email ltr-field">{user?.email}</p>
              </div>
              <button className="topbar__menu-item" onClick={handleLogout}>
                <LogOut size={16} />
                تسجيل الخروج
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
