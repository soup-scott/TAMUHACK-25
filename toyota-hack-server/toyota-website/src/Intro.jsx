import React, { useState } from "react";
import "./style/Intro.css";
import ToyotaLogo from "./assets/Toyota_logo_Red.svg.png";
import ChatBot from "./ChatBot.jsx";
import GenCars from "./GenCars.jsx";

function Intro() {
  const [showIntro, setShowIntro] = useState(true);
  const [showImage, setShowImage] = useState(false);
  const [showChatbot, setShowChatbot] = useState(false);

  const handleIntroFadeOut = () => {
    setShowIntro(false);
    setTimeout(() => {
      setShowImage(true);
    }, 1000);
  };

  const handleImageFadeOut = () => {
    setShowImage(false);
    setTimeout(() => {
      setShowChatbot(true);
    }, 1000);
  };

  return (
    <div className="app">
      {showIntro && (
        <div className={`intro-message ${!showIntro ? "fade-out" : ""}`}>
          <p>We Heard</p>
          <p>You Were</p>
          <p>Looking For</p>
          <p>Your Dream Car</p>
          <button className="begin-button" onClick={handleIntroFadeOut}> BEGIN </button>
        </div>
      )}
      {showImage && (
        <img
          src={ToyotaLogo}
          alt="Toyota Logo"
          className={`image ${!showImage ? "fade-out" : "fade-in"}`}
          onClick={handleImageFadeOut}
        />
      )}
      {showChatbot && (
        <>
          <ChatBot />
          <GenCars />
        </>
      )}
    </div>
  );
}

export default Intro;