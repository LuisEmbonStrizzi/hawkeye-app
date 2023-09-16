import { useEffect, useState } from "react";
import AlignCorners from "../new-analysis/AlignCorners";
import Topbar from "./Topbar";
import type { Step } from "./Topbar";
import Recording from "../new-analysis/Recording";
import {
  type TrecordResponse,
  type cameraData,
} from "~/server/api/routers/videos";
import axios from "axios";
import { type InferGetServerSidePropsType } from "next/types";
import { type TgetBattery } from "~/server/api/routers/videos";
import Loading from "../new-analysis/Loading";
type courtData = {
  message: string;
  file_url: string;
};

const NewAnalysisSteps: React.FC = () => {
  const [courtData, setCourtData] = useState<courtData | null>(null); // Define un estado para almacenar los datos
  const [battery, setBattery] = useState<number>(0);
  async function getBattery() {
    try {
      // const getBattery: TgetBattery = await axios.get(
      //   "http://localhost:8000/getBattery",
      //   {
      //     responseType: "json",
      //   }
      // );
      // console.log(getBattery);
      const battery = 90;
      setBattery(battery);
    } catch (error) {
      console.error("Error al obtener los datos:", error);
    }
  }

  useEffect(() => {
    // Dentro de useEffect, puedes hacer una solicitud para obtener los datos cuando el componente se monte
    async function getCourtPhoto() {
      try {
        // const record: cameraData = await axios.get(
        //   "http://127.0.0.1:8000/courtPhoto",
        //   {
        //     responseType: "json",
        //   }
        // );
        setTimeout(() => {
          setCourtData({
            message: "Cancha encontrada",
            file_url: "/img/cancha.jpg",
          });
        }, 7000);
      } catch (err: unknown) {
        console.log(err);
      }
    }

    void getBattery();
    void getCourtPhoto();
  }, []);

  const [alignedCorners, setAlignedCorners] = useState<boolean>(false);

  return (
    <>
      {alignedCorners ? (
        <Recording initialBattery={90} />
      ) : courtData !== null ? (
        <AlignCorners
          image={courtData?.file_url}
          firstOnClick={() => setAlignedCorners(true)}
        />
      ) : (
        <Loading loadingText="Fetching court image..." />
      )}
    </>
  );
};
export default NewAnalysisSteps;

/*

        <AlignCorners
          image={courtData?.file_url}
          firstOnClick={() => setAlignedCorners(true)}
        />

*/
