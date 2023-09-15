import React from "react";
import Button from "../Button";
import Link from "next/link";

type ErrorProps = {
  firstOnClick: () => void;
};

const Error: React.FC<ErrorProps> = ({ firstOnClick }) => {
  return (
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-6 p-6">
      {" "}
      <svg
        width="128"
        height="128"
        viewBox="0 0 128 128"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M117.333 91.3333L95.9998 70V84.8L87.9998 76.8V29.3333H40.5332L32.5332 21.3333H87.9998C90.1332 21.3333 91.9998 22.1333 93.5998 23.7333C95.1998 25.3333 95.9998 27.2 95.9998 29.3333V58L117.333 36.6667V91.3333ZM113.066 124.4L5.19983 16.5333L10.7998 10.9333L118.666 118.8L113.066 124.4ZM21.1998 21.3333L29.1998 29.3333H18.6665V98.6667H87.9998V88.1333L95.9998 96.1333V98.6667C95.9998 100.8 95.1998 102.667 93.5998 104.267C91.9998 105.867 90.1332 106.667 87.9998 106.667H18.6665C16.5332 106.667 14.6665 105.867 13.0665 104.267C11.4665 102.667 10.6665 100.8 10.6665 98.6667V29.3333C10.6665 27.2 11.4665 25.3333 13.0665 23.7333C14.6665 22.1333 16.5332 21.3333 18.6665 21.3333H21.1998Z"
          fill="#1F2331"
        />
      </svg>
      <h2 className="text-3xl font-bold text-foreground-important">
        Whoops...
      </h2>
      <p className="text-center font-medium text-foreground">
        An error happened while trying to connect to the cameras.
      </p>
      <div className="mt-4 flex w-full max-w-sm flex-col gap-4">
        <Link href={"/home"} className="flex flex-col">
          <Button label="Go back" style="secondary" />
        </Link>
        <Button label="Try again" style="primary" onClick={firstOnClick} />
      </div>
    </div>
  );
};
export default Error;
