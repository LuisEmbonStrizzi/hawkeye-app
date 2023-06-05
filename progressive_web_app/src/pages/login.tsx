import AuthForm from "~/components/AuthForm";
import Link from "next/link";
import { type NextPage } from "next";

const LogIn: NextPage = () => {
  return (
    <>
      <h1>LogIn</h1>
      <AuthForm mode="login"/>
      <p>
        Do not have an account?{" "}
        <Link href="/sign-up">Sign Up</Link>
      </p>

    </>
  );
};

export default LogIn;
