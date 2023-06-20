import AuthForm from "~/components/AuthForm";
import { type NextPage } from "next";

const LogIn: NextPage = () => {
  return (
    <main className="flex flex-col gap-[24px] px-[16px] min-h-screen items-center justify-center bg-[url('/img/bg-1920x1080.png')]">
      <AuthForm mode="login" />
    </main>
  );
};

export default LogIn;
