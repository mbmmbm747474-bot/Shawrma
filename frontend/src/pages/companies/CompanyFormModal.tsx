import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import type { Company, CompanyCreateInput } from "@/types/api";

interface CompanyFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: CompanyCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: Company;
}

export function CompanyFormModal({ open, onClose, onSubmit, submitting, title, initialValues }: CompanyFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CompanyCreateInput>({
    defaultValues: { currency: "EGP", is_active: true },
  });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              name: initialValues.name,
              legal_name: initialValues.legal_name ?? "",
              tax_number: initialValues.tax_number ?? "",
              commercial_register: initialValues.commercial_register ?? "",
              address: initialValues.address ?? "",
              phone: initialValues.phone ?? "",
              email: initialValues.email ?? "",
              currency: initialValues.currency,
              is_active: initialValues.is_active,
            }
          : { currency: "EGP", is_active: true },
      );
    }
  }, [open, initialValues, reset]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={560}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <FormField label="اسم الشركة" required {...register("name", { required: "اسم الشركة مطلوب" })} error={errors.name?.message} />
        <FormField label="الاسم القانوني" {...register("legal_name")} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="الرقم الضريبي" ltr {...register("tax_number")} />
          <FormField label="السجل التجاري" ltr {...register("commercial_register")} />
        </div>

        <FormField label="العنوان" {...register("address")} />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="الهاتف" ltr {...register("phone")} />
          <FormField label="البريد الإلكتروني" type="email" ltr {...register("email")} />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="العملة" ltr {...register("currency")} />
          <div className="field__checkbox-row" style={{ marginTop: "26px" }}>
            <input id="is_active" type="checkbox" {...register("is_active")} />
            <label htmlFor="is_active">نشطة</label>
          </div>
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
