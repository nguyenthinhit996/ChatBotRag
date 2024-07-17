import React, { useState, useEffect } from "react";
import { Box } from "@mui/material";

const MovingImage = ({
  imageUrl,
  containerWidth = 300,
  containerHeight = 150,
  imageSize = 50,
}) => {
  const [positionX, setPositionX] = useState(0);
  const [isMovingRight, setIsMovingRight] = useState(true);
  const speed = 2; // pixels per frame

  useEffect(() => {
    const moveImage = () => {
      setPositionX((prevX) => {
        let newX;
        if (isMovingRight) {
          newX = prevX + speed;
          if (newX >= containerWidth - imageSize) {
            setIsMovingRight(false);
            return containerWidth - imageSize;
          }
        } else {
          newX = prevX - speed;
          if (newX <= 0) {
            setIsMovingRight(true);
            return 0;
          }
        }
        return newX;
      });
    };

    const intervalId = setInterval(moveImage, 16); // ~60 fps

    return () => clearInterval(intervalId);
  }, [containerWidth, imageSize, isMovingRight]);

  return (
    <Box
      sx={{
        width: containerWidth,
        height: containerHeight,
        // border: "1px solid #ccc",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <Box
        component="img"
        src={imageUrl}
        alt="Moving Image"
        sx={{
          width: imageSize,
          height: imageSize,
          position: "absolute",
          left: positionX,
          top: (containerHeight - imageSize) / 2, // Center vertically
          transition: "left 0.016s linear",
        }}
      />
    </Box>
  );
};

export default MovingImage;
