import { InputHTMLAttributes, forwardRef } from "react";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, id, className = "", ...props }, ref) => {
    return (
      <div className="w-full">
        {label ? (
          <label
            htmlFor={id}
            className="block text-xs text-[#52524E] dark:text-[#9C9C98] mb-1.5"
          >
            {label}
          </label>
        ) : null}
        <input
          ref={ref}
          id={id}
          className={[
            "w-full h-9 px-3 text-sm",
            "bg-page-light dark:bg-page-dark",
            "text-[#111110] dark:text-[#F0F0EE]",
            "border-[0.5px] rounded-md",
            "border-[rgba(0,0,0,0.09)] dark:border-[rgba(255,255,255,0.08)]",
            "outline-none transition-colors",
            "focus:border-accent-light dark:focus:border-accent-dark",
            "focus:ring-2 focus:ring-accent-light/20 dark:focus:ring-accent-dark/20",
            "disabled:opacity-60",
            className,
          ].join(" ")}
          {...props}
        />
        {error ? (
          <p className="mt-1.5 text-xs text-[#B91C1C] dark:text-[#FCA5A5]">
            {error}
          </p>
        ) : null}
      </div>
    );
  }
);

Input.displayName = "Input";