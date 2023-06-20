import { clsx } from "clsx";

type SeparatorProps = {
  label?: string;
};

const Separator: React.FC<SeparatorProps> = ({ label }) => {
  return (
    <span className="flex w-full select-none items-center gap-[8px] text-sm font-bold text-tertiary-border before:flex-grow before:border-t before:border-background-border after:flex-grow after:border-t after:border-background-border">
      {label}
    </span>
  );
};
export default Separator;
