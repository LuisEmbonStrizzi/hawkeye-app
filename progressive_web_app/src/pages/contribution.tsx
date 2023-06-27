import { type NextPage } from "next";
import {getSession } from "next-auth/react";
import type { GetServerSidePropsContext } from "next/types";

const Contribution: NextPage = () => {
  return (
    <>
      <h1>Contribution</h1>
    </>
  );
};

export default Contribution;

export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  const session = await getSession(ctx);
  console.log(session);

  if (!session) {
    return {
      redirect: {
        destination: "/log-in",
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