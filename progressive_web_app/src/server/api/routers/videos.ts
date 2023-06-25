import {
  createTRPCRouter,
  protectedProcedure,
  publicProcedure,
} from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";
import { env } from "~/env.mjs";
import axios from "axios";

type cameraData = {
  data: {
    video: string;
  };
};

export const videoRouter = createTRPCRouter({
  uploadVideo: protectedProcedure.mutation(async ({ ctx }) => {
    try {
      const cameraData: cameraData = await axios.get(
        "http://127.0.0.1:8000/getVideo",
        { responseType: "json" }
      );
      console.log("holaholaholahola");
      console.log(cameraData.data.video);

      //Conectarse con el servicio

      if (!env.AZURE_STORAGE_CONNECTION_STRING) {
        throw Error("Azure Storage Connection string not found");
      }

      const blobServiceClient = BlobServiceClient.fromConnectionString(
        env.AZURE_STORAGE_CONNECTION_STRING
      );

      //Crear Container o elegir container preexistente
      const containerClient =
        blobServiceClient.getContainerClient("pruebavideos");

      //Crear Blob
      const blobName = "Video" + uuidv1() + ".mp4";
      const blockBlobClient = containerClient.getBlockBlobClient(blobName);
      console.log(
        `\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`
      );

      //Upload Data
      /*const response = await axios.get(input.video, { responseType: 'json' });
            const uploadBlobResponse = await blockBlobClient.upload(response.data, Buffer.byteLength(response.data));
            console.log(
              `Blob was uploaded successfully. requestId: ${uploadBlobResponse.requestId}`
            );*/

      //Prueba
      const response = await axios.get(cameraData.data.video, {
        responseType: "stream",
      });
      //console.log(response);
      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      const uploadResponse = await blockBlobClient.uploadStream(response.data);
      console.log(
        // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
        `Blob was uploaded successfully. requestId: ${uploadResponse.requestId}`
      );

      // const azureResponse = { videoUrl: blockBlobClient.url };
      const azureResponse = {
        videoUrl:
          "https://hawkeyevideos1.blob.core.windows.net/pruebavideos/Videoa4a641a0-1398-11ee-bff6-a515a2285270.mp4?sp=r&st=2023-06-25T20:44:36Z&se=2023-06-26T04:44:36Z&spr=https&sv=2022-11-02&sr=b&sig=7%2ByLuQyhdnt%2BQhpJcfcO5LlAXkVrZb2Vf0YIFGN4C3M%3D",
      };
      await ctx.prisma.videos.create({
        data: {
          videoUrl: azureResponse.videoUrl,
          userId: ctx.session?.user.id,
        },
      });
    } catch (err: any) {
      // eslint-disable-next-line @typescript-eslint/restrict-template-expressions, @typescript-eslint/no-unsafe-member-access
      console.log(`Error: ${err.message}`);
    }
  }),

  getVideo: protectedProcedure.query(async ({ ctx }) => {
    const result = await ctx.prisma.videos.findMany({
      where: {
        userId: ctx.session.user.id,
      },
    });
    console.log(result);
    return result;
  }),
});
