import React from "react";
import Button from "../Button";
import { useCopyToClipboard } from "@uidotdev/usehooks";

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
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-6 p-6">
      <h1 className="text-3xl font-semibold text-foreground-important">
        Connect to the Gopro&apos; Wifi Network
      </h1>
      <p className="text-foreground">
        This will allow us to establish a connection with the camera. Please
        copy the name and password and enter the Wifi Network before continuing.
      </p>
      <div className="flex items-center justify-center gap-4">
        <input value={goproName} className="relative w-full rounded-lg border border-secondary-border bg-secondary-background p-[10px] pr-[40px] text-sm text-foreground-important outline-none transition-all duration-300 ease-out focus:border-primary focus:ring-2 focus:ring-primary/30" />
        <Button style="secondary" onClick={void copyToClipboard(goproName)} />
      </div>
      <div className="relative">
        <input className="relative w-full rounded-lg border border-secondary-border bg-secondary-background p-[10px] pr-[40px] text-sm text-foreground-important outline-none transition-all duration-300 ease-out focus:border-primary focus:ring-2 focus:ring-primary/30" />
        <Button style="secondary" onClick={void copyToClipboard(goproPassword)} />
      </div>
      <Button style="primary" label="Continue" onClick={firstOnClick} />
    </div>
  );
};
export default GoproWifi;
