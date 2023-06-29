import { type NextPage } from "next";
import { api } from "~/utils/api";
const NewAnalysis: NextPage = () => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars

  const uploadVideo = api.videos.uploadVideo.useMutation();
  const { data: videos } = api.videos.getVideo.useQuery(undefined, {
    refetchInterval: 3000,
  });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmit = (e: any) => {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
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
