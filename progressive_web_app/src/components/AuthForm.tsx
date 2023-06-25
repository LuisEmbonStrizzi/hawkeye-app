/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-misused-promises */
import Button from "~/components/Button";
import Separator from "~/components/Separator";
import Link from "next/link";
import type { SubmitHandler, FieldValues } from "react-hook-form";
import { useForm } from "react-hook-form";
import { signIn } from "next-auth/react";
import { useState } from "react";
import { useRouter } from "next/router";
import { toast } from "react-hot-toast";
import clsx from "clsx";
import Progress from "./Progress";

type AuthFormProps = {
  mode: "login" | "register";
};

const AuthForm: React.FC<AuthFormProps> = ({ mode }) => {
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors, isDirty, isValid, isSubmitting },
    watch,
  } = useForm<FieldValues>({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  const passwordLength: number = watch("Password")
    ? watch("Password").length
    : 0;
  const emailLength: number = watch("Email") ? watch("Email").length : 0;
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const onSubmit: SubmitHandler<FieldValues> = (data) => {
    setLoading(true);
    if (mode === "login") {
      signIn("Login", {
        redirect: false, //CAMBIAR DESPUÉS
        email: data.Email,
        password: data.Password,
        callbackUrl: "http://localhost:3000/home",
      })
        .then((callback) => {
          if (callback?.error) {
            toast.error("Error, verify your email and password");
          } else {
            void router.push("/home");
          }
        })
        .finally(() => {
          setLoading(false);
        });
    }
    if (mode === "register") {
      signIn("SignUp", {
        redirect: false, //CAMBIAR DESPUÉS
        email: data.Email,
        password: data.Password,
        callbackUrl: "http://localhost:3000/home",
      })
        .then((callback) => {
          if (callback?.error) {
            toast.error("User already exists or email is not right");
          } else {
            void router.push("/home");
          }
        })
        .finally(() => {
          setLoading(false);
        });
    }
  };

  return (
    <div className="mx-auto flex w-full  max-w-[450px] flex-col items-center gap-[24px]">
      <h1 className="mb-[24px] text-h2 font-bold text-foreground-important">
        {mode === "login" ? "Log In" : "Sign Up"}
      </h1>
      <form
        className="flex w-full flex-col gap-[24px]"
        onSubmit={handleSubmit(onSubmit)}
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
          <div className="relative">
            <input
              className="relative w-full rounded-lg border border-secondary-border bg-secondary-background p-[10px] pr-[40px] text-sm text-foreground-important outline-none transition-all duration-300 ease-out focus:border-primary focus:ring-2 focus:ring-primary/30"
              type={showPassword ? "text" : "password"}
              {...register("Password", { required: true, minLength: 8 })}
            />
            <button onClick={() => setShowPassword(!showPassword)} className="absolute right-[10px] my-[11.5px] pl-[10px] border-l border-secondary-border">
              {showPassword === true ? (
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M13.2708 11.1458L11.9792 9.85417C12.0347 9.32639 11.875 8.87153 11.5 8.48959C11.125 8.10764 10.6736 7.94445 10.1458 8.00001L8.85417 6.70834C9.03472 6.63889 9.22222 6.58681 9.41667 6.55209C9.61111 6.51737 9.80556 6.50001 10 6.50001C10.9722 6.50001 11.7986 6.84028 12.4792 7.52084C13.1597 8.20139 13.5 9.02778 13.5 10C13.5 10.1944 13.4826 10.3889 13.4479 10.5833C13.4132 10.7778 13.3542 10.9653 13.2708 11.1458ZM16.0417 13.9167L14.9583 12.8333C15.4583 12.4444 15.9132 12.0174 16.3229 11.5521C16.7326 11.0868 17.0764 10.5694 17.3542 10C16.6736 8.59723 15.6701 7.49653 14.3438 6.69792C13.0174 5.89931 11.5694 5.50001 10 5.50001C9.63889 5.50001 9.28472 5.52084 8.9375 5.56251C8.59028 5.60417 8.25 5.67362 7.91667 5.77084L6.70833 4.56251C7.23611 4.35417 7.77431 4.20834 8.32292 4.12501C8.87153 4.04167 9.43056 4.00001 10 4.00001C11.9861 4.00001 13.8021 4.5382 15.4479 5.61459C17.0938 6.69098 18.2778 8.15278 19 10C18.6944 10.7917 18.2882 11.5104 17.7812 12.1563C17.2743 12.8021 16.6944 13.3889 16.0417 13.9167ZM16 18.125L13.2917 15.4167C12.7639 15.6111 12.2257 15.7569 11.6771 15.8542C11.1285 15.9514 10.5694 16 10 16C8.01389 16 6.19792 15.4618 4.55208 14.3854C2.90625 13.309 1.72222 11.8472 1 10C1.30556 9.20834 1.70833 8.48612 2.20833 7.83334C2.70833 7.18056 3.29167 6.59028 3.95833 6.06251L1.875 3.97917L2.9375 2.91667L17.0625 17.0625L16 18.125ZM5.02083 7.14584C4.53472 7.53473 4.08333 7.96181 3.66667 8.42709C3.25 8.89237 2.90972 9.41667 2.64583 10C3.32639 11.4028 4.32986 12.5035 5.65625 13.3021C6.98264 14.1007 8.43056 14.5 10 14.5C10.3611 14.5 10.7153 14.4757 11.0625 14.4271C11.4097 14.3785 11.7569 14.3125 12.1042 14.2292L11.1667 13.2917C10.9722 13.3611 10.7778 13.4132 10.5833 13.4479C10.3889 13.4826 10.1944 13.5 10 13.5C9.02778 13.5 8.20139 13.1597 7.52083 12.4792C6.84028 11.7986 6.5 10.9722 6.5 10C6.5 9.80556 6.52431 9.61112 6.57292 9.41667C6.62153 9.22223 6.66667 9.02778 6.70833 8.83334L5.02083 7.14584Z"
                    className="fill-secondary-foreground"
                  />
                </svg>
              ) : (
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 13.5C10.9722 13.5 11.7986 13.1597 12.4792 12.4792C13.1597 11.7986 13.5 10.9722 13.5 10C13.5 9.02778 13.1597 8.20139 12.4792 7.52083C11.7986 6.84028 10.9722 6.5 10 6.5C9.02778 6.5 8.20139 6.84028 7.52083 7.52083C6.84028 8.20139 6.5 9.02778 6.5 10C6.5 10.9722 6.84028 11.7986 7.52083 12.4792C8.20139 13.1597 9.02778 13.5 10 13.5ZM10 12C9.44444 12 8.97222 11.8056 8.58333 11.4167C8.19444 11.0278 8 10.5556 8 10C8 9.44444 8.19444 8.97222 8.58333 8.58333C8.97222 8.19444 9.44444 8 10 8C10.5556 8 11.0278 8.19444 11.4167 8.58333C11.8056 8.97222 12 9.44444 12 10C12 10.5556 11.8056 11.0278 11.4167 11.4167C11.0278 11.8056 10.5556 12 10 12ZM10 16C8.0195 16 6.21535 15.4549 4.58754 14.3646C2.95974 13.2743 1.76389 11.8194 1 10C1.76389 8.18056 2.95974 6.72569 4.58754 5.63542C6.21535 4.54514 8.0195 4 10 4C11.9805 4 13.7847 4.54514 15.4125 5.63542C17.0403 6.72569 18.2361 8.18056 19 10C18.2361 11.8194 17.0403 13.2743 15.4125 14.3646C13.7847 15.4549 11.9805 16 10 16ZM10 14.5C11.5556 14.5 12.9931 14.0972 14.3125 13.2917C15.6319 12.4861 16.6458 11.3889 17.3542 10C16.6458 8.61111 15.6319 7.51389 14.3125 6.70833C12.9931 5.90278 11.5556 5.5 10 5.5C8.44444 5.5 7.00694 5.90278 5.6875 6.70833C4.36806 7.51389 3.35417 8.61111 2.64583 10C3.35417 11.3889 4.36806 12.4861 5.6875 13.2917C7.00694 14.0972 8.44444 14.5 10 14.5Z"
                    className="fill-secondary-foreground"
                  />
                </svg>
              )}
            </button>
          </div>
          {mode === "login" ? (
            <div className="my-[10px] flex gap-[5px]">
              <Link
                href={"/forgot-password"}
                className="text-sm text-primary underline"
              >
                Forgot password?
              </Link>
            </div>
          ) : (
            <div className="my-[10px] flex gap-[5px]">
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9.07337 14.1766H10.9267V9H9.07337V14.1766ZM9.99562 7.73552C10.2736 7.73552 10.5081 7.64149 10.6991 7.45344C10.89 7.2654 10.9855 7.03238 10.9855 6.7544C10.9855 6.4764 10.8915 6.24191 10.7035 6.05094C10.5154 5.85997 10.2824 5.76448 10.0044 5.76448C9.72641 5.76448 9.49193 5.85851 9.30095 6.04656C9.10998 6.2346 9.01449 6.46762 9.01449 6.7456C9.01449 7.0236 9.10852 7.25809 9.29658 7.44906C9.48462 7.64003 9.71763 7.73552 9.99562 7.73552ZM10.0058 18.4004C8.8419 18.4004 7.75036 18.1819 6.73114 17.745C5.7119 17.308 4.82032 16.7076 4.05639 15.9436C3.29245 15.1797 2.692 14.2884 2.25506 13.2698C1.81811 12.2511 1.59964 11.158 1.59964 9.99046C1.59964 8.8229 1.81811 7.73299 2.25506 6.72071C2.692 5.70842 3.29245 4.82031 4.05639 4.05638C4.82032 3.29243 5.71161 2.69199 6.73027 2.25504C7.74892 1.8181 8.84202 1.59962 10.0096 1.59962C11.1771 1.59962 12.267 1.8181 13.2793 2.25504C14.2916 2.69199 15.1797 3.29243 15.9436 4.05638C16.7076 4.82031 17.308 5.70997 17.745 6.72538C18.1819 7.74078 18.4004 8.8304 18.4004 9.99425C18.4004 11.1581 18.1819 12.2497 17.745 13.2689C17.308 14.2881 16.7076 15.1797 15.9436 15.9436C15.1797 16.7076 14.29 17.308 13.2746 17.745C12.2592 18.1819 11.1696 18.4004 10.0058 18.4004ZM10 16.3587C11.7742 16.3587 13.2775 15.7424 14.51 14.51C15.7425 13.2775 16.3587 11.7742 16.3587 10C16.3587 8.22585 15.7425 6.72253 14.51 5.49004C13.2775 4.25756 11.7742 3.64131 10 3.64131C8.22586 3.64131 6.72254 4.25756 5.49006 5.49004C4.25757 6.72253 3.64133 8.22585 3.64133 10C3.64133 11.7742 4.25757 13.2775 5.49006 14.51C6.72254 15.7424 8.22586 16.3587 10 16.3587Z"
                  className={clsx(
                    passwordLength >= 8
                      ? "fill-primary"
                      : "fill-secondary-foreground"
                  )}
                />
              </svg>

              <p
                className={clsx(
                  "text-sm font-semibold transition-all duration-300 ease-out",
                  passwordLength >= 8
                    ? "text-primary"
                    : "text-secondary-foreground"
                )}
              >
                At least eight characters
              </p>
            </div>
          )}
        </div>
        <Button
          style="primary"
          label={
            loading ? "" : mode === "register" ? "Create an account" : "Log in"
          }
          icon={loading ? <Progress color="#181B27" /> : null}
          type="submit"
          disabled={isSubmitting}
          onClick={() => {
            if (!isValid) {
              if (!isDirty || passwordLength === 0 || emailLength === 0) {
                if (passwordLength === 0 && emailLength === 0) {
                  toast.error("Please fill the form");
                } else if (passwordLength === 0) {
                  toast.error("Please provide your password");
                } else if (emailLength === 0) {
                  toast.error("Please provide your email");
                }
              } else {
                if (mode === "login") {
                  toast.error("Error, verify your email and password");
                } else if (mode === "register") {
                  if (errors.Email) {
                    toast.error("Invalid email, try again");
                  } else if (errors.Password) {
                    toast.error("Your password is too short");
                  }
                }
              }
            }
          }}
        />
      </form>
      <Separator label="OR" />
      <div className="flex w-full flex-col gap-[24px]">
        <Button
          style="secondary"
          label="Continue with Google"
          onClick={() => signIn("google", { callbackUrl: "/home" })}
          iconPosition="left"
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
      </div>
      {mode === "login" ? (
        <p className="mt-[24px] text-sm text-foreground">
          Do not have an account?{" "}
          <Link className="text-primary underline" href="/sign-up">
            Sign Up
          </Link>
        </p>
      ) : (
        <p className="mt-[24px] text-sm text-foreground">
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
