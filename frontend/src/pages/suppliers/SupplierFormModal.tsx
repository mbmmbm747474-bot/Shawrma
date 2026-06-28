import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import type { Supplier, SupplierCreateInput } from "@/types/api";

interface SupplierFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: SupplierCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: Supplier;
  companyId: string;
}

export function SupplierFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  companyId,
}: SupplierFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SupplierCreateInput>({ defaultValues: { is_active: true, company_id: companyId } });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              company_id: initialValues.company_id,
              name: initialValues.name,
              phone: initialValues.phone ?? "",
              email: initialValues.email ?? "",
              address: initialValues.address ?? "",
              is_active: initialValues.is_active,
            }
          : { is_active: true, company_id: companyId },
      );
    }
  }, [open, initialValues, reset, companyId]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={500}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <FormField
          label="اسم المورد"
          required
          {...register("name", { required: "اسم المورد مطلوب" })}
          error={errors.name?.message}
        />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="الهاتف" ltr {...register("phone")} />
          <FormField label="البريد الإلكتروني" type="email" ltr {...register("email")} />
        </div>

        <FormField label="العنوان" {...register("address")} />

        <div className="field__checkbox-row">
          <input id="supplier_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="supplier_is_active">نشط</label>
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
