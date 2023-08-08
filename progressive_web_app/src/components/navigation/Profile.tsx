import React from "react";
import { signOut, useSession } from "next-auth/react";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";

const Profile: React.FC = () => {
  const { data: sessionData } = useSession();
  const [open, setOpen] = useState<boolean>(false);
  const ref = useRef<HTMLDivElement>(null);

  const handleClickOutside = (event: MouseEvent) => {
    if (ref.current && !ref.current.contains(event.target as Node)) {
      setOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={ref} className="relative flex flex-col">
      {open && (
        <div className="absolute bottom-full left-0 z-20 mb-[10px] w-full rounded-md border border-tertiary-border bg-tertiary-background py-[5px]  shadow-lg backdrop-blur-[8px]">
          <nav role="none">
            <ul>
              <li className="group mx-[5px] flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-xs text-foreground-important transition-all duration-300 ease-in-out hover:bg-tertiary-hover/75">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M7.64583 18.3333L7.33333 15.7083C7.19444 15.625 7.04167 15.5347 6.875 15.4375C6.70833 15.3403 6.55556 15.25 6.41667 15.1667L3.97917 16.1875L1.625 12.125L3.70833 10.5417V9.45834L1.625 7.87501L3.97917 3.81251L6.41667 4.83334C6.55556 4.75001 6.70833 4.65973 6.875 4.56251C7.04167 4.46528 7.19444 4.37501 7.33333 4.29167L7.64583 1.66667H12.3542L12.6667 4.29167C12.8056 4.37501 12.9583 4.46528 13.125 4.56251C13.2917 4.65973 13.4444 4.75001 13.5833 4.83334L16.0208 3.81251L18.375 7.87501L16.3125 9.45834V10.5417L18.375 12.125L16.0208 16.1875L13.5833 15.1667C13.4444 15.25 13.2917 15.3403 13.125 15.4375C12.9583 15.5347 12.8056 15.625 12.6667 15.7083L12.3542 18.3333H7.64583ZM10 12.9792C10.8194 12.9792 11.5208 12.6875 12.1042 12.1042C12.6875 11.5208 12.9792 10.8195 12.9792 10C12.9792 9.18056 12.6875 8.47917 12.1042 7.89584C11.5208 7.31251 10.8194 7.02084 10 7.02084C9.18056 7.02084 8.47917 7.31251 7.89583 7.89584C7.3125 8.47917 7.02083 9.18056 7.02083 10C7.02083 10.8195 7.3125 11.5208 7.89583 12.1042C8.47917 12.6875 9.18056 12.9792 10 12.9792ZM10 11.2292C9.66667 11.2292 9.37847 11.1076 9.13542 10.8646C8.89236 10.6215 8.77083 10.3333 8.77083 10C8.77083 9.66667 8.89236 9.37848 9.13542 9.13542C9.37847 8.89237 9.66667 8.77084 10 8.77084C10.3333 8.77084 10.6215 8.89237 10.8646 9.13542C11.1076 9.37848 11.2292 9.66667 11.2292 10C11.2292 10.3333 11.1076 10.6215 10.8646 10.8646C10.6215 11.1076 10.3333 11.2292 10 11.2292ZM9.16667 16.5833H10.8333L11.0833 14.4167C11.4861 14.3056 11.875 14.1389 12.25 13.9167C12.625 13.6945 12.9653 13.4306 13.2708 13.125L15.2917 13.9792L16.125 12.6042L14.3542 11.25C14.4236 11.0556 14.4722 10.8542 14.5 10.6458C14.5278 10.4375 14.5417 10.2222 14.5417 10C14.5417 9.80556 14.5278 9.60765 14.5 9.40626C14.4722 9.20487 14.4306 8.99306 14.375 8.77084L16.1458 7.39584L15.3125 6.02084L13.2917 6.89584C12.9722 6.57639 12.6285 6.30903 12.2604 6.09376C11.8924 5.87848 11.5069 5.71528 11.1042 5.60417L10.8333 3.41667H9.16667L8.89583 5.60417C8.49306 5.71528 8.10764 5.87848 7.73958 6.09376C7.37153 6.30903 7.03472 6.56945 6.72917 6.87501L4.70833 6.02084L3.875 7.39584L5.625 8.75001C5.56944 8.97223 5.52778 9.18751 5.5 9.39584C5.47222 9.60417 5.45833 9.80556 5.45833 10C5.45833 10.1945 5.47222 10.3924 5.5 10.5938C5.52778 10.7951 5.56944 11.007 5.625 11.2292L3.875 12.6042L4.70833 13.9792L6.72917 13.125C7.03472 13.4306 7.37153 13.691 7.73958 13.9063C8.10764 14.1215 8.49306 14.2847 8.89583 14.3958L9.16667 16.5833Z"
                    className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
                  />
                </svg>
                Settings
              </li>
              <li className="group mx-[5px] flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-xs text-foreground-important transition-all duration-300 ease-in-out hover:bg-tertiary-hover/75">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10 15C10.2778 15 10.5139 14.9028 10.7083 14.7083C10.9028 14.5139 11 14.2778 11 14C11 13.7222 10.9028 13.4861 10.7083 13.2917C10.5139 13.0972 10.2778 13 10 13C9.72222 13 9.48611 13.0972 9.29167 13.2917C9.09722 13.4861 9 13.7222 9 14C9 14.2778 9.09722 14.5139 9.29167 14.7083C9.48611 14.9028 9.72222 15 10 15ZM9.25 11.8125H10.7708C10.7708 11.2986 10.816 10.934 10.9062 10.7188C10.9965 10.5035 11.2153 10.2292 11.5625 9.89583C12.0486 9.42361 12.3854 9.02083 12.5729 8.6875C12.7604 8.35417 12.8542 7.98611 12.8542 7.58333C12.8542 6.81944 12.5938 6.19792 12.0729 5.71875C11.5521 5.23958 10.8889 5 10.0833 5C9.375 5 8.76042 5.1875 8.23958 5.5625C7.71875 5.9375 7.35417 6.44444 7.14583 7.08333L8.5 7.64583C8.625 7.25694 8.82292 6.95486 9.09375 6.73958C9.36458 6.52431 9.68056 6.41667 10.0417 6.41667C10.4306 6.41667 10.75 6.52778 11 6.75C11.25 6.97222 11.375 7.26389 11.375 7.625C11.375 7.94444 11.2674 8.22917 11.0521 8.47917C10.8368 8.72917 10.5972 8.97222 10.3333 9.20833C9.84722 9.65278 9.54514 10.0174 9.42708 10.3021C9.30903 10.5868 9.25 11.0903 9.25 11.8125ZM10 18C8.90278 18 7.86806 17.7917 6.89583 17.375C5.92361 16.9583 5.07292 16.3854 4.34375 15.6562C3.61458 14.9271 3.04167 14.0764 2.625 13.1042C2.20833 12.1319 2 11.0972 2 10C2 8.88889 2.20833 7.85069 2.625 6.88542C3.04167 5.92014 3.61458 5.07292 4.34375 4.34375C5.07292 3.61458 5.92361 3.04167 6.89583 2.625C7.86806 2.20833 8.90278 2 10 2C11.1111 2 12.1493 2.20833 13.1146 2.625C14.0799 3.04167 14.9271 3.61458 15.6562 4.34375C16.3854 5.07292 16.9583 5.92014 17.375 6.88542C17.7917 7.85069 18 8.88889 18 10C18 11.0972 17.7917 12.1319 17.375 13.1042C16.9583 14.0764 16.3854 14.9271 15.6562 15.6562C14.9271 16.3854 14.0799 16.9583 13.1146 17.375C12.1493 17.7917 11.1111 18 10 18ZM10 16.5C11.8056 16.5 13.3403 15.8681 14.6042 14.6042C15.8681 13.3403 16.5 11.8056 16.5 10C16.5 8.19444 15.8681 6.65972 14.6042 5.39583C13.3403 4.13194 11.8056 3.5 10 3.5C8.19444 3.5 6.65972 4.13194 5.39583 5.39583C4.13194 6.65972 3.5 8.19444 3.5 10C3.5 11.8056 4.13194 13.3403 5.39583 14.6042C6.65972 15.8681 8.19444 16.5 10 16.5Z"
                    className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
                  />
                </svg>
                Help
              </li>
              <div className="my-[5px] h-[1px] bg-tertiary-border"></div>
              <li
                onClick={() => void signOut({ callbackUrl: "/log-in" })}
                className="group mx-[5px] flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-xs text-foreground-important transition-all duration-300 ease-in-out hover:bg-tertiary-hover/75"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M4.5 17C4.0875 17 3.73437 16.8531 3.44062 16.5594C3.14687 16.2656 3 15.9125 3 15.5V4.5C3 4.0875 3.14687 3.73438 3.44062 3.44063C3.73437 3.14688 4.0875 3 4.5 3H10V4.5H4.5V15.5H10V17H4.5ZM13.5 13.5L12.4375 12.4375L14.125 10.75H8V9.25H14.125L12.4375 7.5625L13.5 6.5L17 10L13.5 13.5Z"
                    className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
                  />
                </svg>
                Sign Out
              </li>
            </ul>
          </nav>
        </div>
      )}
      <button
        onClick={() => {
          setOpen(!open);
        }}
        className="group flex items-center gap-[10px] overflow-hidden rounded-md p-[10px] transition-all duration-300 ease-in-out hover:bg-secondary-background"
      >
        <span className="flex-shrink-0 flex h-6 w-6 select-none items-center justify-center rounded-[3px] bg-primary text-[10px] font-bold text-background">
          {sessionData?.user.email?.slice(0, 2).toUpperCase()}
        </span>
        <p className="flex-grow overflow-hidden text-left whitespace-nowrap select-none text-ellipsis text-sm font-normal text-foreground-important">
          {sessionData?.user.email}
        </p>
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="flex-shrink-0"
        >
          <path
            d="M6.46155 13C6.18655 13 5.95113 12.9021 5.7553 12.7063C5.55946 12.5104 5.46155 12.275 5.46155 12C5.46155 11.725 5.55946 11.4896 5.7553 11.2938C5.95113 11.0979 6.18655 11 6.46155 11C6.73656 11 6.97199 11.0979 7.16782 11.2938C7.36366 11.4896 7.46157 11.725 7.46157 12C7.46157 12.275 7.36366 12.5104 7.16782 12.7063C6.97199 12.9021 6.73656 13 6.46155 13ZM12 13C11.725 13 11.4896 12.9021 11.2938 12.7063C11.0979 12.5104 11 12.275 11 12C11 11.725 11.0979 11.4896 11.2938 11.2938C11.4896 11.0979 11.725 11 12 11C12.275 11 12.5104 11.0979 12.7063 11.2938C12.9021 11.4896 13 11.725 13 12C13 12.275 12.9021 12.5104 12.7063 12.7063C12.5104 12.9021 12.275 13 12 13ZM17.5385 13C17.2635 13 17.0281 12.9021 16.8322 12.7063C16.6364 12.5104 16.5385 12.275 16.5385 12C16.5385 11.725 16.6364 11.4896 16.8322 11.2938C17.0281 11.0979 17.2635 11 17.5385 11C17.8135 11 18.0489 11.0979 18.2447 11.2938C18.4406 11.4896 18.5385 11.725 18.5385 12C18.5385 12.275 18.4406 12.5104 18.2447 12.7063C18.0489 12.9021 17.8135 13 17.5385 13Z"
            className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
          />
        </svg>
      </button>
    </div>
  );
};
export default Profile;
