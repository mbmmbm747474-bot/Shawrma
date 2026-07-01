import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import { SelectField } from "@/components/ui/SelectField";
import type { Warehouse, WarehouseCreateInput } from "@/types/api";

interface WarehouseFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: WarehouseCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: Warehouse;
  branchOptions: { value: string; label: string }[];
}

export function WarehouseFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  branchOptions,
}: WarehouseFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<WarehouseCreateInput>({ defaultValues: { is_active: true } });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? { branch_id: initialValues.branch_id, name: initialValues.name, is_active: initialValues.is_active }
          : { is_active: true, branch_id: branchOptions[0]?.value ?? "" },
      );
    }
  }, [open, initialValues, reset, branchOptions]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={480}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <SelectField
          label="الفرع"
          required
          options={branchOptions}
          placeholder="اختر الفرع"
          disabled={Boolean(initialValues)}
          {...register("branch_id", { required: "الفرع مطلوب" })}
          error={errors.branch_id?.message}
        />
        {initialValues && (
          <p
            style={{
              marginTop: "calc(-1 * var(--space-3))",
              marginBottom: "var(--space-3)",
              fontSize: "var(--text-xs)",
              color: "var(--color-ink-faint)",
            }}
          >
            لا يمكن تغيير الفرع بعد إنشاء المخزن.
          </p>
        )}

        <FormField
          label="اسم المخزن"
          required
          {...register("name", { required: "اسم المخزن مطلوب" })}
          error={errors.name?.message}
        />

        <div className="field__checkbox-row">
          <input id="warehouse_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="warehouse_is_active">نشط</label>
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
