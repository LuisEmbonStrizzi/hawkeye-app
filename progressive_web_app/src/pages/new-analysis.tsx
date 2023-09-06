import { type NextPage } from "next";
import {getSession } from "next-auth/react";
import type { GetServerSidePropsContext } from "next/types";
import { useState } from "react";
import Button from "~/components/Button";
import Link from "next/link";
import Topbar from "~/components/navigation/Topbar";
import AlignCorners from "~/components/AlignCorners";

const NewAnalysis: NextPage = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [success, setSuccess] = useState<boolean>(false);

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-6 p-6">
        {loading ? (
          <>
            {" "}
            <svg
              width="48"
              height="49"
              viewBox="0 0 48 49"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="animate-spin"
            >
              <path
                d="M24 44.5C21.2 44.5 18.5833 43.9833 16.15 42.95C13.7167 41.9167 11.6 40.5 9.8 38.7C8 36.9 6.58333 34.7833 5.55 32.35C4.51667 29.9167 4 27.3 4 24.5C4 21.7 4.51667 19.0833 5.55 16.65C6.58333 14.2167 8 12.1 9.8 10.3C11.6 8.5 13.7167 7.08333 16.15 6.05C18.5833 5.01667 21.2 4.5 24 4.5C24.4 4.5 24.75 4.65 25.05 4.95C25.35 5.25 25.5 5.6 25.5 6C25.5 6.4 25.35 6.75 25.05 7.05C24.75 7.35 24.4 7.5 24 7.5C19.3 7.5 15.2917 9.15833 11.975 12.475C8.65833 15.7917 7 19.8 7 24.5C7 29.2 8.65833 33.2083 11.975 36.525C15.2917 39.8417 19.3 41.5 24 41.5C28.7 41.5 32.7083 39.8417 36.025 36.525C39.3417 33.2083 41 29.2 41 24.5C41 24.1 41.15 23.75 41.45 23.45C41.75 23.15 42.1 23 42.5 23C42.9 23 43.25 23.15 43.55 23.45C43.85 23.75 44 24.1 44 24.5C44 27.3 43.4833 29.9167 42.45 32.35C41.4167 34.7833 40 36.9 38.2 38.7C36.4 40.5 34.2833 41.9167 31.85 42.95C29.4167 43.9833 26.8 44.5 24 44.5Z"
                className="fill-primary"
              />
            </svg>
            <p className="font-medium text-foreground-important">
              Loading cameras...
            </p>
            <div className="flex w-full flex-col items-center justify-center gap-4 sm:flex-row">
              <Button
                label="Success"
                style="primary"
                onClick={() => {
                  setLoading(false);
                  setSuccess(true);
                }}
              />
              <Button
                label="Failure"
                style="secondary"
                onClick={() => {
                  setLoading(false);
                  setSuccess(false);
                }}
              />
            </div>
          </>
        ) : success ? (<><Topbar step={1}/><AlignCorners image="/img/test.png"/></>) : (
          <>
            <svg
              width="128"
              height="128"
              viewBox="0 0 128 128"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M117.333 91.3333L95.9998 70V84.8L87.9998 76.8V29.3333H40.5332L32.5332 21.3333H87.9998C90.1332 21.3333 91.9998 22.1333 93.5998 23.7333C95.1998 25.3333 95.9998 27.2 95.9998 29.3333V58L117.333 36.6667V91.3333ZM113.066 124.4L5.19983 16.5333L10.7998 10.9333L118.666 118.8L113.066 124.4ZM21.1998 21.3333L29.1998 29.3333H18.6665V98.6667H87.9998V88.1333L95.9998 96.1333V98.6667C95.9998 100.8 95.1998 102.667 93.5998 104.267C91.9998 105.867 90.1332 106.667 87.9998 106.667H18.6665C16.5332 106.667 14.6665 105.867 13.0665 104.267C11.4665 102.667 10.6665 100.8 10.6665 98.6667V29.3333C10.6665 27.2 11.4665 25.3333 13.0665 23.7333C14.6665 22.1333 16.5332 21.3333 18.6665 21.3333H21.1998Z"
                fill="#1F2331"
              />
            </svg>
            <h2 className="text-3xl font-bold text-foreground-important">
              Whoops...
            </h2>
            <p className="text-center font-medium text-foreground">
              An error happened while trying to connect to the cameras.
            </p>
            <div className="mt-4 flex w-full max-w-sm flex-col gap-4">
              <Link href={"/home"} className="flex flex-col">
                <Button label="Go back" style="secondary" />
              </Link>
              <Button
                label="Try again"
                style="primary"
                onClick={() => {
                  setSuccess(true);
                  setLoading(true);
                }}
              />
            </div>
          </>
        )}
      </div>
    </main>
  );
};

export default NewAnalysis;

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

/* Esto es lo que había antes.

import { type NextPage } from "next";
import { api } from "~/utils/api";

const NewAnalysis: NextPage = () => {
  const uploadVideo = api.videos.uploadVideo.useMutation({
    onSuccess: () => {
      void refetchVideos();
    },
  });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmit = (e: any) => {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    e.preventDefault();
    uploadVideo.mutate();
  };

  const { data: videos, refetch: refetchVideos } =
    api.videos.getVideo.useQuery();

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
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        <div key={video.id}>
          <video
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            src={video.videoUrl!}
            height={800}
            width={800}
          ></video>

          <pre> {video.boundsArray} </pre>
        </div>
      ))}
    </>
  );
};

export default NewAnalysis;
*/
