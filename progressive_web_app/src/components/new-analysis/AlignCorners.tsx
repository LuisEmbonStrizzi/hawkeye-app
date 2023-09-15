import Image from "next/image";
import { motion } from "framer-motion";
import { useState, useRef } from "react";
import Button from "../Button";
import Link from "next/link";
import axios from "axios";

type AlignCornersProps = {
  image: string | undefined;
  firstOnClick: () => void;
};

const AlignCorners: React.FC<AlignCornersProps> = ({ image, firstOnClick }) => {
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

      const handleCorners = async ()=>{
        //Código para enviar "vertices" state
        const sendCorners = await axios.post("http://20.226.51.27/predict", {
          esquinas: vertices,
          //Ver si lo mando desde videos.ts
        });
        firstOnClick;
      }

  return (
    <div className="mx-auto my-auto flex h-screen w-full flex-col items-center justify-center gap-6 p-6 pt-[63px]">
      <header className="fixed top-0 flex w-full justify-center border-b border-background-border bg-background px-4 py-[10px]">
        <div className="flex w-full items-center justify-between max-w-7xl whitespace-nowrap text-base font-semibold text-foreground-important">
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
            icon={
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9.1665 14.1667H10.8332V9.16666H9.1665V14.1667ZM9.99984 7.49999C10.2359 7.49999 10.4339 7.42013 10.5936 7.26041C10.7533 7.10068 10.8332 6.90277 10.8332 6.66666C10.8332 6.43055 10.7533 6.23263 10.5936 6.07291C10.4339 5.91318 10.2359 5.83332 9.99984 5.83332C9.76373 5.83332 9.56581 5.91318 9.40609 6.07291C9.24637 6.23263 9.1665 6.43055 9.1665 6.66666C9.1665 6.90277 9.24637 7.10068 9.40609 7.26041C9.56581 7.42013 9.76373 7.49999 9.99984 7.49999ZM9.99984 18.3333C8.84706 18.3333 7.76373 18.1146 6.74984 17.6771C5.73595 17.2396 4.854 16.6458 4.104 15.8958C3.354 15.1458 2.76025 14.2639 2.32275 13.25C1.88525 12.2361 1.6665 11.1528 1.6665 9.99999C1.6665 8.84721 1.88525 7.76388 2.32275 6.74999C2.76025 5.7361 3.354 4.85416 4.104 4.10416C4.854 3.35416 5.73595 2.76041 6.74984 2.32291C7.76373 1.88541 8.84706 1.66666 9.99984 1.66666C11.1526 1.66666 12.2359 1.88541 13.2498 2.32291C14.2637 2.76041 15.1457 3.35416 15.8957 4.10416C16.6457 4.85416 17.2394 5.7361 17.6769 6.74999C18.1144 7.76388 18.3332 8.84721 18.3332 9.99999C18.3332 11.1528 18.1144 12.2361 17.6769 13.25C17.2394 14.2639 16.6457 15.1458 15.8957 15.8958C15.1457 16.6458 14.2637 17.2396 13.2498 17.6771C12.2359 18.1146 11.1526 18.3333 9.99984 18.3333ZM9.99984 16.6667C11.8609 16.6667 13.4373 16.0208 14.729 14.7292C16.0207 13.4375 16.6665 11.8611 16.6665 9.99999C16.6665 8.13888 16.0207 6.56249 14.729 5.27082C13.4373 3.97916 11.8609 3.33332 9.99984 3.33332C8.13873 3.33332 6.56234 3.97916 5.27067 5.27082C3.979 6.56249 3.33317 8.13888 3.33317 9.99999C3.33317 11.8611 3.979 13.4375 5.27067 14.7292C6.56234 16.0208 8.13873 16.6667 9.99984 16.6667Z"
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
            onClick={handleCorners}
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