import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useForm } from "react-hook-form";
import { ChefHat, Eye, EyeOff } from "lucide-react";
import { login, fetchMe } from "@/services/authService";
import { useAuthStore } from "@/store/authStore";
import { getApiErrorMessage } from "@/services/apiClient";
import { Button } from "@/components/ui/Button";
import "./LoginPage.css";

interface LoginFormValues {
  username: string;
  password: string;
}

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const setTokens = useAuthStore((s) => s.setTokens);
  const setUser = useAuthStore((s) => s.setUser);

  const [showPassword, setShowPassword] = useState(false);
  const [serverError, setServerError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>();

  async function onSubmit(values: LoginFormValues) {
    setServerError(null);
    setSubmitting(true);
    try {
      const tokens = await login(values.username, values.password);
      setTokens(tokens.access_token, tokens.refresh_token);
      const me = await fetchMe();
      setUser(me);

      const redirectTo = (location.state as { from?: string } | null)?.from ?? "/";
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setServerError(getApiErrorMessage(err, "اسم المستخدم أو كلمة المرور غير صحيحة"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-page__pattern" aria-hidden="true" />

      <div className="login-card">
        <div className="login-card__brand">
          <span className="login-card__mark">
            <ChefHat size={26} />
          </span>
          <div>
            <p className="login-card__brand-name">مدينة الشاورما</p>
            <p className="login-card__brand-sub">نظام إدارة المطاعم</p>
          </div>
        </div>

        <h2 className="login-card__heading">تسجيل الدخول</h2>
        <p className="login-card__subheading">أدخل بيانات حسابك للوصول إلى لوحة التحكم</p>

        {serverError && <div className="login-card__error">{serverError}</div>}

        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="field">
            <label htmlFor="username" className="field__label">
              اسم المستخدم
            </label>
            <input
              id="username"
              className="field__input ltr-field"
              autoComplete="username"
              autoFocus
              {...register("username", { required: "اسم المستخدم مطلوب" })}
            />
            {errors.username && <p className="field__error">{errors.username.message}</p>}
          </div>

          <div className="field">
            <label htmlFor="password" className="field__label">
              كلمة المرور
            </label>
            <div className="login-card__password-wrap">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                className="field__input ltr-field"
                autoComplete="current-password"
                {...register("password", { required: "كلمة المرور مطلوبة" })}
              />
              <button
                type="button"
                className="login-card__password-toggle"
                onClick={() => setShowPassword((v) => !v)}
                aria-label={showPassword ? "إخفاء كلمة المرور" : "إظهار كلمة المرور"}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            {errors.password && <p className="field__error">{errors.password.message}</p>}
          </div>

          <Button type="submit" loading={submitting} style={{ width: "100%", marginTop: "var(--space-2)" }}>
            دخول
          </Button>
        </form>

        <p className="login-card__footnote">
          لا تملك حسابًا؟ يجب على مدير النظام إنشاء حساب لك من لوحة المستخدمين.
        </p>
      </div>
    </div>
  );
}
