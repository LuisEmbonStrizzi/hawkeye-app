import { createTRPCRouter, protectedProcedure } from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";
import { env } from "~/env.mjs";
import axios from "axios";
import { z } from "zod";
type cameraData = {
  data: {
    video: string;
  };
};

const Battery = z.object({
  message: z.string(),
  battery: z.number(),
});

type TBattery = z.infer<typeof Battery>;

const CourtPhotoResponse = z.object({
  message: z.string(),
  file_url: z.string(),
});

type TCourtPhotoResponse = z.infer<typeof CourtPhotoResponse>;

const Wificredentials = z.object({
  netname: z.string(),
  password: z.string(),
});

type TWificredentials = z.infer<typeof Wificredentials>;

const RecordResponse = z.object({
  message: z.string(),
  file_url: z.string(),
});

export type TRecordResponse = Omit<z.infer<typeof RecordResponse>, "file_url">;
export type TStopRecording = z.infer<typeof RecordResponse>;

export const videoRouter = createTRPCRouter({
  enableWifi: protectedProcedure.mutation(async ({ ctx }) => {
    const Wificredentials: TWificredentials = await axios.get(
      "http://127.0.0.1:8080/enable_Wifi",
      { responseType: "json" }
    );
    const result = await ctx.prisma.videos.create({
      data: {
        userId: ctx.session?.user.id,
        ssid: Wificredentials.netname,
        Wifipassword: Wificredentials.password,
      },
    });
    console.log(result);
    return result;
  }),
  getWifiCredentials: protectedProcedure.query(async ({ ctx }) => {
    try {
      const result = await ctx.prisma.videos.findFirst({
        where: {
          userId: ctx.session.user.id,
        },
      });
      console.log(result);
      return result;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
  CourtPhoto: protectedProcedure.mutation(async ({ ctx }) => {
    try {
      const courtPhoto: TCourtPhotoResponse = await axios.get(
        "http://127.0.0.1:8080/courtPhoto",
        {
          responseType: "json",
        }
      );

      const result = await ctx.prisma.videos.create({
        data: {
          thumbnailUrl: courtPhoto.file_url,
          userId: ctx.session.user.id,
        },
      });

      return result;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
  getCourtPhoto: protectedProcedure.query(async ({ ctx }) => {
    try {
      const result = await ctx.prisma.videos.findFirst({
        where: {
          userId: ctx.session.user.id,
        },
      });
      console.log(result);
      return result;
    } catch (err: unknown) {
      console.log(err);
    }
  }),

  record: protectedProcedure.mutation(async ({}) => {
    try {
      const record: TRecordResponse = await axios.get(
        "http://127.0.0.1:8000/record",
        {
          responseType: "json",
        }
      );
      return record;
    } catch (err: unknown) {
      console.log(err);
    }
  }),

  stopRecording: protectedProcedure.mutation(async ({ ctx }) => {
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

  getBattery: protectedProcedure.query(async ({}) => {
    try {
      const battery: TBattery = await axios.get(
        "http://127.0.0.1:8080/getBattery",
        {
          responseType: "json",
        }
      );
      return battery;
    } catch (err: unknown) {
      console.log(err);
    }
  }),
});
