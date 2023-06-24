import { type NextPage } from "next";
import { signOut, useSession } from "next-auth/react";
import Button from "~/components/Button";
import { api } from "~/utils/api";

const Home: NextPage = () => {
  const { data: sessionData } = useSession();

  const { data: secretMessage } = api.example.getSecretMessage.useQuery(
    undefined, // no input
    { enabled: sessionData?.user !== undefined }
  );
  return (
    <>
      <div className="w-1/4 bg-secondary-background">
        <div className="flex flex-col gap-[20px] p-20 text-center">
          <p className="flex flex-col gap-[10px] text-center text-xl text-gray-500 ">
            {sessionData && (
              <span>
                Logged in as{" "}
                {sessionData.user?.name ||
                  sessionData.user.email?.split("@")[0]}
              </span>
            )}
            {secretMessage && <span> {secretMessage}</span>}
            {sessionData && (
              <Button
                style="primary"
                label="Sign out"
                onClick={() => void signOut({ callbackUrl: "/log-in" })}
              />
            )}
          </p>
        </div>
      </div>
    </>
  );
};

export default Home;
