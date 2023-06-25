import { type NextPage } from "next";
import { api } from "~/utils/api";
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server';
import type { AppRouter } from "~/server/api/root"; 
import { useState } from "react";

type RouterOutput = inferRouterOutputs<AppRouter>;
 
type Video = RouterOutput['videos']['uploadVideo'];

const [type, setType] = useState("")

const NewAnalysis: NextPage = () => {
  type blobVideo = {
    url: string;
  };

  
  const handleSubmit = ()=>{
    setType("luisPanza")
  }
  if (type == "luisPanza"){
    const uploadVideo = api.videos.uploadVideo.useQuery()
    const hola:Video = uploadVideo
  }
  return (
    <>
      <h1>NewAnalysis</h1>

      <form
        className="flex flex-col gap-[20px] "
        onSubmit={handleSubmit}
      >
        <button
          type="submit"
          className="rounded-md bg-blue-800 px-4 py-3 text-white"
        >
          Submit
        </button>
      </form>

      <br />

      <video src={`${uploadVideo}`} width={700} ></video>

    </>
  );
};

export default NewAnalysis;
