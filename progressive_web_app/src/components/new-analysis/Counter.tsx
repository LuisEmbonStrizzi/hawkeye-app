import { useState, useEffect } from "react";

const Counter: React.FC = () => {
  const [seconds, setSeconds] = useState(0);
  const [minutes, setMinutes] = useState(0);
  const [hours, setHours] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((seconds) => seconds + 1);

      if (seconds === 59) {
        setSeconds(0);
        setMinutes((minutes) => minutes + 1);

        if (minutes === 59) {
          setMinutes(0);
          setHours((hours) => hours + 1);
        }
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [minutes, seconds, hours]);

  const formatTime = (value: number) => {
    return value.toString().padStart(2, "0");
  };

  return (
    <div>
      <h1 className="text-5xl font-semibold text-foreground-important">
        {formatTime(hours)}:{formatTime(minutes)}:{formatTime(seconds)}
      </h1>
    </div>
  );
};
export default Counter;
