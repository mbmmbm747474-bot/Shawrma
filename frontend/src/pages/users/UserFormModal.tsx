import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import { SelectField } from "@/components/ui/SelectField";
import type { Branch, Company, User, UserCreateInput, UserUpdateInput } from "@/types/api";

interface UserFormValues extends Omit<UserCreateInput, "password"> {
  password?: string;
}

interface UserFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: UserCreateInput | UserUpdateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: User;
  companies: Company[];
  branches: Branch[];
}

export function UserFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  companies,
  branches,
}: UserFormModalProps) {
  const isEdit = Boolean(initialValues);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string>("");

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors },
  } = useForm<UserFormValues>({
    defaultValues: { is_active: true, language: "ar", timezone: "Africa/Cairo" },
  });

  const watchedCompanyId = watch("company_id");

  useEffect(() => {
    if (open) {
      const initialCompanyId = initialValues?.company_id ?? companies[0]?.id ?? "";
      setSelectedCompanyId(initialCompanyId);
      reset(
        initialValues
          ? {
              username: initialValues.username,
              email: initialValues.email,
              full_name: initialValues.full_name,
              mobile: initialValues.mobile ?? "",
              company_id: initialValues.company_id,
              branch_id: initialValues.branch_id,
              is_active: initialValues.is_active,
              is_superuser: initialValues.is_superuser,
            }
          : {
              is_active: true,
              language: "ar",
              timezone: "Africa/Cairo",
              company_id: initialCompanyId,
            },
      );
    }
  }, [open, initialValues, reset, companies]);

  useEffect(() => {
    if (!watchedCompanyId) return;
    setSelectedCompanyId(watchedCompanyId);
    // Only clear branch_id if the user actively changed the company while
    // the form is open for creation — not on the initial reset for edit.
    if (!isEdit && open) {
      const stillValid = branches.some((b) => b.id === watch("branch_id") && b.company_id === watchedCompanyId);
      if (!stillValid) {
        setValue("branch_id", "");
      }
    }
  }, [watchedCompanyId]);

  const branchOptions = branches
    .filter((b) => b.company_id === selectedCompanyId)
    .map((b) => ({ value: b.id, label: b.name }));

  function handleFormSubmit(values: UserFormValues) {
    if (isEdit) {
      const { username, email, full_name, mobile, is_active, password } = values;
      const payload: UserUpdateInput = { username, email, full_name, mobile, is_active };
      if (password) payload.password = password;
      onSubmit(payload);
    } else {
      onSubmit(values as UserCreateInput);
    }
  }

  return (
    <Modal open={open} onClose={onClose} title={title} width={580}>
      <form onSubmit={handleSubmit(handleFormSubmit)} noValidate>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField
            label="الاسم الكامل"
            required
            {...register("full_name", { required: "الاسم الكامل مطلوب" })}
            error={errors.full_name?.message}
          />
          <FormField
            label="اسم المستخدم"
            required
            ltr
            {...register("username", { required: "اسم المستخدم مطلوب" })}
            error={errors.username?.message}
          />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField
            label="البريد الإلكتروني"
            type="email"
            required
            ltr
            {...register("email", { required: "البريد الإلكتروني مطلوب" })}
            error={errors.email?.message}
          />
          <FormField label="رقم الموبايل" ltr {...register("mobile")} />
        </div>

        <FormField
          label={isEdit ? "كلمة المرور الجديدة (اتركها فارغة للإبقاء على الحالية)" : "كلمة المرور"}
          type="password"
          required={!isEdit}
          ltr
          {...register("password", {
            required: isEdit ? false : "كلمة المرور مطلوبة",
            minLength: { value: 8, message: "٨ أحرف على الأقل" },
          })}
          error={errors.password?.message}
        />

        {!isEdit && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
            <SelectField
              label="الشركة"
              required
              options={companies.map((c) => ({ value: c.id, label: c.name }))}
              placeholder="اختر الشركة"
              {...register("company_id", { required: "الشركة مطلوبة" })}
              error={errors.company_id?.message}
            />
            <SelectField
              label="الفرع"
              required
              options={branchOptions}
              placeholder={branchOptions.length ? "اختر الفرع" : "اختر شركة أولًا"}
              disabled={branchOptions.length === 0}
              {...register("branch_id", { required: "الفرع مطلوب" })}
              error={errors.branch_id?.message}
            />
          </div>
        )}

        <div className="field__checkbox-row">
          <input id="user_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="user_is_active">نشط</label>
        </div>

        {!isEdit && (
          <div className="field__checkbox-row">
            <input id="user_is_superuser" type="checkbox" {...register("is_superuser")} />
            <label htmlFor="user_is_superuser">مدير عام (صلاحيات كاملة)</label>
          </div>
        )}

        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end", marginTop: "var(--space-5)" }}>
          <Button type="button" variant="ghost" onClick={onClose} disabled={submitting}>
            إلغاء
          </Button>
          <Button type="submit" loading={submitting}>
            حفظ
          </Button>
        </div>
      </form>
    </Modal>
  );
}
