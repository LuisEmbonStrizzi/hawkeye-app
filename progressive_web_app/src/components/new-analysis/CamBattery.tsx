import { motion, useAnimation } from "framer-motion";
import { useEffect } from "react";

type CamBatteryProps = {
  battery?: number;
};

const CamBattery: React.FC<CamBatteryProps> = ({ battery }) => {
  const radius = 100;
  const circumference = 2 * Math.PI * radius;
  const percentage = (battery && (battery / 100 * circumference))

  const circleAnimation = useAnimation();

  useEffect(() => {
    void circleAnimation.start({
      strokeDasharray: `${percentage}px ${circumference}px`,
      strokeDashoffset: 0,
    });
  }, [circleAnimation, percentage, circumference]);

  const svgMeasure = 2 * radius + 40;

  return (
    <svg width={svgMeasure} height={svgMeasure}>
      <circle
        cx={svgMeasure / 2}
        cy={svgMeasure / 2}
        r={radius}
        fill="transparent"
        strokeWidth={3}
        className="stroke-background-border"
      />
      <motion.circle
        cx={svgMeasure / 2}
        cy={svgMeasure / 2}
        r={radius}
        fill="transparent"
        strokeWidth={3}
        className="stroke-primary"
        strokeDasharray={`${circumference}px ${circumference}px`}
        strokeDashoffset={percentage!}
        initial={{ strokeDashoffset: circumference }}
        animate={circleAnimation}
        strokeLinecap={"round"}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        alignmentBaseline="middle"
        dominantBaseline="middle"
        className="fill-primary text-2xl font-semibold"
      >
        {battery}%
      </text>
    </svg>
  );
};
export default CamBattery;
