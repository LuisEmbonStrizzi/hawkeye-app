import { type NextPage } from "next";
import type { GetServerSidePropsContext } from "next/types";
import { getSession } from "next-auth/react";
import React from "react";
import AuthForm from "~/components/AuthForm";

const SignUp: NextPage = () => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-[24px] bg-[url('/img/bg-alt-1920x1080.png')] bg-top bg-no-repeat px-[32px]">
      <AuthForm mode="register" />
    </main>
  );
};

export default SignUp;

export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  const session = await getSession(ctx);
  console.log(session);

  if (session) {
    return {
      redirect: {
        destination: "/home",
        permanent: false,
      },
    };
  }
  return {
    props: {
      session,
    },
  };
};
