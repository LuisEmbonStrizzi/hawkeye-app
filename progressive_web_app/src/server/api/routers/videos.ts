import { createTRPCRouter, protectedProcedure, publicProcedure } from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";
import { env } from "~/env.mjs";
import axios from "axios";

type cameraData = {
  video: string;
};

export const videoRouter = createTRPCRouter({
  uploadVideo: publicProcedure.mutation(async ({ ctx }) => {
    try {
      const cameraData: cameraData = await axios.get(
        "http://127.0.0.1:8000/getVideo",
        { responseType: "text" }
      );
      console.log("hola")
      console.log(cameraData.data);

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
      console.log(response);
      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      const uploadResponse = await blockBlobClient.uploadStream(response.data);
      console.log(
        // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
        `Blob was uploaded successfully. requestId: ${uploadResponse.requestId}`
      );

      const azureResponse = { videoUrl: uploadResponse.requestId };
      await ctx.prisma.videos.create({
        data: {
          videoUrl: azureResponse.videoUrl,
          userId: ctx.session.user.id,
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
    return result;
  }),
});
