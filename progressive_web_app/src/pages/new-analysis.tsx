import { type NextPage } from "next";
import { api } from "~/utils/api";
import type { inferRouterInputs, inferRouterOutputs } from '@trpc/server';
import type { AppRouter } from "~/server/api/root"; 

type RouterOutput = inferRouterOutputs<AppRouter>;
 
type Video = RouterOutput['videos']['uploadVideo'];

const NewAnalysis: NextPage = () => {
  type blobVideo = {
    url: string;
  };

  
  const uploadVideo:Video = api.videos.uploadVideo.useMutation()
  const handleSubmit = ()=>{
    const Video = uploadVideo.mutate()
    console.log(Video)
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

      <video src={`${Video.url}`} width={700} ></video>

    </>
  );
};

export default NewAnalysis;
