import { useState } from "react";
import "./App.css";
import React from "react";
import Cubicles from "./Cubicles/Cubicles";
import ArrowUp from "./assets/arrow_up.png";
import ArrowDown from "./assets/arrow_down.png";

const socket = new WebSocket("ws://localhost:8080");

export default function App() {
  let [page, setPage] = useState(0);
  let pages = [<Cubicles socket={socket} />];

  return (
    <>
      <div className="view">{pages[page]}</div>
      <div className="buttons">
        <img
          id="up"
          src={ArrowUp}
          alt="UP"
          onClick={() => setPage(++page)}
        ></img>
        <img
          id="down"
          src={ArrowDown}
          alt="DOWN"
          onClick={() => setPage(--page)}
        ></img>
      </div>
    </>
  );
}
