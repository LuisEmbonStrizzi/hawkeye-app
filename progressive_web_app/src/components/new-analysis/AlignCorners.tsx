import Image from "next/image";
import { motion } from "framer-motion";
import { useState, useRef } from "react";
import clsx from "clsx";

type AlignCornersProps = {
  image: string;
};

const AlignCorners: React.FC<AlignCornersProps> = ({ image }) => {
  const initialVertices = [
    { x: 100, y: 100 },
    { x: 100, y: 200 },
    { x: 200, y: 100 },
    { x: 200, y: 200 },
  ];
  const [vertices, setVertices] = useState(initialVertices);
  const [selectedVertex, setSelectedVertex] = useState({ x: 0, y: 0 });
  const [selectedIndex, setSelectedIndeex] = useState<number>(-1);
  const [magnifyingGlassVisible, setMagnifyingGlassVisible] = useState(false);
  const [[imgWidth, imgHeight], setSize] = useState<number[]>([0, 0]);

  const constraintsRef = useRef(null);
  const imageRef = useRef(null);

  const aVertexRef = useRef(null);
  const bVertexRef = useRef(null);
  const cVertexRef = useRef(null);
  const dVertexRef = useRef(null);

  const vertexRefs = [aVertexRef, bVertexRef, cVertexRef, dVertexRef];

  const handleDrag = (index: number, x: number, y: number) => {
    const proportionWidth =
      imgWidth / constraintsRef.current.getBoundingClientRect().width;
    const proportionHeight =
      imgHeight / constraintsRef.current.getBoundingClientRect().height;
    const parentPos = constraintsRef.current.getBoundingClientRect();

    const X = vertexRefs[index].current.getBoundingClientRect().left + 20;
    const Y = vertexRefs[index].current.getBoundingClientRect().top + 20;

    const XFinal = (X - parentPos.left) * proportionWidth;
    const YFinal = (Y - parentPos.top) * proportionHeight;

    const newVertices = [...vertices];
    newVertices[index] = { x: XFinal, y: YFinal };
    setVertices(newVertices);
    setSelectedVertex({ x: X as number, y: Y as number });
    setSelectedIndeex(index);
  };

  const variants = {
    leftTop: { x: 0, y: 0 },
    rightTop: { x: imgWidth - 128, y: 0 },
    leftBottom: { x: 0, y: imgHeight - 128 },
    rightBottom: { x: imgWidth - 128, y: imgHeight - 128 },
  };

  return (
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-4 p-4">
      <h2 className="flex gap-4 p-4 font-semibold text-foreground-important">
        {vertices.map((vertex, index) => (
          <span
            key={index}
            className={clsx(
              index === selectedIndex && "text-primary",
              "transition-all duration-300 ease-in-out"
            )}
          >
            Vertex {index + 1}: ({Math.round(vertex.x)}, {Math.round(vertex.y)})
          </span>
        ))}
      </h2>
      <section className="relative w-full max-w-4xl" ref={constraintsRef}>
        {magnifyingGlassVisible && (
          <motion.div
            animate={
              (vertices[selectedIndex]?.x > imgWidth/2) &
              (vertices[selectedIndex]?.y > imgHeight/2)
                ? "rightBottom"
                : (vertices[selectedIndex]?.x > imgWidth/2) &
                  (vertices[selectedIndex]?.y < imgHeight/2)
                ? "rightTop"
                : (vertices[selectedIndex]?.x < imgWidth/2) &
                  (vertices[selectedIndex]?.y > imgHeight/2)
                ? "leftBottom"
                : "leftTop"
            }
            variants={variants}
            transition={{ duration: 0.5, type: "tween", ease: "linear" }}
            className="left- absolute z-20 flex h-32 w-32 items-center justify-center overflow-hidden rounded-full border border-background-border bg-background shadow-xl"
            style={{
              backgroundImage: `url('${image}')`,
              backgroundRepeat: "no-repeat",
              backgroundSize: `${imgWidth * 2}px ${imgHeight * 2}px`,
              backgroundPositionX: `${
                -(
                  selectedVertex.x -
                  imageRef.current.getBoundingClientRect().left -
                  window.scrollX
                ) *
                  2 +
                128 / 2
              }px`,
              backgroundPositionY: `${
                -(
                  selectedVertex.y -
                  imageRef.current.getBoundingClientRect().top -
                  window.scrollY
                ) *
                  2 +
                128 / 2
              }px`,
            }}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M11.25 12.75H6.24998C5.83578 12.75 5.5 12.4142 5.5 12V12C5.5 11.5858 5.83578 11.25 6.24998 11.25H11.25V6.25001C11.25 5.83581 11.5858 5.50003 12 5.50003V5.50003C12.4142 5.50003 12.7499 5.83581 12.7499 6.25001V11.25H17.75C18.1642 11.25 18.5 11.5858 18.5 12V12C18.5 12.4142 18.1642 12.75 17.75 12.75H12.7499V17.75C12.7499 18.1642 12.4142 18.5 12 18.5V18.5C11.5858 18.5 11.25 18.1642 11.25 17.75V12.75Z"
                className="fill-background"
              />
            </svg>
          </motion.div>
        )}
        {vertices.map((vertex, index) => (
          <motion.span
            key={index}
            dragConstraints={constraintsRef}
            drag
            ref={vertexRefs[index]}
            dragElastic={0}
            dragMomentum={false}
            whileDrag={{ scale: 1.2 }}
            onDrag={(event, info) =>
              handleDrag(index, info.point.x, info.point.y)
            }
            onDragStart={(event, info) => setMagnifyingGlassVisible(true)}
            onDragEnd={(event, info) => setMagnifyingGlassVisible(false)}
            initial={initialVertices[index]}
            className="absolute z-10 flex h-8 w-8 items-center justify-center rounded-full border border-primary bg-background/60 shadow-sm shadow-primary/50"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M11.25 12.75H6.24998C5.83578 12.75 5.5 12.4142 5.5 12V12C5.5 11.5858 5.83578 11.25 6.24998 11.25H11.25V6.25001C11.25 5.83581 11.5858 5.50003 12 5.50003V5.50003C12.4142 5.50003 12.7499 5.83581 12.7499 6.25001V11.25H17.75C18.1642 11.25 18.5 11.5858 18.5 12V12C18.5 12.4142 18.1642 12.75 17.75 12.75H12.7499V17.75C12.7499 18.1642 12.4142 18.5 12 18.5V18.5C11.5858 18.5 11.25 18.1642 11.25 17.75V12.75Z"
                fill="#4ECB71"
              />
            </svg>
          </motion.span>
        ))}
        <Image
          className="constrast-200 w-full rounded-md border border-background-border hue-rotate-15 "
          ref={imageRef}
          onMouseEnter={(e) => {
            const elem = e.currentTarget;
            const { width, height } = elem.getBoundingClientRect();
            setSize([width, height]);
          }}
          width={1000}
          height={1000}
          quality={100}
          src={image}
          alt="Frame of the camera display"
        />
      </section>
    </div>
  );
};
export default AlignCorners;
