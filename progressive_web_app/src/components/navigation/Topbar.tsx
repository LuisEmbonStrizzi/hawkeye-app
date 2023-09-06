import React from "react";
import Button from "../Button";
import Badge from "../Badge";
import { useState } from "react";
import Link from "next/link";

const Topbar: React.FC = () => {
  const [step, setStep] = useState<number>(0);

  return (
    <header className="fixed top-0 flex w-full items-center border-b border-background-border bg-background px-4 py-[10px] text-sm text-foreground-important">
      <div className="flex w-full items-center justify-start">
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
                  fill="#596585"
                />
              </svg>
            }
            padding="icon"
          />
        </Link>
      </div>
      <div className="flex w-full items-center justify-center gap-2 whitespace-nowrap text-base font-semibold text-foreground-important">
        Align corners <Badge label="0/2" />
      </div>
      <div className="flex w-full items-center justify-end lg:hidden">
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
                fill="#596585"
              />
            </svg>
          }
          padding="icon"
        />
      </div>
      <div className="hidden w-full items-center justify-end lg:flex">
        <Button
          style="primary"
          icon={
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M8 15L6.9375 13.9375L10.875 10L6.9375 6.0625L8 5L13 10L8 15Z"
                fill="#181B27"
              />
            </svg>
          }
          label="Next step"
          padding="both-left"
        />
      </div>
    </header>
  );
};
export default Topbar;
