import type { ReactNode } from "react";
import "@/theme/ticket-badge.css";

type BadgeTone = "active" | "inactive" | "warning" | "danger" | "info";

interface StatusBadgeProps {
  active: boolean;
  activeLabel?: string;
  inactiveLabel?: string;
}

/** Standard is_active -> ticket badge, used across every list screen. */
export function StatusBadge({ active, activeLabel = "نشط", inactiveLabel = "غير نشط" }: StatusBadgeProps) {
  return (
    <span className={`ticket-badge ticket-badge--${active ? "active" : "inactive"}`}>
      <span className="ticket-badge--dot" />
      {active ? activeLabel : inactiveLabel}
    </span>
  );
}

interface ToneBadgeProps {
  tone: BadgeTone;
  children: ReactNode;
}

export function ToneBadge({ tone, children }: ToneBadgeProps) {
  return (
    <span className={`ticket-badge ticket-badge--${tone}`}>
      <span className="ticket-badge--dot" />
      {children}
    </span>
  );
}
