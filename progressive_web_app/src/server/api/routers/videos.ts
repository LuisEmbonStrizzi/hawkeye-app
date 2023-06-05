import { z } from "zod";
import {
  createTRPCRouter,
  publicProcedure,
  protectedProcedure,
} from "~/server/api/trpc";

import { BlobServiceClient } from "@azure/storage-blob";
import { v1 as uuidv1 } from "uuid";

export const videoRouter = createTRPCRouter({
    hello: publicProcedure
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
  