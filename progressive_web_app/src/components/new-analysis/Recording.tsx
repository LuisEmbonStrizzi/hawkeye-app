import Button from "../Button";
import CamBattery from "./CamBattery";
import Counter from "./Counter";
import { api } from "~/utils/api";
import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
import clsx from "clsx";
import Image from "next/image";
import { TgetBattery, type TrecordResponse } from "~/server/api/routers/videos";
import Loading from "./Loading";
type Tbattery = {
  battery: string;
};

export type cameraData = {
  data: {
    message: string;
    file_url: string;
  };
};
export type cameraData2 = {
  data: {
    file_url: string;
  };
};

type RecordingProps = {
  initialBattery: number;
};

const Recording: React.FC<RecordingProps> = ({ initialBattery }) => {
  const [battery, setBattery] = useState<number>(initialBattery);
  const [recordData, setRecordData] = useState<string | null>(null);
  const [startRecord, setStartRecord] = useState<boolean>(false);
  const [stopRecord, setStopRecord] = useState<boolean>(false);
  const [continueRecord, setContinueRecord] = useState<boolean>(false);
  const [hasFetchedData, setHasFetchedData] = useState<boolean>(true);
  const [repe, setRepe] = useState<string>("");
  const [video, setVideo] = useState<boolean>(false);


  async function getBattery() {
    try {
      const getBattery: TgetBattery = await axios.get(
        "http://localhost:8000/getBattery",
        {
          responseType: "json",
        }
      );
      console.log(getBattery);
      setBattery(getBattery.data.battery);
      return getBattery.data.battery;
    } catch (error) {
      console.error("Error al obtener los datos:", error);
    }
  }
  useEffect(() => {

    if(!continueRecord) {
      const intervalId = setInterval(async () => {
        const updatedBattery = await getBattery();
        console.log(updatedBattery);
        if (updatedBattery !== null) {
          setBattery(updatedBattery!);
        }
      }, 30000);
  
      return () => clearInterval(intervalId);
    }
    else {
      const intervalId = setInterval(async () => {
        setBattery(battery - 1);
      }, 60000);
  
      return () => clearInterval(intervalId);
    }
    
  }, [continueRecord]);

  // const uploadVideo = api.videos.stopRecording.useMutation({
  //   onSuccess: () => {
  //     void refetchVideos();
  //   },
  // });
  // const { data: videos, refetch: refetchVideos } =
  //   api.videos.getVideo.useQuery();

  // function callHawkeye() {
  //   try {
  //     uploadVideo.mutate();
  //     setStopRecord(true);
  //     setContinueRecord(false)
  //     setHasFetchedData(true)
  //   } catch (err: unknown) {
  //     console.log(err);
  //   }
  // }

  async function startRecording() {
    try {
      const record: TrecordResponse = await axios.get(
        "http://127.0.0.1:8000/record",
        {
          responseType: "json",
        }
      );
      if (record.data.message === "RecordStarted") {
        // Aquí puedes manipular los datos recibidos del backend
        setRecordData(record.data.message);
        setStartRecord(true);
      }

      console.log(record.data.message);
    } catch (err: unknown) {
      console.log(err);
    }
  }

  async function stopRecording() {
    try {
      const stopRecording: cameraData = await axios.get(
        "http://127.0.0.1:8000/stopRecording",
        {
          responseType: "json",
        }
      );

      console.log(stopRecording)

      const analysedVideo: cameraData2 = await axios.post("http://localhost:8080/predict", {
        url: stopRecording.data.file_url,
        });
        

        if (analysedVideo.data.file_url !== null) {
          // Aquí puedes manipular los datos recibidos del backend
          setRepe(analysedVideo.data.file_url)
          setHasFetchedData(true)
        }
      }     
    catch (err: unknown) {
      console.log(err);
    }
  }


  const videoRef = useRef<HTMLVideoElement | null>(null);
  let hasReachedZoomMoment = false;
  const zoomMoment = 6.97;

  useEffect(() => {
    if (video && videoRef.current) {
      setInterval(() => {
        if (
          videoRef.current &&
          videoRef.current.currentTime >= zoomMoment &&
          !hasReachedZoomMoment
        ) {
          videoRef.current.pause();
          console.log(videoRef.current.currentTime);
          console.log(hasReachedZoomMoment);
        }
      }, 10);
    }
  }, [video, hasReachedZoomMoment]);

  const handleZoom = () => {
    if (videoRef.current) {
      hasReachedZoomMoment = true;
      void videoRef.current.play();
    }
  };

  const handleReplay = () => {
    if (videoRef.current) {
      hasReachedZoomMoment = false;
      videoRef.current.currentTime = 0;
      void videoRef.current.play();
    }
  };

  
  return (
    <div className="flex h-screen w-full">
      <aside
        className={clsx(
          video ? "hidden md:flex" : "flex",
          " h-full w-full flex-col border-background-border md:w-96 md:border-r"
        )}
      >
        <div className="flex flex-grow flex-col items-center justify-center px-8 py-16">
          <Counter startRecord={startRecord} stopRecord={stopRecord} />
        </div>
        <hr className="border-background-border" />
        <section className="flex flex-col gap-4 p-8">
          <Button
            style="primary"
            label="Call hawkeye"
            onClick={() => {
              setVideo(true);
              void stopRecording();
            }}
            icon={
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M10.0001 18.3333C8.8473 18.3333 7.76397 18.1146 6.75008 17.6771C5.73619 17.2396 4.85425 16.6458 4.10425 15.8958C3.35425 15.1458 2.7605 14.2639 2.323 13.25C1.8855 12.2361 1.66675 11.1528 1.66675 9.99999C1.66675 8.84721 1.8855 7.76388 2.323 6.74999C2.7605 5.7361 3.35425 4.85416 4.10425 4.10416C4.85425 3.35416 5.73619 2.76041 6.75008 2.32291C7.76397 1.88541 8.8473 1.66666 10.0001 1.66666C11.1529 1.66666 12.2362 1.88541 13.2501 2.32291C14.264 2.76041 15.1459 3.35416 15.8959 4.10416C16.6459 4.85416 17.2397 5.7361 17.6772 6.74999C18.1147 7.76388 18.3334 8.84721 18.3334 9.99999C18.3334 11.1528 18.1147 12.2361 17.6772 13.25C17.2397 14.2639 16.6459 15.1458 15.8959 15.8958C15.1459 16.6458 14.264 17.2396 13.2501 17.6771C12.2362 18.1146 11.1529 18.3333 10.0001 18.3333ZM10.0001 16.6667C11.8612 16.6667 13.4376 16.0208 14.7292 14.7292C16.0209 13.4375 16.6667 11.8611 16.6667 9.99999C16.6667 8.13888 16.0209 6.56249 14.7292 5.27082C13.4376 3.97916 11.8612 3.33332 10.0001 3.33332C8.13897 3.33332 6.56258 3.97916 5.27092 5.27082C3.97925 6.56249 3.33341 8.13888 3.33341 9.99999C3.33341 11.8611 3.97925 13.4375 5.27092 14.7292C6.56258 16.0208 8.13897 16.6667 10.0001 16.6667ZM10.0001 15C8.61119 15 7.43064 14.5139 6.45841 13.5417C5.48619 12.5694 5.00008 11.3889 5.00008 9.99999C5.00008 8.6111 5.48619 7.43055 6.45841 6.45832C7.43064 5.4861 8.61119 4.99999 10.0001 4.99999C11.389 4.99999 12.5695 5.4861 13.5417 6.45832C14.514 7.43055 15.0001 8.6111 15.0001 9.99999C15.0001 11.3889 14.514 12.5694 13.5417 13.5417C12.5695 14.5139 11.389 15 10.0001 15ZM10.0001 13.3333C10.9167 13.3333 11.7015 13.0069 12.3542 12.3542C13.007 11.7014 13.3334 10.9167 13.3334 9.99999C13.3334 9.08332 13.007 8.2986 12.3542 7.64582C11.7015 6.99305 10.9167 6.66666 10.0001 6.66666C9.08342 6.66666 8.29869 6.99305 7.64592 7.64582C6.99314 8.2986 6.66675 9.08332 6.66675 9.99999C6.66675 10.9167 6.99314 11.7014 7.64592 12.3542C8.29869 13.0069 9.08342 13.3333 10.0001 13.3333ZM10.0001 11.6667C9.54175 11.6667 9.14939 11.5035 8.823 11.1771C8.49661 10.8507 8.33342 10.4583 8.33342 9.99999C8.33342 9.54166 8.49661 9.1493 8.823 8.82291C9.14939 8.49652 9.54175 8.33332 10.0001 8.33332C10.4584 8.33332 10.8508 8.49652 11.1772 8.82291C11.5036 9.1493 11.6667 9.54166 11.6667 9.99999C11.6667 10.4583 11.5036 10.8507 11.1772 11.1771C10.8508 11.5035 10.4584 11.6667 10.0001 11.6667Z"
                  fill="#181B27"
                />
              </svg>
            }
            iconPosition="left"
          />
          <Button
            style="secondary"
            label="Finish recording"
            onClick={() => {
              setVideo(false);
              void startRecording();
            }}
            icon={
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M6.66675 13.3333H13.3334V6.66666H6.66675V13.3333ZM10.0001 18.3333C8.8473 18.3333 7.76397 18.1146 6.75008 17.6771C5.73619 17.2396 4.85425 16.6458 4.10425 15.8958C3.35425 15.1458 2.7605 14.2639 2.323 13.25C1.8855 12.2361 1.66675 11.1528 1.66675 9.99999C1.66675 8.84721 1.8855 7.76388 2.323 6.74999C2.7605 5.7361 3.35425 4.85416 4.10425 4.10416C4.85425 3.35416 5.73619 2.76041 6.75008 2.32291C7.76397 1.88541 8.8473 1.66666 10.0001 1.66666C11.1529 1.66666 12.2362 1.88541 13.2501 2.32291C14.264 2.76041 15.1459 3.35416 15.8959 4.10416C16.6459 4.85416 17.2397 5.7361 17.6772 6.74999C18.1147 7.76388 18.3334 8.84721 18.3334 9.99999C18.3334 11.1528 18.1147 12.2361 17.6772 13.25C17.2397 14.2639 16.6459 15.1458 15.8959 15.8958C15.1459 16.6458 14.264 17.2396 13.2501 17.6771C12.2362 18.1146 11.1529 18.3333 10.0001 18.3333ZM10.0001 16.6667C11.8612 16.6667 13.4376 16.0208 14.7292 14.7292C16.0209 13.4375 16.6667 11.8611 16.6667 9.99999C16.6667 8.13888 16.0209 6.56249 14.7292 5.27082C13.4376 3.97916 11.8612 3.33332 10.0001 3.33332C8.13897 3.33332 6.56258 3.97916 5.27092 5.27082C3.97925 6.56249 3.33341 8.13888 3.33341 9.99999C3.33341 11.8611 3.97925 13.4375 5.27092 14.7292C6.56258 16.0208 8.13897 16.6667 10.0001 16.6667Z"
                  className="fill-secondary-foreground transition-all duration-150 ease-out group-hover:fill-foreground"
                />
              </svg>
            }
            iconPosition="left"
          />
        </section>
        <hr className="border-background-border" />
        <section className="flex flex-col items-center justify-center gap-4 p-8">
          <CamBattery battery={battery} />
        </section>
      </aside>
      <section
        className={clsx(
          video ? "flex" : "hidden md:flex",
          "relative h-full w-full flex-col items-center justify-center gap-4 pt-[64px] "
        )}

      >
        <main className="min-h-screen bg-background">
    
  </main>
      {hasFetchedData ? (
          video ? (
            <>
            <div className="absolute top-0 z-10 flex w-full items-center justify-between gap-4 border-b border-background-border bg-background p-8 py-[10px] md:justify-end">
              {
                <div className="md:hidden">
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
                    onClick={() => setVideo(false)}
                  />
                </div>
              }
              <div className="flex gap-4">
                <Button
                  style="primary"
                  label="Zoom"
                  iconPosition="left"
                  onClick={handleZoom}
                  icon={
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M4.5 17C4.0875 17 3.73437 16.8531 3.44062 16.5594C3.14687 16.2656 3 15.9125 3 15.5V12H4.5V15.5H8V17H4.5ZM12 17V15.5H15.5V12H17V15.5C17 15.9125 16.8531 16.2656 16.5594 16.5594C16.2656 16.8531 15.9125 17 15.5 17H12ZM3 8V4.5C3 4.0875 3.14687 3.73438 3.44062 3.44063C3.73437 3.14688 4.0875 3 4.5 3H8V4.5H4.5V8H3ZM15.5 8V4.5H12V3H15.5C15.9125 3 16.2656 3.14688 16.5594 3.44063C16.8531 3.73438 17 4.0875 17 4.5V8H15.5ZM9.99529 14C8.88732 14 7.94444 13.6095 7.16667 12.8286C6.38889 12.0477 6 11.1033 6 9.99529C6 8.88732 6.39046 7.94444 7.17138 7.16667C7.95229 6.38889 8.89674 6 10.0047 6C11.1127 6 12.0556 6.39046 12.8333 7.17138C13.6111 7.95229 14 8.89674 14 10.0047C14 11.1127 13.6095 12.0556 12.8286 12.8333C12.0477 13.6111 11.1033 14 9.99529 14ZM10 12.5C10.6944 12.5 11.2847 12.2569 11.7708 11.7708C12.2569 11.2847 12.5 10.6944 12.5 10C12.5 9.30556 12.2569 8.71528 11.7708 8.22917C11.2847 7.74306 10.6944 7.5 10 7.5C9.30556 7.5 8.71528 7.74306 8.22917 8.22917C7.74306 8.71528 7.5 9.30556 7.5 10C7.5 10.6944 7.74306 11.2847 8.22917 11.7708C8.71528 12.2569 9.30556 12.5 10 12.5Z"
                        className="fill-background"
                      />
                    </svg>
                  }
                  padding="both-right"
                />
                <Button
                  style="secondary"
                  onClick={handleReplay}
                  icon={
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M10 18.125C9.02778 18.125 8.11713 17.9403 7.26806 17.5708C6.41898 17.2014 5.68009 16.7023 5.0514 16.0736C4.42269 15.4449 3.92361 14.706 3.55417 13.8569C3.18472 13.0079 3 12.0972 3 11.125H4.5C4.5 12.6389 5.03819 13.934 6.11458 15.0104C7.19097 16.0868 8.48611 16.625 10 16.625C11.5139 16.625 12.809 16.0868 13.8854 15.0104C14.9618 13.934 15.5 12.6389 15.5 11.125C15.5 9.61111 14.9618 8.31597 13.8854 7.23958C12.809 6.16319 11.5112 5.625 9.99187 5.625H9.875L10.9375 6.6875L9.875 7.75L7 4.875L9.875 2L10.9375 3.0625L9.85417 4.125H10C10.9722 4.125 11.8829 4.30972 12.7319 4.67917C13.581 5.04861 14.3199 5.54769 14.9486 6.1764C15.5773 6.80509 16.0764 7.54398 16.4458 8.39306C16.8153 9.24213 17 10.1528 17 11.125C17 12.0972 16.8153 13.0079 16.4458 13.8569C16.0764 14.706 15.5773 15.4449 14.9486 16.0736C14.3199 16.7023 13.581 17.2014 12.7319 17.5708C11.8829 17.9403 10.9722 18.125 10 18.125Z"
                        className="fill-secondary-foreground transition-all duration-150 ease-out group-hover:fill-foreground"
                      />
                    </svg>
                  }
                  padding="icon"
                />
              </div>
            </div>
                <video autoPlay className="h-full" ref={videoRef} controls>
                  <source src={repe} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>            
          </>
          ) : (
            <>
            {" "}
            <h1 className="text-3xl font-semibold text-foreground-important">
              No hawkeye call yet
            </h1>
            <p className="text-foreground">
              Here you will see the clip of the point you want to analyze.
            </p>
          </>
          )
        ) : (
          <Loading loadingText="Fetching GoPro network..." />
        )}
      </section>
    </div>
  );
};
export default Recording;
