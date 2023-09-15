import React from "react";
import Button from "../Button";
import { useCopyToClipboard } from "@uidotdev/usehooks";
import { toast } from "react-hot-toast";
import Link from "next/link";

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

  return (
    <div className="mx-auto my-auto flex h-screen w-full max-w-xl flex-col items-center justify-center gap-6 p-6">
      <header className="fixed top-0 flex w-full items-center justify-center border-b border-background-border bg-background px-4 py-[10px] ">
        <div className="flex w-full max-w-7xl items-center justify-between whitespace-nowrap text-base font-semibold text-foreground-important">
          <Link href="/home">
            <Button
              style="secondary"
              icon={
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 15L7 10L12 5L13.0625 6.0625L9.125 10L13.0625 13.9375L12 15Z"
                    className="fill-secondary-foreground transition-all duration-150 ease-out group-hover:fill-foreground"
                  />
                </svg>
              }
              padding="icon"
            />
          </Link>
          GoPro Connection
          <Button
            style="secondary"
            icon={
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9.1665 14.1667H10.8332V9.16666H9.1665V14.1667ZM9.99984 7.49999C10.2359 7.49999 10.4339 7.42013 10.5936 7.26041C10.7533 7.10068 10.8332 6.90277 10.8332 6.66666C10.8332 6.43055 10.7533 6.23263 10.5936 6.07291C10.4339 5.91318 10.2359 5.83332 9.99984 5.83332C9.76373 5.83332 9.56581 5.91318 9.40609 6.07291C9.24637 6.23263 9.1665 6.43055 9.1665 6.66666C9.1665 6.90277 9.24637 7.10068 9.40609 7.26041C9.56581 7.42013 9.76373 7.49999 9.99984 7.49999ZM9.99984 18.3333C8.84706 18.3333 7.76373 18.1146 6.74984 17.6771C5.73595 17.2396 4.854 16.6458 4.104 15.8958C3.354 15.1458 2.76025 14.2639 2.32275 13.25C1.88525 12.2361 1.6665 11.1528 1.6665 9.99999C1.6665 8.84721 1.88525 7.76388 2.32275 6.74999C2.76025 5.7361 3.354 4.85416 4.104 4.10416C4.854 3.35416 5.73595 2.76041 6.74984 2.32291C7.76373 1.88541 8.84706 1.66666 9.99984 1.66666C11.1526 1.66666 12.2359 1.88541 13.2498 2.32291C14.2637 2.76041 15.1457 3.35416 15.8957 4.10416C16.6457 4.85416 17.2394 5.7361 17.6769 6.74999C18.1144 7.76388 18.3332 8.84721 18.3332 9.99999C18.3332 11.1528 18.1144 12.2361 17.6769 13.25C17.2394 14.2639 16.6457 15.1458 15.8957 15.8958C15.1457 16.6458 14.2637 17.2396 13.2498 17.6771C12.2359 18.1146 11.1526 18.3333 9.99984 18.3333ZM9.99984 16.6667C11.8609 16.6667 13.4373 16.0208 14.729 14.7292C16.0207 13.4375 16.6665 11.8611 16.6665 9.99999C16.6665 8.13888 16.0207 6.56249 14.729 5.27082C13.4373 3.97916 11.8609 3.33332 9.99984 3.33332C8.13873 3.33332 6.56234 3.97916 5.27067 5.27082C3.979 6.56249 3.33317 8.13888 3.33317 9.99999C3.33317 11.8611 3.979 13.4375 5.27067 14.7292C6.56234 16.0208 8.13873 16.6667 9.99984 16.6667Z"
                  className="fill-secondary-foreground transition-all duration-150 ease-out group-hover:fill-foreground"
                />
              </svg>
            }
            padding="icon"
          />
        </div>
      </header>
      <div className="flex w-full justify-center pb-8">
        <svg
          width="128"
          height="128"
          viewBox="0 0 128 128"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M30.9333 80.4L22.5333 72C28.7556 65.7778 35.2667 61.1111 42.0667 58C48.8667 54.8889 56.1778 53.3333 64 53.3333C71.8222 53.3333 79.1333 54.8889 85.9333 58C92.7333 61.1111 99.2444 65.7778 105.467 72L97.0667 80.4C91.6445 74.9778 86.1778 71.1111 80.6667 68.8C75.1556 66.4889 69.6 65.3333 64 65.3333C58.4 65.3333 52.8444 66.4889 47.3333 68.8C41.8222 71.1111 36.3556 74.9778 30.9333 80.4ZM8.4 57.8666L0 49.4666C8.26667 41.0222 17.8889 34.2222 28.8667 29.0666C39.8444 23.9111 51.5556 21.3333 64 21.3333C76.4444 21.3333 88.1556 23.9111 99.1333 29.0666C110.111 34.2222 119.733 41.0222 128 49.4666L119.6 57.8666C111.778 50.4 103.222 44.4444 93.9333 40C84.6445 35.5555 74.6667 33.3333 64 33.3333C53.3333 33.3333 43.3556 35.5555 34.0667 40C24.7778 44.4444 16.2222 50.4 8.4 57.8666ZM64 113.467L83.7333 93.6C81.1556 91.0222 78.2 89 74.8667 87.5333C71.5333 86.0667 67.9111 85.3333 64 85.3333C60.0889 85.3333 56.4667 86.0667 53.1333 87.5333C49.8 89 46.8444 91.0222 44.2667 93.6L64 113.467Z"
            fill="#4ECB71"
          />
        </svg>
      </div>

      <h1 className="w-full text-center text-3xl font-semibold text-foreground-important sm:text-left">
        Connect to <span className="text-primary">{networkName}</span> Network
      </h1>
      <p className="text-center text-foreground sm:text-left">
        This will allow us to establish a connection with the camera. Please
        copy the password and connect with the serialized network before
        continuing.
      </p>
      <div className="flex w-full flex-col gap-4">
        <div className="flex flex-1 flex-grow items-center justify-between gap-2 rounded-md bg-secondary-background py-2 pl-4 pr-2 text-foreground">
          {password}
          <Button
            style="secondary"
            onClick={() => {
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

/*

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


*/
