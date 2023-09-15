import { type NextPage } from "next";
import { getSession } from "next-auth/react";
import type {
  GetServerSidePropsContext,
  InferGetServerSidePropsType,
} from "next/types";
import { useEffect, useState } from "react";
import Button from "~/components/Button";
import Link from "next/link";
import NewAnalysisSteps from "~/components/navigation/NewAnalysisSteps";
import Loading from "~/components/new-analysis/Loading";
import Error from "~/components/new-analysis/Error";
import GoproWifi from "~/components/new-analysis/GoproWifi";
import AlignCorners from "~/components/new-analysis/AlignCorners";
import Recording from "~/components/new-analysis/Recording";

type APcredentials = {
  networkName: string;
  password: string;
};

const NewAnalysis: NextPage = () => {
  const [alignedCorners, setAlignedCorners] = useState<boolean>(false);
  const [wifi, setWifi] = useState<boolean>(true);
  const [hasFetchedData, setHasFetchedData] = useState<boolean>(false);

  const [wifiCredentials, setWifiCredentials] = useState<APcredentials | null>(
    null
  );

  async function getWifiCredentials() {
    try {
      if (!hasFetchedData) {
        const record: TWificredentials = await axios.get(
          "http://127.0.0.1:8000/enable_Wifi",
          {
            responseType: "json",
          }
        );

        console.log("holaaaaaaaaaaa");
        console.log(record);
        setWifiCredentials(record.data);
        setHasFetchedData(true);
      }
    } catch (err: unknown) {
      console.log(err);
    }
  }

  getWifiCredentials();

  return (
    <main className="min-h-screen bg-background">
      {alignedCorners ? (
        <Recording />
      ) : wifi ? (
        <AlignCorners firstOnClick={()=>{
          setWifi(false);
          setAlignedCorners(true);
        }}/>
      ) : hasFetchedData ? (
        <GoproWifi
          firstOnClick={() => {
            setWifi(true);
          }}
          networkName={wifiCredentials?.networkName}
          password={wifiCredentials?.password}
        />
      ) : (
        <Loading loadingText="Fetching GoPro data..." />
      )}
    </main>
  );
};

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

/*

      {wifi ? (
        <GoproWifi
          firstOnClick={() => {
            setWifi(false);
            setLoading(true);
          }}
          name={name}
          password={password}
        />
      ) : loading ? (
        <Loading
          firstOnClick={() => {
            setLoading(false);
            setSuccess(true);
          }}
          secondOnClick={() => {
            setLoading(false);
            setSuccess(false);
          }}
        />
      ) : success ? (
        alignedCorners ? (
          <Recording />
        ) : (
          <AlignCorners
            image="/img/test.png"
            firstOnClick={() => setAlignedCorners(true)}
          />
        )
      ) : (
        <Error
          firstOnClick={() => {
            setSuccess(true);
            setLoading(true);
          }}
        />
      )}

*/

/*

import { type NextPage } from "next";
import { getSession } from "next-auth/react";
import type {
  GetServerSidePropsContext,
  InferGetServerSidePropsType,
} from "next/types";
import { useEffect, useState } from "react";
import Button from "~/components/Button";
import Link from "next/link";
import NewAnalysisSteps from "~/components/navigation/NewAnalysisSteps";
import Loading from "~/components/new-analysis/Loading";
import Error from "~/components/new-analysis/Error";
import GoproWifi from "~/components/new-analysis/GoproWifi";
import {
  type TWificredentials,
  TgetBattery,
} from "~/server/api/routers/videos";
import axios from "axios";
import { getBattery } from "~/components/new-analysis/Recording";

type APcredentials = {
  networkName: string;
  password: string;
};

const NewAnalysis = () => {
  const [wifi, setWifi] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);
  const [initialBattery, setInitialBattery] = useState<number | undefined>(
    undefined
  );
  const [wifiCredentials, setWifiCredentials] = useState<APcredentials | null>(
    null
  );
  const [hasFetchedData, setHasFetchedData] = useState(false);

  async function getWifiCredentials() {
    try {
      if (!hasFetchedData) {
        const record: TWificredentials = await axios.get(
          "http://127.0.0.1:8000/enable_Wifi",
          {
            responseType: "json",
          }
        );

        console.log("holaaaaaaaaaaa");
        console.log(record);
        setWifiCredentials(record.data);
        setHasFetchedData(true);
      }
    } catch (err: unknown) {
      console.log(err);
    }
  }

  getWifiCredentials();

  return (
    <main className="min-h-screen bg-background">
      {hasFetchedData ? (
        <GoproWifi
          firstOnClick={() => {
            setWifi(false);
            setLoading(true);
          }}
          networkName={wifiCredentials?.networkName}
          password={wifiCredentials?.password}
        />
      ) : (
        <Loading loadingText="Fetching GoPro data..."/>
      )}
    </main>
  );
};

export default NewAnalysis;

/*

      {wifi ? (
        <GoproWifi
          firstOnClick={() => {
            setWifi(false);
            setLoading(true);
          }}
          networkName={wifiCredentials?.networkName}
          password={wifiCredentials?.password}
        />
      ) : loading ? (
        <Loading
          firstOnClick={() => {
            setLoading(false);
            setSuccess(true);
          }}
          secondOnClick={() => {
            setLoading(false);
            setSuccess(false);
          }}
        />
      ) : success ? (
        <NewAnalysisSteps />
      ) : (
        <Error
          firstOnClick={() => {
            setSuccess(true);
            setLoading(true);
          }}
        />
      )}

*/
