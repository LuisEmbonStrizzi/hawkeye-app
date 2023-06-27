import { type NextPage } from "next";
import {getSession } from "next-auth/react";
import type { GetServerSidePropsContext } from "next/types";
import Profile from "~/components/Profile";

const Home: NextPage = () => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-[24px] bg-background bg-no-repeat px-[32px] ">
      <Profile />
    </main>
  );
};

/*

            {sessionData && (
              <Button
                style="primary"
                label="Sign out"
                onClick={() => void signOut({ callbackUrl: "/log-in" })}
              />
            )}

*/


export default Home;


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