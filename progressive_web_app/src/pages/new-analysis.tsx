import { type NextPage } from "next";
import { api } from "~/utils/api";

const NewAnalysis: NextPage = () => {
  
  const blobVideo = api.videos.uploadVideo.useMutation()
  const handleSubmit = ()=>{
    blobVideo.mutate({video: "https://res.cloudinary.com/dfpitoil1/video/upload/v1677799061/rudp2zur1irdqnvc4qho.mp4"})
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

    </>
  );
};

export default NewAnalysis;
