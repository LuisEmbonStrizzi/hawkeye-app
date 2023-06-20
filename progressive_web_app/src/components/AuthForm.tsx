/* eslint-disable @typescript-eslint/no-misused-promises */
import Button from "~/components/Button";
import Separator from "~/components/Separator";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { signIn } from "next-auth/react";
import { useState } from "react";
import clsx from "clsx";
import Progress from "./Progress";

type AuthFormProps = {
  mode: "login" | "register";
};
type Data = {
  Email: string;
  Password: string;
};
type Type = "password" | "text";

const AuthForm: React.FC<AuthFormProps> = ({ mode }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Data>();

  const [type, setType] = useState<Type>("password");
  const [loading, setLoading] = useState<boolean>(false);

  const onSubmit = async (data: Data) => {
    setLoading(true);
    const status = await signIn("Login", {
      redirect: false,
      email: data.Email,
      password: data.Password,
      callbackUrl: "http://localhost:3000/",
    });
    console.log(status);
    setLoading(false);
  };
  console.log(errors);

  return (
    <div className="mx-auto flex w-full  max-w-[450px] flex-col items-center gap-[24px]">
      <h1 className="mb-[24px] text-[24px] font-bold text-foreground-important">
        {mode === "login" ? "Login to Hawkeye" : "Sign Up to Hawkeye"}
      </h1>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex w-full flex-col gap-[24px]"
      >
        <div className="flex flex-col gap-[5px]">
          <label htmlFor="email" className="text-sm text-secondary-foreground">
            Email
          </label>
          <input
            className={clsx(
              "rounded-lg border border-secondary-border bg-secondary-background p-[10px] text-sm text-foreground-important outline-none transition-all duration-300 ease-out focus:border-primary focus:ring-2 focus:ring-primary/30",
              errors.Email && "border-[#FF034F]"
            )}
            type="text"
            {...register("Email", { required: true, pattern: /^\S+@\S+$/i })}
          />
        </div>
        <div className="flex flex-col gap-[5px]">
          <label
            htmlFor="password"
            className="text-sm text-secondary-foreground"
          >
            Password
          </label>
          <input
            className="relative rounded-lg border border-secondary-border bg-secondary-background p-[10px] text-sm text-foreground-important outline-none transition-all duration-300 ease-out focus:border-primary focus:ring-2 focus:ring-primary/30"
            type="password"
            {...register("Password", { required: true, min: 8 })}
          />
        </div>
        <Button
          style="primary"
          label={loading ? "" : "Log in"}
          icon={loading ? <Progress color="#181B27" /> : null}
          type="submit"
        />
      </form>
      <Separator label="OR" />
      <div className="flex w-full flex-col gap-[24px]">
        <Button
          style="secondary"
          label="Continue with Google"
          icon={
            <svg
              width="20"
              height="21"
              viewBox="0 0 20 21"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16.4666 9.47498L16.3916 9.18331H10.1916V11.8166H13.9C13.693 12.6202 13.2226 13.3311 12.5639 13.8357C11.9052 14.3403 11.0963 14.6094 10.2666 14.6C9.18399 14.591 8.14375 14.1779 7.34996 13.4416C6.95975 13.057 6.64923 12.5992 6.43617 12.0945C6.22311 11.5897 6.11169 11.0479 6.1083 10.5C6.12089 9.39953 6.55657 8.34616 7.32496 7.55831C8.10755 6.81694 9.14701 6.40773 10.225 6.41664C11.1482 6.42375 12.0371 6.76746 12.725 7.38331L14.5583 5.49998C13.35 4.42194 11.7859 3.82838 10.1666 3.83331C9.27583 3.82802 8.39271 3.99824 7.56769 4.33425C6.74267 4.67026 5.99192 5.16548 5.3583 5.79164C4.15305 7.04354 3.47352 8.70981 3.45957 10.4475C3.44562 12.1853 4.0983 13.8622 5.2833 15.1333C5.93984 15.7874 6.72015 16.3041 7.57864 16.6532C8.43713 17.0024 9.35659 17.1769 10.2833 17.1666C11.1237 17.1729 11.9566 17.0084 12.7315 16.6833C13.5065 16.3581 14.2073 15.879 14.7916 15.275C15.9382 14.0142 16.5585 12.3622 16.525 10.6583C16.534 10.263 16.5145 9.86751 16.4666 9.47498Z"
                className="fill-secondary-foreground group-hover:fill-foreground"
              />
            </svg>
          }
        />
        <Button
          style="secondary"
          label="Continue with Apple"
          icon={
            <svg
              width="20"
              height="21"
              viewBox="0 0 20 21"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M14.2084 17.4C13.3917 18.1917 12.5001 18.0667 11.6417 17.6917C10.7334 17.3083 9.90005 17.2917 8.94172 17.6917C7.74172 18.2083 7.10839 18.0583 6.39172 17.4C2.32506 13.2083 2.92506 6.825 7.54172 6.59167C8.66672 6.65 9.45006 7.20833 10.1084 7.25833C11.0917 7.05833 12.0334 6.48333 13.0834 6.55833C14.3417 6.65833 15.2917 7.15833 15.9167 8.05833C13.3167 9.61667 13.9334 13.0417 16.3167 14C15.8417 15.25 15.2251 16.4917 14.2001 17.4083L14.2084 17.4ZM10.0251 6.54167C9.90005 4.68333 11.4084 3.15 13.1417 3C13.3834 5.15 11.1917 6.75 10.0251 6.54167Z"
                className="fill-secondary-foreground group-hover:fill-foreground"
              />
            </svg>
          }
        />
      </div>
      {mode === "login" ? (
        <p className="text-sm text-foreground">
          Do not have an account?{" "}
          <Link className="text-primary underline" href="/sign-up">
            Sign Up
          </Link>
        </p>
      ) : (
        <p className="text-sm text-foreground">
          Have an account?{" "}
          <Link className="text-primary underline" href="/log-in">
            Log In
          </Link>
        </p>
      )}
    </div>
  );
};
export default AuthForm;
