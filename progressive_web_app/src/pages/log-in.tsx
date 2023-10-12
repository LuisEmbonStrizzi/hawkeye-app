import AuthForm from "~/components/AuthForm";
import { type NextPage } from "next";
import { getSession } from "next-auth/react";
import type { GetServerSidePropsContext } from "next/types";

const LogIn: NextPage = () => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-[24px] bg-[url('/img/bg-alt-1920x1080.png')] bg-top bg-no-repeat px-[32px] ">
      <AuthForm mode="login" />
    </main>
  );
};

export default LogIn;

export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  const session = await getSession(ctx);
  console.log(session);

  if (session) {
    return {
      redirect: {
        destination: "/new-analysis",
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
