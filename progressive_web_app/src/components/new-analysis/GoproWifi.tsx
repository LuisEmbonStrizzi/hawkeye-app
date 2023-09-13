import React from "react";
import Button from "../Button";
import { useCopyToClipboard } from "@uidotdev/usehooks";
import { toast } from "react-hot-toast";

type GoproWifiProps = {
  name: string;
  password: string;
  firstOnClick: () => void;
};

const GoproWifi: React.FC<GoproWifiProps> = ({
  name,
  password,
  firstOnClick,
}) => {
  const [copiedText, copyToClipboard] = useCopyToClipboard();
  const hasCopiedText = Boolean(copiedText);

  const goproPassword = password;
  const goproName = name;

  return (
    <div className="mx-auto my-auto max-w-xl flex h-screen w-full flex-col items-center justify-center gap-6 p-6">
      <h1 className="text-3xl w-full font-semibold text-foreground-important">
        Connect to <span className="text-primary">{goproName}</span> Network
      </h1>
      <p className="text-foreground">
        This will allow us to establish a connection with the camera. Please
        copy the password and connect with the serialized network before continuing.
      </p>
      <div className="w-full flex flex-col gap-4">
        <div className="py-2 pl-4 pr-2 flex-1 flex-grow bg-background-border text-foreground rounded-md flex items-center justify-between gap-2">
          {goproPassword}
          <Button style="secondary" onClick={()=>{void copyToClipboard(goproPassword); toast.success("Network password copied to clipboard")}} label="Copy" />
        </div>
        <Button style="primary" label="Continue" onClick={firstOnClick} />
      </div>
    </div>
  );
};
export default GoproWifi;
