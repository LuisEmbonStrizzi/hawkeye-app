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

const NewAnalysis: NextPage = () => {
  const [wifi, setWifi] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);
  const [alignedCorners, setAlignedCorners] = useState<boolean>(false);

  const password = "asn2djk12snd3sk";
  const name = "qZXA-321";

  return (
    <main className="min-h-screen bg-background">
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
