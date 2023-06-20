import { clsx } from "clsx";

type SeparatorProps = {
  label?: string;
};

const Separator: React.FC<SeparatorProps> = ({ label }) => {
  return (
    <div>
      <p>Separator</p>
    </div>
  );
};
export default Separator;
