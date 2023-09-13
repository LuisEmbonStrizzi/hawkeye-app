import { useState } from "react";
import AlignCorners from "../new-analysis/AlignCorners";
import Topbar from "./Topbar";
import Button from "../Button";
import type { Step } from "./Topbar";
import Recording from "../new-analysis/Recording";

const NewAnalysisSteps: React.FC = () => {
  const [step, setStep] = useState<number>(0);
  const handleStep = (stepState: Step) => {
    if (stepState === "more") {
      setStep(step + 1);
    } else {
      setStep(step - 1);
    }
  };

  return (
    <>
      <Topbar step={step} handleStep={handleStep} />
      {step === 0 ? (
        <AlignCorners image="/img/test.png" />
      ) : (
        <Recording handleStep={() => handleStep("more")} step={step} />
      )}
    </>
  );
};
export default NewAnalysisSteps;
