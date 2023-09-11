import React from "react";
import Button from "../Button";

type LoadingProps = {
  firstOnClick: () => void;
  secondOnClick: () => void;
};

const Loading: React.FC<LoadingProps> = ({ firstOnClick, secondOnClick }) => {
  return (
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-4 p-4">
      <svg
        width="48"
        height="49"
        viewBox="0 0 48 49"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="animate-spin"
      >
        <path
          d="M24 44.5C21.2 44.5 18.5833 43.9833 16.15 42.95C13.7167 41.9167 11.6 40.5 9.8 38.7C8 36.9 6.58333 34.7833 5.55 32.35C4.51667 29.9167 4 27.3 4 24.5C4 21.7 4.51667 19.0833 5.55 16.65C6.58333 14.2167 8 12.1 9.8 10.3C11.6 8.5 13.7167 7.08333 16.15 6.05C18.5833 5.01667 21.2 4.5 24 4.5C24.4 4.5 24.75 4.65 25.05 4.95C25.35 5.25 25.5 5.6 25.5 6C25.5 6.4 25.35 6.75 25.05 7.05C24.75 7.35 24.4 7.5 24 7.5C19.3 7.5 15.2917 9.15833 11.975 12.475C8.65833 15.7917 7 19.8 7 24.5C7 29.2 8.65833 33.2083 11.975 36.525C15.2917 39.8417 19.3 41.5 24 41.5C28.7 41.5 32.7083 39.8417 36.025 36.525C39.3417 33.2083 41 29.2 41 24.5C41 24.1 41.15 23.75 41.45 23.45C41.75 23.15 42.1 23 42.5 23C42.9 23 43.25 23.15 43.55 23.45C43.85 23.75 44 24.1 44 24.5C44 27.3 43.4833 29.9167 42.45 32.35C41.4167 34.7833 40 36.9 38.2 38.7C36.4 40.5 34.2833 41.9167 31.85 42.95C29.4167 43.9833 26.8 44.5 24 44.5Z"
          className="fill-primary"
        />
      </svg>
      <p className="font-medium text-foreground-important">
        Loading cameras...
      </p>
      <div className="flex w-full flex-col items-center justify-center gap-4 sm:flex-row">
        <Button label="Success" style="primary" onClick={firstOnClick} />
        <Button label="Failure" style="secondary" onClick={secondOnClick} />
      </div>
    </div>
  );
};
export default Loading;
