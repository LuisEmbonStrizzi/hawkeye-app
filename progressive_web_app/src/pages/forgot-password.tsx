/* eslint-disable @typescript-eslint/no-misused-promises */
import { type NextPage } from "next";
import { api } from "~/utils/api";

const ForgotPassword: NextPage = () => {
  const send = api.user.sendEmail.useMutation();

  function sendEmail() {
    send.mutate({ email: "luisembon@gmail.com" });
  }
  return (
    <>
      <h1>ForgotPassword</h1>
      <button onClick={sendEmail}>Send email</button>
    </>
  );
};

export default ForgotPassword;
