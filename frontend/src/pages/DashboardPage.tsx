import { useQuery } from "@tanstack/react-query";
import {
  Bell,
  Boxes,
  ClipboardList,
  Clock,
  CreditCard,
  DollarSign,
  Receipt,
  ShieldAlert,
  ShoppingCart,
  TrendingUp,
  User,
  Users,
  Wallet,
} from "lucide-react";
import { fetchDashboardSummary } from "@/services/dashboardService";
import { Card } from "@/components/ui/Card";
import { PageSpinner } from "@/components/ui/EmptyState";
import "./DashboardPage.css";

const METRICS = [
  {
    label: "مبيعات اليوم",
    value: "12,450 ج.م",
    icon: DollarSign,
    tone: "saffron",
  },
  {
    label: "مبيعات الشهر",
    value: "325,800 ج.م",
    icon: TrendingUp,
    tone: "sky",
  },
  {
    label: "صافي الربح",
    value: "89,200 ج.م",
    icon: Wallet,
    tone: "olive",
  },
  {
    label: "قيمة المخزون",
    value: "142,500 ج.م",
    icon: Boxes,
    tone: "brick",
  },
  {
    label: "عدد الفواتير",
    value: "318",
    icon: Receipt,
    tone: "saffron",
  },
  {
    label: "أصناف منخفضة المخزون",
    value: "14",
    icon: ShieldAlert,
    tone: "brick",
  },
];

const weeklySales = [65, 80, 72, 95, 88, 120, 110];
const monthlySales = [45, 60, 72, 85, 90, 110, 125, 140, 132, 150, 170, 190];
const topCategories = [
  { name: "الشاورما", value: 40 },
  { name: "الوجبات", value: 28 },
  { name: "المشروبات", value: 18 },
  { name: "الحلويات", value: 14 },
];
const paymentMethods = [
  { name: "نقدي", value: 55 },
  { name: "بطاقة", value: 30 },
  { name: "محفظة", value: 15 },
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
    <div className="dashboard-modern">
      <div className="dashboard-topbar">
        <div className="dashboard-brand">
          <div className="dashboard-brand__logo">🍽️</div>
          <div>
            <h1 className="dashboard-brand__title">Shawrma City ERP</h1>
            <p className="dashboard-brand__subtitle">لوحة تحكم احترافية للمطاعم</p>
          </div>
        </div>

        <div className="dashboard-topbar__actions">
          <div className="dashboard-time">
            <Clock size={18} />
            <div>
              <strong>الوقت الحالي</strong>
              <span>{new Date().toLocaleString("ar-EG")}</span>
            </div>
          </div>

          <button className="dashboard-icon-btn" aria-label="الإشعارات">
            <Bell size={18} />
          </button>

          <button className="dashboard-profile-btn">
            <User size={18} />
            <span>المستخدم الحالي</span>
          </button>
        </div>
      </div>

      <div className="dashboard-metrics-grid">
        {METRICS.map(({ label, value, icon: Icon, tone }) => (
          <div key={label} className={`dashboard-metric-card dashboard-metric-card--${tone}`}>
            <div className="dashboard-metric-card__icon">
              <Icon size={24} />
            </div>
            <div>
              <p className="dashboard-metric-card__label">{label}</p>
              <p className="dashboard-metric-card__value">{value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-charts-grid">
        <Card className="dashboard-chart-card">
          <div className="dashboard-section-title">
            <TrendingUp size={18} />
            <span>مبيعات آخر 7 أيام</span>
          </div>

          <div className="mini-bars">
            {weeklySales.map((value, index) => (
              <div key={index} className="mini-bars__item">
                <div className="mini-bars__bar" style={{ height: `${value}%` }} />
                <span>يوم {index + 1}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="dashboard-chart-card">
          <div className="dashboard-section-title">
            <TrendingUp size={18} />
            <span>مبيعات الأشهر</span>
          </div>

          <div className="line-chart-placeholder">
            <div className="line-chart-placeholder__line" />
            <div className="line-chart-placeholder__points">
              {monthlySales.map((value, index) => (
                <span key={index} style={{ bottom: `${value / 2}%`, left: `${(index / 11) * 100}%` }} />
              ))}
            </div>
          </div>
        </Card>
      </div>

      <div className="dashboard-charts-grid">
        <Card className="dashboard-chart-card">
          <div className="dashboard-section-title">
            <ShoppingCart size={18} />
            <span>أفضل الفئات</span>
          </div>

          <div className="progress-list">
            {topCategories.map((item) => (
              <div key={item.name} className="progress-item">
                <div className="progress-item__header">
                  <span>{item.name}</span>
                  <span>{item.value}%</span>
                </div>
                <div className="progress-item__bar">
                  <div style={{ width: `${item.value}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="dashboard-chart-card">
          <div className="dashboard-section-title">
            <CreditCard size={18} />
            <span>توزيع طرق الدفع</span>
          </div>

          <div className="payment-chart">
            {paymentMethods.map((item) => (
              <div key={item.name} className="payment-chart__item">
                <div className="payment-chart__circle">{item.value}%</div>
                <span>{item.name}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="dashboard-lists-grid">
        <Card>
          <div className="dashboard-section-title">
            <Receipt size={18} />
            <span>آخر الفواتير</span>
          </div>

          <table className="dashboard-table">
            <thead>
              <tr>
                <th>الرقم</th>
                <th>العميل</th>
                <th>القيمة</th>
                <th>الحالة</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>INV-1001</td>
                <td>عميل نقدي</td>
                <td>450 ج.م</td>
                <td><span className="status status--paid">مدفوعة</span></td>
              </tr>
              <tr>
                <td>INV-1002</td>
                <td>محمد علي</td>
                <td>820 ج.م</td>
                <td><span className="status status--paid">مدفوعة</span></td>
              </tr>
              <tr>
                <td>INV-1003</td>
                <td>أحمد حسن</td>
                <td>1,120 ج.م</td>
                <td><span className="status status--pending">معلقة</span></td>
              </tr>
            </tbody>
          </table>
        </Card>

        <Card>
          <div className="dashboard-section-title">
            <ShoppingCart size={18} />
            <span>أكثر 10 أصناف مبيعًا</span>
          </div>

          <ul className="dashboard-list">
            <li><span>شاورما دجاج</span><strong>320</strong></li>
            <li><span>شاورما لحم</span><strong>280</strong></li>
            <li><span>بطاطس</span><strong>240</strong></li>
            <li><span>بيبسي</span><strong>190</strong></li>
            <li><span>وجبة عائلية</span><strong>150</strong></li>
          </ul>
        </Card>
      </div>

      <div className="dashboard-lists-grid dashboard-lists-grid--three">
        <Card>
          <div className="dashboard-section-title">
            <Users size={18} />
            <span>تنبيهات الموردين</span>
          </div>

          <ul className="dashboard-alerts">
            <li>مورد اللحوم لم يسلّم الطلبية المجدولة.</li>
            <li>تأخر دفع فاتورة مورد الخضروات.</li>
            <li>طلب شراء جديد يحتاج اعتماد.</li>
          </ul>
        </Card>

        <Card>
          <div className="dashboard-section-title">
            <ShieldAlert size={18} />
            <span>تنبيهات انتهاء الصلاحية</span>
          </div>

          <ul className="dashboard-alerts">
            <li>صلصة الثوم تنتهي خلال 3 أيام.</li>
            <li>الجبنة تنتهي خلال 5 أيام.</li>
            <li>المشروبات الغازية تنتهي خلال أسبوع.</li>
          </ul>
        </Card>

        <Card>
          <div className="dashboard-section-title">
            <ClipboardList size={18} />
            <span>طلبات قيد التنفيذ</span>
          </div>

          <ul className="dashboard-alerts">
            <li>طلب رقم #205 - جاري التحضير.</li>
            <li>طلب رقم #206 - بانتظار الدفع.</li>
            <li>طلب رقم #207 - جاهز للتسليم.</li>
          </ul>
        </Card>
      </div>
    </div>
  );
}
