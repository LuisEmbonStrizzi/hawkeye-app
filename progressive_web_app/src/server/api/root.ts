import { exampleRouter } from "~/server/api/routers/example";
import { userRouter } from "./routers/user";
import { videoRouter } from "./routers/videos";
import { createTRPCRouter } from "~/server/api/trpc";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  example: exampleRouter,
  user: userRouter,
  videos: videoRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;