var Pywars = {};
Pywars.Arena = new function() {
  var CANVAS_ID = 'stage';
  var CANVAS_WITH = 700;
  var CANVAS_HEIGHT = 500;
  var START_POSITION = {
    "1": {x: 200, y: 210},
    "2": {x: 350, y: 210}
  };
  var players = [];
  var stage;

  this.initStage = function() {
    document.getElementById(CANVAS_ID).width = CANVAS_WITH;
    document.getElementById(CANVAS_ID).height = CANVAS_HEIGHT;
    stage = new createjs.Stage(CANVAS_ID);

    createjs.Ticker.setFPS(30);
    createjs.Ticker.useRAF = true;
    createjs.Ticker.addEventListener("tick", tick);
  };

  this.addFighter = function(fighter) {
    var fighterAnimation = fighter.getAnimation();
    fighterAnimation.x = START_POSITION[fighter.order].x;
    fighterAnimation.y = START_POSITION[fighter.order].y;
    stage.addChild(fighterAnimation);
    players.push(fighter);
    fighter.stance()
  };

  function tick(event) {
    stage.update(event);
  }
};
