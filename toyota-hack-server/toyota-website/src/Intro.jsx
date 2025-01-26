import React, { useState } from "react";
import "./style/Intro.css";
import ToyotaLogo from "./assets/Toyota_logo_Red.svg.png";

function Intro() {
  const [showIntro, setShowIntro] = useState(true); // Controls the intro message visibility
  const [showImage, setShowImage] = useState(false); // Controls the image visibility

  const handleIntroFadeOut = () => {
    setShowIntro(false); // Trigger the fade-out for the intro message
    setTimeout(() => {
      setShowImage(true); // Show the image after the intro fades out
    }, 1000); // Match the fade-out duration
  };

  const handleImageFadeOut = () => {
    setShowImage(false); // Trigger fade-out for the image
  };

  return (
    <div className="app">
      {showIntro && (
        <div
          className={`intro-message ${!showIntro ? "fade-out" : ""}`}
          onClick={handleIntroFadeOut}
        >
          <p>We Heard</p>
          <p>You Were</p>
          <p>Looking For</p>
          <p>Your Dream Car</p>
        </div>
      )}
      {showImage && (
        <img
          src={ToyotaLogo} // Use the imported image
          alt="Toyota Logo"
          className={`image ${!showImage ? "fade-out" : "fade-in"}`}
          onClick={handleImageFadeOut}
        />
      )}
    </div>
  );
}

export default Intro;