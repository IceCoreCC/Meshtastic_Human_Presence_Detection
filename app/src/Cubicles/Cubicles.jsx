import { useState } from "react";
import "./Cubicles.css";
import React from "react";
import cubicles from "../assets/Cubicles.png";

export default function Cubicles({ socket }) {
  const [charlie, setCharlie] = useState("green");
  const [ekko, setEkko] = useState("green");
  const [bruno, setBruno] = useState("green");
  const [diego, setDiego] = useState("green");

  /* useEffect(() => {
    if (socket) {
      socket.onmessage = function (event) {
        console.log(event.data);
        if (event.data.toString().includes("Charlie")) {
          setCharlie(event.data.toString().includes("detected") ? "red" : "green");
        }
        if (event.data.toString().includes("Ekko")) {
          setEkko(event.data.toString().includes("detected") ? "red" : "green");
        }
        if (event.data.toString().includes("Bruno")) {
          setBruno(event.data.toString().includes("detected") ? "red" : "green");
        }
        if (event.data.toString().includes("Diego")) {
          setDiego(event.data.toString().includes("detected") ? "red" : "green");
        }
    }
  }
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [socket]); */

  return (
    <>
      <img src={cubicles}></img>
      <div className="cubicles">
        <div className="cubicle" style={{ backgroundColor: charlie }}>
          <h1>Charlie</h1>
        </div>
        <div className="cubicle" style={{ backgroundColor: bruno }}>
          <h1>Bruno</h1>
        </div>
        <div className="cubicle" style={{ backgroundColor: ekko }}>
          <h1>Ekko</h1>
        </div>
        <div className="cubicle" style={{ backgroundColor: diego }}>
          <h1>Diego</h1>
        </div>
      </div>
    </>
  );
}
