import { type SelectHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";
import "./FormField.css";

interface SelectFieldProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { value: string; label: string }[];
  placeholder?: string;
}

export const SelectField = forwardRef<HTMLSelectElement, SelectFieldProps>(
  ({ label, error, options, placeholder, className, id, ...rest }, ref) => {
    const selectId = id ?? rest.name;
    return (
      <div className="field">
        <label htmlFor={selectId} className="field__label">
          {label}
          {rest.required && <span className="field__required">*</span>}
        </label>
        <select
          ref={ref}
          id={selectId}
          className={clsx("field__select", error && "field__input--error", className)}
          {...rest}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="field__error">{error}</p>}
      </div>
    );
  },
);

SelectField.displayName = "SelectField";
