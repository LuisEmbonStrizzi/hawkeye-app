import { PrismaAdapter } from "@next-auth/prisma-adapter";
import { type GetServerSidePropsContext } from "next";
import {
  getServerSession,
  type NextAuthOptions,
  type DefaultSession,
} from "next-auth";
import { env } from "~/env.mjs";
import { prisma } from "~/server/db";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcrypt";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string(),
});

const hash = async (password: string) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
  const salt = await bcrypt.genSalt(10);
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
  const hashedPassword = await bcrypt.hash(password, salt);
  // eslint-disable-next-line @typescript-eslint/no-unsafe-return
  return hashedPassword;
};

/**
 * Module augmentation for `next-auth` types. Allows us to add custom properties to the `session`
 * object and keep type safety.
 *
 * @see https://next-auth.js.org/getting-started/typescript#module-augmentation
 */
declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: string;
      // ...other properties
      // role: UserRole;
    } & DefaultSession["user"];
  }

  // interface User {
  //   // ...other properties
  //   // role: UserRole;
  // }
}

/**
 * Options for NextAuth.js used to configure adapters, providers, callbacks, etc.
 *
 * @see https://next-auth.js.org/configuration/options
 */
export const authOptions: NextAuthOptions = {
  callbacks: {
    session({ session, token }) {
      console.log("session", session);
      console.log("token", token);

      if (token) {
        session.user.id = token.sub as string;
      }

      return session;
    },
  },
  adapter: PrismaAdapter(prisma),
  providers: [
    CredentialsProvider({
      id: "Login",
      name: "Login",
      credentials: {
        email: { type: "email" },
        password: { type: "password" },
      },
      async authorize(credentials) {
        const user = await prisma.user.findUnique({
          where: {
            email: credentials?.email,
          },
        });

        if (!user) return Promise.reject(new Error("User not found"));

        if (user?.password && credentials?.password) {
          // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
          const isValidPassword = await bcrypt.compare(
            credentials?.password,
            user?.password
          );
          if (!isValidPassword) {
            return Promise.reject(new Error("Invalid password"));
          }
          return user;
        }
        return Promise.reject(new Error("Internal server error"));
      },
    }),
    CredentialsProvider({
      id: "SignUp",
      name: "SignUp",
      credentials: {
        email: { type: "email" },
        password: { type: "password" },
      },
      async authorize(credentials) {
        const creds = loginSchema.parse(credentials);

        const existingUser = await prisma.user.findUnique({
          where: {
            email: credentials?.email,
          },
        });

        if (existingUser) {
          return Promise.reject(new Error("User already exists"));
        }

        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
        const hashedPassword = await hash(creds.password);
        const user = await prisma.user.create({
          data: {
            email: credentials?.email,
            // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
            password: hashedPassword,
          },
        });

        return user;
      },
    }),
    GoogleProvider({
      clientId: env.GOOGLE_CLIENT_ID,
      clientSecret: env.GOOGLE_CLIENT_SECRET,
    }),
    /**
     * ...add more providers here.
     *
     * Most other providers require a bit more work than the Discord provider. For example, the
     * GitHub provider requires you to add the `refresh_token_expires_in` field to the Account
     * model. Refer to the NextAuth.js docs for the provider you want to use. Example:
     *
     * @see https://next-auth.js.org/providers/github
     */
  ],

  session: {
    strategy: "jwt",
  },
  secret: env.NEXTAUTH_SECRET,
};
/**
 * Wrapper for `getServerSession` so that you don't need to import the `authOptions` in every file.
 *
 * @see https://next-auth.js.org/configuration/nextjs
 */
export const getServerAuthSession = (ctx: {
  req: GetServerSidePropsContext["req"];
  res: GetServerSidePropsContext["res"];
}) => {
  return getServerSession(ctx.req, ctx.res, authOptions);
};
