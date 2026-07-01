import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import { SelectField } from "@/components/ui/SelectField";
import type { Branch, BranchCreateInput } from "@/types/api";

interface BranchFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: BranchCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: Branch;
  companyOptions: { value: string; label: string }[];
}

export function BranchFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  companyOptions,
}: BranchFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<BranchCreateInput>({
    defaultValues: { is_active: true },
  });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              company_id: initialValues.company_id,
              name: initialValues.name,
              code: initialValues.code ?? "",
              address: initialValues.address ?? "",
              phone: initialValues.phone ?? "",
              email: initialValues.email ?? "",
              manager_name: initialValues.manager_name ?? "",
              tax_number: initialValues.tax_number ?? "",
              opening_time: initialValues.opening_time ?? "",
              closing_time: initialValues.closing_time ?? "",
              is_active: initialValues.is_active,
            }
          : { is_active: true, company_id: companyOptions[0]?.value ?? "" },
      );
    }
  }, [open, initialValues, reset, companyOptions]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={580}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <SelectField
          label="الشركة"
          required
          options={companyOptions}
          placeholder="اختر الشركة"
          disabled={Boolean(initialValues)}
          {...register("company_id", { required: "الشركة مطلوبة" })}
          error={errors.company_id?.message}
        />
        {initialValues && (
          <p style={{ marginTop: "calc(-1 * var(--space-3))", marginBottom: "var(--space-3)", fontSize: "var(--text-xs)", color: "var(--color-ink-faint)" }}>
            لا يمكن تغيير الشركة بعد إنشاء الفرع.
          </p>
        )}

        <FormField label="اسم الفرع" required {...register("name", { required: "اسم الفرع مطلوب" })} error={errors.name?.message} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="رمز الفرع" ltr {...register("code")} />
          <FormField label="اسم المدير" {...register("manager_name")} />
        </div>

        <FormField label="العنوان" {...register("address")} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="الهاتف" ltr {...register("phone")} />
          <FormField label="البريد الإلكتروني" type="email" ltr {...register("email")} />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="وقت الفتح" type="time" ltr {...register("opening_time")} />
          <FormField label="وقت الإغلاق" type="time" ltr {...register("closing_time")} />
        </div>

        <div className="field__checkbox-row">
          <input id="branch_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="branch_is_active">نشط</label>
        </div>

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
