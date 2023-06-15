import Button from "~/components/Button";
import Separator from "~/components/Separator";
import { useForm } from "react-hook-form";
import { signIn } from "next-auth/react";

type AuthFormProps = {
  mode: "login" | "register";
};
type Data = {
  Email: string;
  Password: string;
};

const AuthForm: React.FC<AuthFormProps> = ({ mode }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Data>();

  const onSubmit = async (data: Data) => {
    const status = await signIn("Login", {
      redirect: false,
      email: data.Email,
      password: data.Password,
      callbackUrl: "http://localhost:3000/",
    });
    console.log(status);
  };
  console.log(errors);

  return (
    // eslint-disable-next-line @typescript-eslint/no-misused-promises
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        type="text"
        placeholder="Email"
        {...register("Email", { required: true, pattern: /^\S+@\S+$/i })}
      />
      <input
        type="password"
        placeholder="Password"
        {...register("Password", { required: true, min: 8 })}
      />

      <input type="submit" />
    </form>
  );
};
export default AuthForm;

/* 

import React from 'react';
import { useForm } from 'react-hook-form';

export default function App() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => console.log(data);
  console.log(errors);
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="text" placeholder="Email" {...register("Email", {required: true, pattern: /^\S+@\S+$/i})} />
      <input type="password" placeholder="Password" {...register("Password", {required: true, min: 8})} />

      <input type="submit" />
    </form>
  );
}

*/
