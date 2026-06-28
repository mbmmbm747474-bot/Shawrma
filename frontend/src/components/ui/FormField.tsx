import { type InputHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";
import "./FormField.css";

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
  ltr?: boolean;
}

export const FormField = forwardRef<HTMLInputElement, FormFieldProps>(
  ({ label, error, hint, ltr, className, id, ...rest }, ref) => {
    const inputId = id ?? rest.name;
    return (
      <div className="field">
        <label htmlFor={inputId} className="field__label">
          {label}
          {rest.required && <span className="field__required">*</span>}
        </label>
        <input
          ref={ref}
          id={inputId}
          className={clsx("field__input", ltr && "ltr-field", error && "field__input--error", className)}
          {...rest}
        />
        {hint && !error && <p className="field__hint">{hint}</p>}
        {error && <p className="field__error">{error}</p>}
      </div>
    );
  },
);

FormField.displayName = "FormField";
