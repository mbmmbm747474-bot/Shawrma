import { CheckCircle2, XCircle, Info, X } from "lucide-react";
import { useToastStore } from "@/store/toastStore";
import "./ToastContainer.css";

const ICONS = {
  success: CheckCircle2,
  error: XCircle,
  info: Info,
};

export function ToastContainer() {
  const { toasts, dismiss } = useToastStore();

  if (toasts.length === 0) return null;

  return (
    <div className="toast-container" role="status" aria-live="polite">
      {toasts.map((t) => {
        const Icon = ICONS[t.tone];
        return (
          <div key={t.id} className={`toast toast--${t.tone}`}>
            <Icon size={18} />
            <span className="toast__message">{t.message}</span>
            <button className="toast__close" onClick={() => dismiss(t.id)} aria-label="إغلاق">
              <X size={14} />
            </button>
          </div>
        );
      })}
    </div>
  );
}
