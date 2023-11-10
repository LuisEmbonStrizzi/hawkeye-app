import Image from "next/image";
import { motion } from "framer-motion";
import { useState, useRef } from "react";
import Button from "../Button";
import Link from "next/link";
import { type courtData } from "../navigation/NewAnalysisSteps";

type AlignCornersProps = {
  image: string | undefined;
  firstOnClick: () => void;
  setCourtData: React.Dispatch<React.SetStateAction<courtData | null>>;
};


const AlignCorners: React.FC<AlignCornersProps> = ({
  image,
  firstOnClick,
  setCourtData,
}) => {

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

    const X = vertexRefs[index].current.getBoundingClientRect().left + 19.2;
    const Y = vertexRefs[index].current.getBoundingClientRect().top + 19.2;

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
    rightTop: { x: imgWidth - 192, y: 0 },
    leftBottom: { x: 0, y: imgHeight - 192 },
    rightBottom: { x: imgWidth - 192, y: imgHeight - 192 },
  };

  /*
  
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

  */

  return (
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-6 p-6 pt-[63px]">
      <header className="fixed top-0 flex w-full justify-center border-b border-background-border bg-background px-4 py-[10px]">
        <div className="flex w-full max-w-7xl items-center justify-between whitespace-nowrap text-base font-semibold text-foreground-important">
          <Link href="/home">
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
            />
          </Link>
          Align corners
          <Button
            style="secondary"
            onClick={() => setCourtData(null)}
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
      </header>

      <section className="relative w-full max-w-7xl" ref={constraintsRef}>
        {magnifyingGlassVisible && (
          <motion.div
            animate={
              (vertices[selectedIndex]?.x > imgWidth / 2) &
              (vertices[selectedIndex]?.y > imgHeight / 2)
                ? "rightBottom"
                : (vertices[selectedIndex]?.x > imgWidth / 2) &
                  (vertices[selectedIndex]?.y < imgHeight / 2)
                ? "rightTop"
                : (vertices[selectedIndex]?.x < imgWidth / 2) &
                  (vertices[selectedIndex]?.y > imgHeight / 2)
                ? "leftBottom"
                : "leftTop"
            }
            variants={variants}
            transition={{ duration: 0.5, type: "tween", ease: "linear" }}
            className="left- absolute z-20 flex h-48 w-48 items-center justify-center overflow-hidden rounded-full border border-background-border bg-background shadow-xl"
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
                192 / 2
              }px`,
              backgroundPositionY: `${
                -(
                  selectedVertex.y -
                  imageRef.current.getBoundingClientRect().top -
                  window.scrollY
                ) *
                  2 +
                192 / 2
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
        <div className="flex flex-col pt-6">
          <Button
            style="primary"
            onClick={firstOnClick}
            icon={
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M8 15L6.9375 13.9375L10.875 10L6.9375 6.0625L8 5L13 10L8 15Z"
                  fill="#181B27"
                />
              </svg>
            }
            label="Submit corners"
            padding="both-left"
          />
        </div>
      </section>
    </div>
  );
};
export default AlignCorners;
