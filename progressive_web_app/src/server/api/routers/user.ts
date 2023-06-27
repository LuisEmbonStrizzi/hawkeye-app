/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-return */

import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";
import bcrypt from "bcrypt";
import { Resend } from "resend";
import { EmailTemplate } from "~/components/EmailTemplate";

const hash = async (password: string) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  const salt = await bcrypt.genSalt(10);
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  const hashedPassword = await bcrypt.hash(password, salt);
  return hashedPassword;
};

// eslint-disable-next-line @typescript-eslint/no-unsafe-call
const resend = new Resend(process.env.RESEND_API_KEY);

export const userRouter = createTRPCRouter({
  register: publicProcedure
    .input(z.object({ email: z.string().email(), password: z.string() }))
    .mutation(async ({ ctx, input }) => {
      const hashedPassword = await hash(input.password);
      const result = ctx.prisma.user.create({
        data: {
          email: input.email,
          password: hashedPassword,
        },
      });

      if (result !== null) {
        return { message: "User created", status: 201 };
      }

      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: "An unexpected error occurred, please try again later.",
      });
    }),
  sendEmail: publicProcedure
    .input(z.object({ email: z.string().email() }))
    .mutation(async ({ input }) => {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-call
      const response = await resend.emails.send({
        from: "onboarding@resend.dev",
        to: input.email,
        subject: "Hello World",
        html: "<p>Congrats on sending your <strong>first email</strong>!</p>",
        react: EmailTemplate({ firstName: "John" }),
      });
      console.log(response);
    }),
});
