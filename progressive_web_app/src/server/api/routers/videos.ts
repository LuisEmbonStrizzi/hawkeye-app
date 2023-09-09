import { createTRPCRouter, protectedProcedure } from "~/server/api/trpc";

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
        "http://127.0.0.1:8080/stopRecording",
        { responseType: "json" }
      );

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

      //Prueba
      const response = await axios.get(cameraData.data.video, {
        responseType: "stream",
      });

      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      const uploadResponse = await blockBlobClient.uploadStream(response.data);
      console.log(
        // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
        `Blob was uploaded successfully. requestId: ${uploadResponse.requestId}`
      );

      const azureResponse = { videoUrl: blockBlobClient.url };

      const analysedVideo = await axios.post("http://20.226.51.27/predict", {
        url: azureResponse.videoUrl,
      });

      console.log(analysedVideo);

      const stringifyArray = JSON.stringify(analysedVideo.data);

      const result = await ctx.prisma.videos.create({
        data: {
          videoUrl: azureResponse.videoUrl,
          userId: ctx.session?.user.id,
          boundsArray: stringifyArray,
        },
      });

      console.log(result);
    } catch (err: unknown) {
      console.log(err);
    }
  }),

  getVideo: protectedProcedure.query(async ({ ctx }) => {
    const result = await ctx.prisma.videos.findFirst({
      where: {
        userId: ctx.session.user.id,
      },
    });
    console.log(result);
    return result;
  }),
  record: protectedProcedure.query(async ({}) => {
    try {
      const record = await axios.get("http://127.0.0.1:8080/record", {
        responseType: "json",
      });
      return record;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
  stopRecording: protectedProcedure.query(async ({}) => {
    try {
      const stopRecording = await axios.get(
        "http://127.0.0.1:8080/stopRecording",
        {
          responseType: "json",
        }
      );
      return stopRecording;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
  getBattery: protectedProcedure.query(async ({}) => {
    try {
      const battery = await axios.get("http://127.0.0.1:8080/getBattery", {
        responseType: "json",
      });
      return battery;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
});
