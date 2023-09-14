import { type NextPage } from "next";
import { getSession } from "next-auth/react";
import type {
  GetServerSidePropsContext,
  InferGetServerSidePropsType,
} from "next/types";
import { useState } from "react";
import Button from "~/components/Button";
import Link from "next/link";
import NewAnalysisSteps, {
  getCourtPhoto,
} from "~/components/navigation/NewAnalysisSteps";
import Loading from "~/components/new-analysis/Loading";
import Error from "~/components/new-analysis/Error";
import GoproWifi from "~/components/new-analysis/GoproWifi";
import { type TWificredentials } from "~/server/api/routers/videos";
import axios from "axios";
import { getBattery } from "~/components/new-analysis/Recording";

async function startRecording() {
  try {
    const record: TWificredentials = await axios.get(
      "http://127.0.0.1:8000/enable_Wifi",
      {
        responseType: "json",
      }
    );

    return record.data;
  } catch (err: unknown) {
    console.log(err);
  }
}

const NewAnalysis = (
  props: InferGetServerSidePropsType<typeof getServerSideProps>
) => {
  const [wifi, setWifi] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);

  return (
    <main className="min-h-screen bg-background">
      {wifi ? (
        <GoproWifi
          firstOnClick={() => {
            setWifi(false);
            setLoading(true);
          }}
          networkName={props.name}
          password={props.password}
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
        <NewAnalysisSteps
          image={props.image}
          initialBattery={props.initialBattery}
        />
      ) : (
        <Error
          firstOnClick={() => {
            setSuccess(true);
            setLoading(true);
          }}
        />
      )}
    </main>
  );
};

export default NewAnalysis;

export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
  const session = await getSession(ctx);
  const wifiCredentials = await startRecording();
  const courtPhoto = wifiCredentials && (await getCourtPhoto());
  const initialBattery = wifiCredentials && (await getBattery());

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
      name: wifiCredentials?.networkName,
      password: wifiCredentials?.password,
      image: courtPhoto?.file_url,
      initialBattery,
    },
  };
};

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
