planes-on-a-snake
=================

planes on a snake


Add snake to game
function SNAKE_GO() { curl -X PUT -d "{\"player_url\":\"http://planes-on-a-snake.herokuapp.com/\"}" http://snakewithus-server.herokuapp.com/game.addplayerurl/$1 -H "Content-Type:application/json"; }
