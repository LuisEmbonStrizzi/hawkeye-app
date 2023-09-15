import React, { useRef, useEffect } from "react";
import { SVG } from '@svgdotjs/svg.js'

const EditablePolygon: React.FC = () => {
  const svgRef = useRef(null);
  const points = useRef<number[][]>([
    [100, 100],
    [200, 100],
    [200, 200],
    [100, 200],
  ]);

  useEffect(() => {
    const svgContainer = svgRef.current ? SVG(svgRef.current) : null;
    svgContainer?.clear();

    const polygon = svgContainer.polygon(points);

    const vertices = points.map(([x, y], index) => {
      const vertex = svgContainer.circle(8).center(x, y);

      vertex.draggable().on("dragmove", function (event) {
        const [newX, newY] = [this.cx(), this.cy()];
        points[index] = [newX, newY];
        polygon.plot(points);
      });

      return vertex;
    });

    polygon.fill("transparent").stroke({ width: 2, color: "black" });

    return () => {
      svgContainer.clear();
    };
  }, []);

  return (
    <div className="editable-polygon">
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default EditablePolygon;