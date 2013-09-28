var pywars = pywars || {};
pywars.Arena = new function () {
  var CANVAS_ID = 'stage';
  var CANVAS_WITH = 700;
  var CANVAS_HEIGHT = 500;
  var START_POSITION = {
    "1": {x: 250, y: 210},
    "2": {x: 300, y: 210}
  };
  var TICKER_DELAY = 500;
  var players = {};
  var stage;
  var timer = null;
  var step = 0;
  var postpone = ['punching', 'kicking', 'blocking'];
  var postponed = [];
  var $pl1health;
  var $pl2health;

  function initTimer(scenario) {
    if (timer) {
      clearInterval(timer);
      step = 0;
    }

    timer = setInterval(function () {
      step += 1;
      onTick(scenario,step);
      if (step == 14) {
        step = 0
      }
    }, TICKER_DELAY)
  }

  function updateStage(event) {
    stage.update(event);
  }

  function onTick(scenario,step) {
    var currentStep = scenario[step];
    for (var i = 0; i < postponed.length; i++) {
      var action = postponed.shift();
      handleScenarioEvent(action);
      delete action.postponed;
      i -= 1;
    }

    if (currentStep) {
      for (var i = 0; i < currentStep.length; i++) {
        var event = currentStep[i];
        handleScenarioEvent(event)
      }
    }
  }

  function handleScenarioEvent(event) {
    var type = event.type;
    eventHandler[type] && eventHandler[type](event)
  }

  var eventHandler = {
    'frame': function (event) {
      var player = event.player;
      var state = event.state;
      if ($.inArray(state, postpone) != -1 && !event.postponed) {
        event.postponed = true;
        postponed.push(event);
        return;
      }
      players[player].setState(state);
    },
    'health': function (event) {
      $pl1health.css('width', event.player1 + '%');
      $pl2health.css('width', event.player2 + '%');
    }
  };

  this.initStage = function () {
    document.getElementById(CANVAS_ID).width = CANVAS_WITH;
    document.getElementById(CANVAS_ID).height = CANVAS_HEIGHT;
    $pl1health = $('.canvas-container .player-1 .health div');
    $pl2health = $('.canvas-container .player-2 .health div');

    stage = new createjs.Stage(CANVAS_ID);

    createjs.Ticker.setFPS(30);
    createjs.Ticker.useRAF = true;
    createjs.Ticker.addEventListener("tick", updateStage);
  };

  this.addFighter = function (fighter) {
    var fighterAnimation = fighter.getAnimation();
    var player = fighter.order;

    $('.canvas-container .player-' + player + ' .name').text(fighter.playerName);

    fighterAnimation.x = START_POSITION[player].x;
    fighterAnimation.y = START_POSITION[player].y;
    stage.addChild(fighterAnimation);
    players[player] = fighter;
    fighter.setState('waiting');
  };

  this.play = function (scenario) {
    $('.canvas-container').append('<img src="/static/core/assets/fight.gif" class="fight" />');
    setTimeout(function(){
      $('.canvas-container .fight').remove()
    },1000);
    initTimer(scenario);
  };


};
