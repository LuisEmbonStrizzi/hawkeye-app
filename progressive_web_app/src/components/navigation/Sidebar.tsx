import React from "react";
import Profile from "../Profile";

const Sidebar: React.FC = () => {
  return (
    <div className="fixed left-0 top-0 flex h-full w-[280px] flex-col justify-between border-r border-background-border bg-background p-4 text-sm text-foreground-important">
      Sidebar
      <Profile />
    </div>
  );
};
export default Sidebar;
