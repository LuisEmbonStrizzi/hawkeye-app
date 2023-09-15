import { createTRPCRouter, protectedProcedure } from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";
import { env } from "~/env.mjs";
import axios from "axios";
import { z } from "zod";
export type cameraData = {
  data: {
    message: string;
    url: string;
  };
};
export type cameraData2 = {
  data: {
    url: string;
  };
};
export type TgetBattery = {
  data: {
    message: string;
    battery: number;
  };
};
export type TrecordResponse = {
  data: {
    message: string;
  };
};
export type TWificredentials = {
  data: {
    networkName: string;
    password: string;
  };
};


const RecordResponse = z.object({
  message: z.string(),
  url: z.string(),
});

export type TRecordResponse = Omit<z.infer<typeof RecordResponse>, "file_url">;
export type TStopRecording = z.infer<typeof RecordResponse>;

export const videoRouter = createTRPCRouter({
  stopRecording: protectedProcedure.mutation(async ({ ctx }) => {
    try {
      const cameraData: cameraData = await axios.get(
        "http://127.0.0.1:8000/stopRecording",
        { responseType: "json" }
      );


      // //Conectarse con el servicio
      // if (!env.AZURE_STORAGE_CONNECTION_STRING) {
      //   throw Error("Azure Storage Connection string not found");
      // }

      // const blobServiceClient = BlobServiceClient.fromConnectionString(
      //   env.AZURE_STORAGE_CONNECTION_STRING
      // );

      // //Crear Container o elegir container preexistente
      // const containerClient =
      //   blobServiceClient.getContainerClient("pruebavideos");

      // //Crear Blob
      // const blobName = "Video" + uuidv1() + ".mp4";
      // const blockBlobClient = containerClient.getBlockBlobClient(blobName);
      // console.log(
      //   `\nUploading to Azure storage as blob\n\tname: ${blobName}:\n\tURL: ${blockBlobClient.url}`
      // );

      // //Prueba
      // const response = await axios.get(cameraData.data.file_url, {
      //   responseType: "stream",
      // });

      // // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      // const uploadResponse = await blockBlobClient.uploadStream(response.data);
      // console.log(
      //   // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
      //   `Blob was uploaded successfully. requestId: ${uploadResponse.requestId}`
      // );

      // const azureResponse = { videoUrl: blockBlobClient.url };

      const analysedVideo: cameraData2 = await axios.post("http://127.0.0.1:8080/predict", {
        url: cameraData.data.url,
      });

      console.log(analysedVideo.data.url);

      // const stringifyArray = JSON.stringify(analysedVideo.data.url);

      const result = await ctx.prisma.videos.create({
        data: {
          videoUrl: analysedVideo.data.url,
          userId: ctx.session?.user.id,
        },
      });

      console.log(result);
    } catch (err: unknown) {
      console.log(err);
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
