import React from "react";
import Profile from "../Profile";
import Button from "../Button";

const Sidebar: React.FC = () => {
  return (
    <div className="fixed left-0 top-0 flex h-full w-[280px] flex-col justify-between border-r border-background-border bg-background p-4 text-sm text-foreground-important">
      <Button style="primary" label="New analysis" />
      <div>
        <div className="h-[1px] bg-background-border my-4"></div>
        <Profile />
      </div>
    </div>
  );
};
export default Sidebar;
