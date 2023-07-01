import { type NextPage } from "next";
import React from "react";
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
