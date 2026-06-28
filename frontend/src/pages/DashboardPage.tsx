import { useQuery } from "@tanstack/react-query";
import { Building2, GitBranch, Users, Boxes, Truck, UserSquare2, ClipboardList, Receipt } from "lucide-react";
import { fetchDashboardSummary } from "@/services/dashboardService";
import { Card } from "@/components/ui/Card";
import { PageSpinner } from "@/components/ui/EmptyState";
import "./DashboardPage.css";

const METRICS: {
  key: keyof Awaited<ReturnType<typeof fetchDashboardSummary>>;
  label: string;
  icon: typeof Building2;
  tone: "saffron" | "olive" | "sky" | "brick";
}[] = [
  { key: "companies_count", label: "الشركات", icon: Building2, tone: "saffron" },
  { key: "branches_count", label: "الفروع", icon: GitBranch, tone: "sky" },
  { key: "users_count", label: "المستخدمون", icon: Users, tone: "olive" },
  { key: "products_count", label: "المنتجات", icon: Boxes, tone: "saffron" },
  { key: "suppliers_count", label: "الموردون", icon: Truck, tone: "sky" },
  { key: "customers_count", label: "العملاء", icon: UserSquare2, tone: "olive" },
  { key: "open_purchase_orders", label: "أوامر شراء مفتوحة", icon: ClipboardList, tone: "brick" },
  { key: "unpaid_sales_invoices", label: "فواتير غير مدفوعة", icon: Receipt, tone: "brick" },
];

export function DashboardPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: fetchDashboardSummary,
  });

  if (isLoading) return <PageSpinner />;

  if (isError || !data) {
    return (
      <Card>
        <p style={{ color: "var(--color-brick)", margin: 0 }}>
          تعذّر تحميل بيانات لوحة التحكم. حاول إعادة تحميل الصفحة.
        </p>
      </Card>
    );
  }

  return (
    <div>
      <p className="dashboard-intro">نظرة سريعة على حالة النظام الآن.</p>

      <div className="metric-grid">
        {METRICS.map(({ key, label, icon: Icon, tone }) => (
          <div key={key} className={`metric-card metric-card--${tone}`}>
            <div className="metric-card__icon">
              <Icon size={20} />
            </div>
            <div>
              <p className="metric-card__value numeric">{data[key]}</p>
              <p className="metric-card__label">{label}</p>
            </div>
          </div>
        ))}
      </div>

      <Card className="dashboard-note">
        <p style={{ margin: 0, color: "var(--color-ink-soft)", fontSize: "var(--text-sm)" }}>
          هذه المرحلة من النظام تشمل الشركات والفروع والمستخدمين فقط. وحدات المخزون والمشتريات ونقاط
          البيع والمحاسبة قيد التطوير وستظهر أرقامها هنا تلقائيًا عند تفعيلها.
        </p>
      </Card>
    </div>
  );
}
