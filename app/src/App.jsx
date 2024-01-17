import { useState } from "react";
import "./App.css";
import React from "react";
import Cubicles from "./Cubicles/Cubicles";
import ArrowUp from "./assets/arrow_up.png";
import ArrowDown from "./assets/arrow_down.png";
import Header from "./assets/hhn.png";

const socket = new WebSocket("ws://localhost:8080");

export default function App() {
  let [page, setPage] = useState(0);
  let pages = [<Cubicles socket={socket} />];

  return (
    <>
      <div className="header">
        <img id="header" src={Header} alt="Header"></img>{" "}
      </div>
      <div className="view">{pages[page]}</div>
      <div className="buttons">
        <img
          id="up"
          src={ArrowUp}
          alt="UP"
          onClick={() => {
            if (page < pages.length - 1) setPage(++page);
          }}
        ></img>
        <img
          id="down"
          src={ArrowDown}
          alt="DOWN"
          onClick={() => {
            if (page > 0) setPage(--page);
          }}
        ></img>
      </div>
    </>
  );
}
