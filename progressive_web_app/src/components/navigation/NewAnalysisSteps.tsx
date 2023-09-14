import { useState } from "react";
import AlignCorners from "../new-analysis/AlignCorners";
import Topbar from "./Topbar";
import type { Step } from "./Topbar";
import Recording, { getBattery } from "../new-analysis/Recording";
import {
  type TrecordResponse,
  type cameraData,
} from "~/server/api/routers/videos";
import axios from "axios";
import { type InferGetServerSidePropsType } from "next/types";

export async function getCourtPhoto() {
  try {
    const record: cameraData = await axios.get(
      "http://127.0.0.1:8000/courtPhoto",
      {
        responseType: "json",
      }
    );

    return record.data;
  } catch (err: unknown) {
    console.log(err);
  }
}

type NewAnalysisStepsProps = {
  image?: string;
  initialBattery?: number;
};

const NewAnalysisSteps: React.FC<NewAnalysisStepsProps> = ({
  image,
  initialBattery,
}) => {
  const [step, setStep] = useState<number>(0);
  const [recordData, setRecordData] = useState<string | null>(null);

  const handleStep = (stepState: Step) => {
    if (stepState === "more") {
      setStep(step + 1);
    } else {
      setStep(step - 1);
    }
  };

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
      }

      console.log(record.data.message);
    } catch (err: unknown) {
      console.log(err);
    }
  }

  return (
    <>
      <Topbar step={step} handleStep={handleStep} />
      {step === 0 ? (
        <AlignCorners image={image} />
      ) : (
        <Recording
          handleStep={() => handleStep("more")}
          step={step}
          startRecording={() => startRecording}
          recordData={recordData}
          initialBattery={initialBattery}
        />
      )}
    </>
  );
};
export default NewAnalysisSteps;

// export const getServerSideProps = async () => {
//   const courtPhoto = await getCourtPhoto();
//   const initialBattery = await getBattery();
//   console.log(courtPhoto);
//   return {
//     props: {
//       image: courtPhoto?.file_url,
//       initialBattery,
//     },
//   };
// };
