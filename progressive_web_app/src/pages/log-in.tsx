import AuthForm from "~/components/AuthForm";
import Link from "next/link";
import { type NextPage } from "next";

const LogIn: NextPage = () => {
  return (
    <main className="flex flex-col min-h-screen items-center justify-center bg-[url('/img/bg-1920x1080.png')]">
      <h1 className="font-bold  text-h1 text-foreground-important">Log In</h1>
      <AuthForm mode="login" />
    </main>
  );
};

export default LogIn;
