import clsx from "clsx";
import Progress from "./Progress";

type ButtonProps = {
  label?: string;
  type?: "submit" | "reset" | "button" | undefined;
  style: "primary" | "secondary";
  disabled?: boolean;
  onClick?: () => void;
  roundedFull?: boolean;
  //Icon related props
  icon?: React.ReactNode;
  iconBtn?: boolean;
  iconPosition?: "left" | "right";
};

const Button: React.FC<ButtonProps> = ({
  label,
  style,
  roundedFull,
  icon,
  iconBtn,
  iconPosition,
  type,
  disabled,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "group flex cursor-pointer select-none items-center justify-center gap-[10px] px-[15px] py-[10px] text-sm font-bold transition-all duration-150 ease-out",
        roundedFull ? "rounded-full" : "rounded-lg",
        style === "primary" && "bg-primary text-background hover:bg-primary/80 focus:ring-2 focus:ring-primary/30 ring-offset-background focus:ring-offset-2",
        style === "secondary" &&
          "border border-secondary-border bg-secondary-background hover:bg-tertiary-background hover:border-tertiary-border hover:text-foreground font-medium text-secondary-foreground focus:ring-2 focus:ring-secondary-foreground/30 ring-offset-background focus:ring-offset-2",
        disabled && "pointer-events-none cursor-default select-none opacity-25",
        iconPosition === "left" ? "flex-row" : "flex-row-reverse",
        iconBtn && "p-[10px]"
      )}
      type={type}
    >
      {icon}
      {label}
    </button>
  );
};
export default Button;
