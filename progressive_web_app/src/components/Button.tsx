import clsx from "clsx";

type ButtonProps = {
  label?: string;
  type?: "submit" | "reset" | "button" | undefined;
  style: "primary" | "secondary";
  disabled?: boolean;
  onClick?: () => void;
  roundedFull?: boolean;
  //Icon related props
  icon?: React.ReactNode;
  padding?: "icon" | "label" | "both-right" | "both-left";
  iconPosition?: "left" | "right";
};

const Button: React.FC<ButtonProps> = ({
  label,
  style,
  roundedFull,
  icon,
  padding,
  iconPosition,
  type,
  disabled,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "group flex cursor-pointer select-none items-center justify-center gap-1 px-[16px] py-[10px] text-sm font-bold transition-all duration-150 ease-out",
        roundedFull ? "rounded-full" : "rounded-lg",
        style === "primary" &&
          "bg-primary text-background ring-offset-background hover:bg-primary/80 focus:ring-2 focus:ring-primary/30 focus:ring-offset-2",
        style === "secondary" &&
          "border border-secondary-border bg-secondary-background font-medium text-secondary-foreground ring-offset-background hover:border-tertiary-border hover:bg-tertiary-background hover:text-foreground focus:ring-2 focus:ring-secondary-foreground/30 focus:ring-offset-2",
        disabled && "pointer-events-none cursor-default select-none opacity-25",
        iconPosition === "left" ? "flex-row" : "flex-row-reverse",
        padding === "icon"
          ? "pl-[10px] pr-[10px]"
          : padding === "label"
          ? "px-4"
          : padding === "both-right"
          ? "pl-[10px pr-4"
          : padding === "both-left" && "pl-4 pr-[10px]"
      )}
      type={type}
    >
      {icon}
      {label}
    </button>
  );
};
export default Button;
