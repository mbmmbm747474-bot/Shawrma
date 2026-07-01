import { type ButtonHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";
import "./IconButton.css";

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "danger";
}

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ variant = "default", className, ...rest }, ref) => {
    return <button ref={ref} type="button" className={clsx("icon-btn", `icon-btn--${variant}`, className)} {...rest} />;
  },
);

IconButton.displayName = "IconButton";
