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
import Recording, { getBattery } from "~/components/new-analysis/Recording";
import AlignCorners from "~/components/new-analysis/AlignCorners";
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
          "http://127.0.0.1:8000/api-gopro/enable_Wifi",
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

  void getWifiCredentials();

  return (
    <main className="min-h-screen bg-background">
      {hasFetchedData ? (
        wifi ? (
          <GoproWifi
            firstOnClick={() => {
              setWifi(false);
              setLoading(true);
            }}
            networkName={wifiCredentials?.networkName}
            password={wifiCredentials?.password}
          />
        ) : (
          <NewAnalysisSteps />
        )
      ) : (
        <Loading loadingText="Fetching GoPro network..." />
      )}
    </main>
  );
};

//Loading de GoProWifi: Correcto
//GoProWifi: Correcto
//Loading de AlignCorners: Correcto
//AlignCorners: Correcto
//Recording: Correcto
//Toast de finish recording: No aun
//Loading de call hawkeye: No aun

export default NewAnalysis;

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

/* Esto es lo que había antes.

import { type NextPage } from "next";
import { api } from "~/utils/api";
const NewAnalysis: NextPage = () => {
  const uploadVideo = api.videos.uploadVideo.useMutation();
  const { data: videos } = api.videos.getVideo.useQuery(undefined, {
    refetchInterval: 3000,
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    uploadVideo.mutate();
  };

  return (
    <>
      <h1>NewAnalysis</h1>
      <form className="flex flex-col gap-[20px] " onSubmit={handleSubmit}>
        <button
          type="submit"
          className="rounded-md bg-blue-800 px-4 py-3 text-white"
        >
          Llamar al ojo de halcón
        </button>
      </form>
      <br />

      {videos?.map((video) => (
        <div key={video.id}>
          <video src={video.videoUrl!} height={800} width={800}></video>
          <pre> {video.boundsArray} </pre>
        </div>
      ))}
    </>
  );
};

export default NewAnalysis;
*/
