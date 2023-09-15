import { type NextPage } from "next";
import { useState } from "react";
import { api } from "~/utils/api";


const NewAnalysis: NextPage = () => {
  
  const useProcessInterval = ({ onSuccess, onError }) =>{
    const [processId, setProcessId] = useState(null);
    const [stop, setStop] = useState(false);
  }
  
  const uploadVideo = api.videos.uploadVideo.useMutation({
    onMutate: () => {
      void refetchVideos();
      
    },
    onError: () =>{

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
