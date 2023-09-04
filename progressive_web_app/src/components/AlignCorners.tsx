import { motion } from "framer-motion";
import Image from "next/image";
import { useState, useRef } from "react";

type AlignCornersProps = {
  image: string;
};

const AlignCorners: React.FC<AlignCornersProps> = ({ image }) => {
  const initialVertices = [
    { x: 100, y: 100 },
    { x: 200, y: 100 },
    { x: 200, y: 200 },
    { x: 100, y: 200 },
  ];

  const [vertices, setVertices] = useState(initialVertices);

  const constraintsRef = useRef(null);

  const handleDrag = (index: number, x: number, y: number) => {
    const newVertices = [...vertices];
    newVertices[index] = { x, y };
    setVertices(newVertices);
  };

  const points = vertices.map((vertex) => `${vertex.x},${vertex.y}`).join(" ");

  return (
    <section ref={constraintsRef} className="relative p-4">
      {vertices.map((vertex, index) => (
        <motion.span
          key={index}
          dragConstraints={constraintsRef}
          drag
          whileDrag={{ scale: 1.2 }}
          onDrag={(event, info) =>
            handleDrag(index, info.point.x, info.point.y)
          }
          style={{
            left: `${vertex.x}px`,
            top: `${vertex.y}px`,
          }}
          className="absolute h-4 w-4 rounded-full border-2 border-primary bg-primary/50 z-10"
        ></motion.span>
      ))}
      <svg className="absolute" width="100%" height="100%">
        <polygon
          points={points}
          fill="transparent"
          stroke="black"
          strokeWidth="2"
        />
      </svg>
      <Image
        className="constrast-200"
        width={1000}
        height={1000}
        quality={100}
        src={image}
        alt="Frame of the camera display"
      />
    </section>
  );
};
export default AlignCorners;

/*
  const mapField = useRef(null);
  const mapFieldContainer = useRef(null);

  const aCorner = useRef(null);
  const bCorner = useRef(null);
  const cCorner = useRef(null);
  const dCorner = useRef(null);

  const setFinalCorners = () => {
    let parentPos = mapField.current.getBoundingClientRect();

    let aCornerPos = aCorner.current.getBoundingClientRect();
    let bCornerPos = bCorner.current.getBoundingClientRect();
    let cCornerPos = cCorner.current.getBoundingClientRect();
    let dCornerPos = dCorner.current.getBoundingClientRect();

    let relativePos = { A: {}, B: {}, C: {}, D: {} };

    const proportionWidth = mapField.current.videoWidth / parentPos.width;
    const proportionHeight = mapField.current.videoHeight / parentPos.height;

    relativePos.A.x = (aCornerPos.left - parentPos.left) * proportionWidth;
    relativePos.B.x = (bCornerPos.left - parentPos.left) * proportionWidth;
    relativePos.C.x = (cCornerPos.left - parentPos.left) * proportionWidth;
    relativePos.D.x = (dCornerPos.left - parentPos.left) * proportionWidth;

    relativePos.A.y = (aCornerPos.top - parentPos.top) * proportionHeight;
    relativePos.B.y = (bCornerPos.top - parentPos.top) * proportionHeight;
    relativePos.C.y = (cCornerPos.top - parentPos.top) * proportionHeight;
    relativePos.D.y = (dCornerPos.top - parentPos.top) * proportionHeight;

    console.log(relativePos);
    setCorners(JSON.stringify(relativePos));
    //return relativePos;
  };

  <motion.div className="court-map-field" ref={mapFieldContainer}>
                  <motion.div
                    drag
                    whileTap={{ cursor: "grabbing" }}
                    whileDrag={{ scale: 1.5 }}
                    className="corner"
                    dragConstraints={mapFieldContainer}
                    dragMomentum={false}
                    style={{
                      zIndex: 100,
                      backgroundColor: "rgba(0, 0, 0, 0.5)",
                    }}
                  >
                    <div className="center">+</div>
                    <div className="refPoint" ref={aCorner}></div>
                  </motion.div>
                  <motion.div
                    drag
                    whileTap={{ cursor: "grabbing" }}
                    whileDrag={{ scale: 1.5 }}
                    className="corner"
                    dragConstraints={mapFieldContainer}
                    dragMomentum={false}
                    style={{
                      zIndex: 100,
                      backgroundColor: "rgba(0, 0, 0, 0.5)",
                    }}
                  >
                    <div className="center">+</div>
                    <div className="refPoint" ref={bCorner}></div>
                  </motion.div>
                  <motion.div
                    drag
                    whileTap={{ cursor: "grabbing" }}
                    whileDrag={{ scale: 1.33 }}
                    className="corner"
                    dragConstraints={mapFieldContainer}
                    dragMomentum={false}
                    style={{
                      zIndex: 100,
                      backgroundColor: "rgba(0, 0, 0, 0.5)",
                    }}
                  >
                    <div className="center">+</div>
                    <div className="refPoint" ref={cCorner}></div>
                  </motion.div>
                  <motion.div
                    drag
                    whileTap={{ cursor: "grabbing" }}
                    whileDrag={{ scale: 1.33 }}
                    className="corner"
                    dragConstraints={mapFieldContainer}
                    dragMomentum={false}
                    style={{
                      zIndex: 100,
                      backgroundColor: "rgba(0, 0, 0, 0.5)",
                    }}
                  >
                    <div className="center">+</div>
                    <div className="refPoint" ref={dCorner}></div>
                  </motion.div>
                  <video
                    src={currentVideo}
                    ref={mapField}
                    height="100%"
                    onClick={() => {
                      console.log(mapField.current.videoHeight);
                      console.log(mapField.current.videoWidth);
                    }}
                  />
                </motion.div>

  */
