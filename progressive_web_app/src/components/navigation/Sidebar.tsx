import React from "react";
import Profile from "./Profile";
import Button from "../Button";
import Link from "next/link";
import clsx from "clsx";
import axios from "axios";

type ActiveItem = "analysis" | "favorites" | "downloads";
type SidebarItemProps = {
  activeItem: ActiveItem;
};

const Sidebar: React.FC<SidebarItemProps> = ({ activeItem }) => {
  
  return (
    <div className="fixed left-0 top-0 flex h-full w-72 flex-col justify-between border-r border-background-border bg-background p-4">
      <nav className="flex flex-col">
        <Link href={"/new-analysis"} className="flex flex-col">
          <Button style="primary" label="New analysis" />
        </Link>
        <div className="my-4 h-[1px] bg-background-border"></div>
        <Link
          href="/home"
          className={clsx(
            "group flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-sm font-medium transition-all duration-300 ease-in-out hover:bg-secondary-background",
            activeItem === "analysis"
              ? "text-primary"
              : "text-foreground hover:text-foreground-important"
          )}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M3.0625 17L2 15.9375L4.5 13.4375C5.125 12.8125 5.53125 12.2118 5.71875 11.6354C5.90625 11.059 6 10.0972 6 8.75C6 7.90278 6.17708 7.07639 6.53125 6.27083C6.88542 5.46528 7.39583 4.72917 8.0625 4.0625C9.28472 2.84028 10.6387 2.14583 12.1245 1.97917C13.6103 1.8125 14.8327 2.22222 15.7917 3.20833C16.75 4.19445 17.1458 5.42709 16.9792 6.90625C16.8125 8.38542 16.1319 9.72917 14.9375 10.9375C14.2708 11.6042 13.5347 12.1146 12.7292 12.4688C11.9236 12.8229 11.0972 13 10.25 13C8.90278 13 7.94097 13.0938 7.36458 13.2813C6.78819 13.4688 6.1875 13.875 5.5625 14.5L3.0625 17ZM8.25 10.75C8.88889 11.3889 9.76736 11.6215 10.8854 11.4479C12.0035 11.2743 12.9971 10.7485 13.8664 9.87042C14.7494 8.97842 15.2772 7.9784 15.4496 6.87038C15.6221 5.76235 15.3889 4.89583 14.75 4.27083C14.1111 3.64583 13.2326 3.4132 12.1146 3.57292C10.9965 3.73264 10 4.25 9.125 5.125C8.25 6 7.72569 6.99653 7.55208 8.11459C7.37847 9.23264 7.61111 10.1111 8.25 10.75ZM14 19.5C13.1667 19.5 12.4583 19.2083 11.875 18.625C11.2917 18.0417 11 17.3333 11 16.5C11 15.6667 11.2917 14.9583 11.875 14.375C12.4583 13.7917 13.1667 13.5 14 13.5C14.8333 13.5 15.5417 13.7917 16.125 14.375C16.7083 14.9583 17 15.6667 17 16.5C17 17.3333 16.7083 18.0417 16.125 18.625C15.5417 19.2083 14.8333 19.5 14 19.5ZM14.0044 18C14.4181 18 14.7708 17.8527 15.0625 17.5581C15.3542 17.2635 15.5 16.9093 15.5 16.4956C15.5 16.0819 15.3527 15.7292 15.0581 15.4375C14.7635 15.1458 14.4093 15 13.9956 15C13.5819 15 13.2292 15.1473 12.9375 15.4419C12.6458 15.7365 12.5 16.0907 12.5 16.5044C12.5 16.9181 12.6473 17.2708 12.9419 17.5625C13.2365 17.8542 13.5907 18 14.0044 18Z"
              className={clsx(
                "transition-all duration-300 ease-in-out",
                activeItem === "analysis"
                  ? "fill-primary"
                  : "fill-secondary-foreground "
              )}
            />
          </svg>
          Analysis
        </Link>
        <li className="group flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-sm font-medium text-secondary-foreground transition-all duration-300 ease-in-out hover:bg-secondary-background hover:text-foreground-important">
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M10 17.5L8.95833 16.5625C7.56944 15.3264 6.42361 14.2674 5.52083 13.3854C4.61806 12.5035 3.90625 11.7188 3.38542 11.0312C2.86458 10.3438 2.50347 9.71528 2.30208 9.14583C2.10069 8.57639 2 7.99306 2 7.39583C2 6.15972 2.42361 5.11806 3.27083 4.27083C4.11806 3.42361 5.15972 3 6.39583 3C7.07639 3 7.73611 3.14583 8.375 3.4375C9.01389 3.72917 9.55556 4.13889 10 4.66667C10.4444 4.13889 10.9861 3.72917 11.625 3.4375C12.2639 3.14583 12.9236 3 13.6042 3C14.8403 3 15.8819 3.42361 16.7292 4.27083C17.5764 5.11806 18 6.15972 18 7.39583C18 7.99306 17.9028 8.56944 17.7083 9.125C17.5139 9.68056 17.1563 10.2986 16.6354 10.9792C16.1146 11.6597 15.3993 12.4479 14.4896 13.3438C13.5799 14.2396 12.4167 15.3264 11 16.6042L10 17.5ZM10 15.4792C11.2917 14.3264 12.3542 13.3438 13.1875 12.5312C14.0208 11.7188 14.684 11.0104 15.1771 10.4062C15.6701 9.80208 16.0139 9.26389 16.2083 8.79167C16.4028 8.31944 16.5 7.85417 16.5 7.39583C16.5 6.57639 16.2222 5.88889 15.6667 5.33333C15.1111 4.77778 14.4236 4.5 13.6042 4.5C13.1181 4.5 12.6632 4.60069 12.2396 4.80208C11.816 5.00347 11.4514 5.28472 11.1458 5.64583L10.4167 6.5H9.58333L8.85417 5.64583C8.54861 5.28472 8.17708 5.00347 7.73958 4.80208C7.30208 4.60069 6.85417 4.5 6.39583 4.5C5.57639 4.5 4.88889 4.77778 4.33333 5.33333C3.77778 5.88889 3.5 6.57639 3.5 7.39583C3.5 7.85417 3.59028 8.30903 3.77083 8.76042C3.95139 9.21181 4.28125 9.73611 4.76042 10.3333C5.23958 10.9306 5.89931 11.6389 6.73958 12.4583C7.57986 13.2778 8.66667 14.2847 10 15.4792Z"
              className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
            />
          </svg>
          Favorites
        </li>
        <li className="group flex cursor-pointer select-none items-center gap-[10px] rounded-md p-[10px] text-sm font-medium text-secondary-foreground transition-all duration-300 ease-in-out hover:bg-secondary-background hover:text-foreground-important">
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M5.4941 16C5.08137 16 4.72917 15.8531 4.4375 15.5594C4.14583 15.2656 4 14.9125 4 14.5V13H5.5V14.5H14.5V13H16V14.5C16 14.9125 15.853 15.2656 15.5591 15.5594C15.2652 15.8531 14.9119 16 14.4992 16H5.4941ZM10 13L6 9L7.0625 7.9375L9.25 10.125V3H10.75V10.125L12.9375 7.9375L14 9L10 13Z"
              className="fill-secondary-foreground transition-all duration-300 ease-in-out group-hover:fill-foreground-important"
            />
          </svg>
          Downloads
        </li>
      </nav>
      <aside>
        <div className="my-4 h-[1px] bg-background-border"></div>
        <Profile />
      </aside>
    </div>
  );
};
export default Sidebar;
