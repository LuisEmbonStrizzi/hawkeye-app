import { type NextPage } from "next";
import { api } from "~/utils/api";

const NewAnalysis: NextPage = () => {
  
  const blobVideo = api.videos.uploadVideo.useMutation()
  const handleSubmit = ()=>{
    blobVideo.mutate({video: "https://res.cloudinary.com/dfpitoil1/video/upload/eo_10,so_6.5/v1681685906/fargowg6dr7m8wj9njcg.mp4"})
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
