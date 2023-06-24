import { type NextPage } from "next";
import { api } from "~/utils/api";

const NewAnalysis: NextPage = () => {
  type blobVideo = {
    url: string;
  };

  let blobVideo = { url: ""}

  const handleSubmit = ()=>{
    blobVideo = api.videos.uploadVideo.useQuery()
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

      <video src={`${blobVideo.url}`} width={700} ></video>

    </>
  );
};

export default NewAnalysis;
