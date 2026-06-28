import { type ButtonHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";
import "./Button.css";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "sm" | "md";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", loading, className, children, disabled, ...rest }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx("btn", `btn--${variant}`, `btn--${size}`, loading && "btn--loading", className)}
        disabled={disabled || loading}
        {...rest}
      >
        {loading && <span className="btn__spinner" aria-hidden="true" />}
        <span className="btn__label">{children}</span>
      </button>
    );
  },
);

Button.displayName = "Button";
