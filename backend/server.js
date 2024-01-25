/*
  WebSocket Server for connecting python client to frontend/website.
  Sends any recieved message to all connected websocket clients.
  Python Client (Listening to meshtastic messages) -> WebSocket Server (this) -> Frontend/Website
*/

const { WebSocketServer } = require("ws");

const sockserver = new WebSocketServer({ port: 8080 });
const sockets = [];

sockserver.on("connection", (ws) => {
  ws.send("Connection established");
  console.log("New user connected: ", ws);
  sockets.push(ws);

  ws.on("message", (data) => {
    console.log(data.toString());
    sockets.forEach((client) => {
      client.send(data.toString());
    });
  });

  ws.onerror = function () {
    console.log("websocket error");
  };
});
