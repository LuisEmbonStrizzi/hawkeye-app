import { z } from "zod";
import {
  createTRPCRouter,
  publicProcedure,
  protectedProcedure,
} from "~/server/api/trpc";

import { v1 as uuidv1 } from "uuid";
import { BlobServiceClient } from "@azure/storage-blob";

// El Router recibe el video - Se sube al Blob Storage - Devuelve una URL - Se manda a analizar - Se muestra mientras tanto - Devuelve el resto de la data - Muestra el resto

export const videoRouter = createTRPCRouter({
    uploadVideo: protectedProcedure
      .input(z.object({ text: z.string() }))
      .query(({ input }) => {
        return {
          greeting: `Hello ${input.text}`,
        };
      }),
  
    getAll: publicProcedure.query(({ ctx }) => {
      return ctx.prisma.example.findMany();
    }),
  
    getSecretMessage: protectedProcedure.query(() => {
      return "you can now see this secret message!";
    }),
  });
  