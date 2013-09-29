var pywars = pywars || {};
pywars.Arena = new function () {
  var CANVAS_ID = 'stage';
  var START_POSITION = {
    "1": {x: 250, y: 210},
    "2": {x: 300, y: 210}
  };
  var TICKER_DELAY = 900;
  var FPS = 10;
  var players = {};
  var stage;
  var timer = null;
  var step = 0;
  var $pl1health;
  var $pl2health;
  var $canvas;
  var scenarios = [];
  var newGame = true;


  function initTimer() {
    var scenario = scenarios.shift();
    if (timer) {
      clearInterval(timer);
      step = 0;
    }

    timer = setInterval(function () {
      onTick(scenario, step);
      step += 1;

      if (step > scenario.lastTick) {
        step = 0;
        if (scenarios.length > 0) {
          $canvas.trigger('scenario.end');
          scenario = scenarios.shift();
        } else {
          $canvas.trigger('scenarios.end');
          clearInterval(timer);
        }
      }

    }, TICKER_DELAY)
  }

  function updateStage(event) {
    players[1].getAnimation().x = START_POSITION[1].x;
    players[1].getAnimation().y = START_POSITION[1].y;
    players[2].getAnimation().x = START_POSITION[2].x;
    players[2].getAnimation().y = START_POSITION[2].y;
    stage.update(event);
  }

  function onTick(scenario, step) {
    var currentStep = scenario[step];
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
      players[player].setState(state);
    },
    'health': function (event) {
      $pl1health.css('width', event.player1 + '%');
      $pl2health.css('width', event.player2 + '%');
    }
  };

  function showSplash() {
    var fight = createjs.Sound.play("fight");
    fight.volume = 1;
    setTimeout(function () {
      $('.canvas-container').append('<img src="/static/core/assets/fight.gif" class="fight" />');
    }, 300);
    setTimeout(function () {
      $('.canvas-container .fight').remove()
    }, 1300);
    newGame = false;
  }

  function resizeCanvas() {
    var $canvasContainer = $canvas.parents('.game-player');
    var width = $canvasContainer.width();
    var height = $canvasContainer.height();
    $canvas.get(0).width = width;
    $canvas.get(0).height = height;

    START_POSITION = {
      "1": {x: width / 2 - 70, y: height / 2 + 50},
      "2": {x: width / 2 - 40, y: height / 2 + 50}
    };
  }

  this.initStage = function () {
    $canvas = $('#' + CANVAS_ID);
    $pl1health = $('.canvas-container .player-1 .health div');
    $pl2health = $('.canvas-container .player-2 .health div');
    $('.canvas-container .player-container').show();
    resizeCanvas();
    $(window).resize(resizeCanvas)
    stage = new createjs.Stage(CANVAS_ID);
    createjs.Ticker.setFPS(FPS);
    createjs.Ticker.useRAF = true;
    createjs.Ticker.addEventListener("tick", updateStage);

    createjs.Sound.registerSound("/static/core/assets/sounds/fight.wav", "fight");
    createjs.Sound.registerSound("/static/core/assets/sounds/punch.wav", "punch");
    createjs.Sound.registerSound("/static/core/assets/sounds/kick.wav", "kick");
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
    var lastTick = 0;

    for (var i in scenario) {
      if (scenario.hasOwnProperty(i)) {
        lastTick = Math.max(parseInt(i), lastTick);
      }
    }

    scenario.lastTick = lastTick;

    scenarios.push(scenario);

    if (newGame) {
      showSplash();
      setTimeout(function () {
        initTimer();
      }, 1000);
    } else if (!timer) {
      initTimer();
    }
  };


};
