import {clsx} from 'clsx'

type ButtonProps = {
  label: string;
  type?: 'submit' | 'reset' | 'button' | undefined;
  style: "primary" | "secondary" | "disabled";
  onClick?: () => void;
  //Icon related props
  icon?: boolean;
  iconBtn?: boolean;
  iconPosition?: "left" | "right";
};

const Button: React.FC<ButtonProps> = ({ label, style, icon, iconBtn, iconPosition, type }) => {
  return <button>Button</button>;
};
export default Button;
