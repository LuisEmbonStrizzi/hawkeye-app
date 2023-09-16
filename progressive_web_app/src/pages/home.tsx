import { type NextPage } from "next";
import {getSession } from "next-auth/react";
import type { GetServerSidePropsContext } from "next/types";
import Searchbar from "~/components/navigation/Searchbar";
import Sidebar from "~/components/navigation/Sidebar";

const Home: NextPage = () => {
  return (
    <main className="min-h-screen bg-background">
      <Sidebar activeItem="analysis"/>
      <Searchbar/>
      {/*Áca el mt del div del content debe tener la misma cantidad de pixeles como altura tenga el searchbar*/}
      <div className="ml-[280px] pt-[86px] pb-8">

      </div>
    </main>
  );
};

export default Home;


export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  const session = await getSession(ctx);

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