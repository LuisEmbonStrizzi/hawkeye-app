import React from "react";
import Button from "../Button";
import { useCopyToClipboard } from "@uidotdev/usehooks";
import { toast } from "react-hot-toast";
type GoproWifiProps = {
  networkName?: string;
  password?: string;
  firstOnClick: () => void;
};

const GoproWifi: React.FC<GoproWifiProps> = ({
  networkName,
  password,
  firstOnClick,
}) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
  const [copiedText, copyToClipboard] = useCopyToClipboard();
  const hasCopiedText = Boolean(copiedText);
  console.log("networkName:", networkName);
  console.log("password:", password);

  return (
    <div className="mx-auto my-auto flex h-screen w-full max-w-xl flex-col items-center justify-center gap-6 p-6">
      <h1 className="w-full text-3xl font-semibold text-foreground-important">
        Connect to <span className="text-primary">{networkName}</span> Network
      </h1>
      <p className="text-foreground">
        This will allow us to establish a connection with the camera. Please
        copy the password and connect with the serialized network before
        continuing.
      </p>
      <div className="flex w-full flex-col gap-4">
        <div className="flex flex-1 flex-grow items-center justify-between gap-2 rounded-md bg-background-border py-2 pl-4 pr-2 text-foreground">
          {password}
          <Button
            style="secondary"
            onClick={() => {
              // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-non-null-assertion
              void copyToClipboard(password!);
              toast.success("Network password copied to clipboard");
            }}
            label="Copy"
          />
        </div>
        <Button style="primary" label="Continue" onClick={firstOnClick} />
      </div>
    </div>
  );
};
export default GoproWifi;
