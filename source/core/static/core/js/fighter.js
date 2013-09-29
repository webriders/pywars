pywars = pywars || {};
pywars.Fighter = function (playerName, order) {
  order = this.order = order || 1;
  this.playerName = playerName || 'Player 1';
  var stanceDelta = order == 1 ? 0 : -35;
  var hitDelta =  order == 1 ? 0 : -55;
  var blockDelta =  order == 1 ? 0 : -50;
  var victoryDelta =  order == 1 ? 20 : -30;
  var fallingDelta =  order == 1 ? [- 20, + 10,+ 40, + 60,+ 90, + 100] : [ 20, - 10,- 40, - 60,- 90, - 100];


  var skin =  order == 1 ? 'scorpion' : 'subzero' ;

  var staticStates = ['waiting'];
  var prevState;

  var sprites = {
    "images": [
      '/static/core/assets/' + skin + '/stance-' + order + '.png',
      '/static/core/assets/' + skin + '/punch-' + order + '.png',
      '/static/core/assets/' + skin + '/kick-' + order + '.png',
      '/static/core/assets/' + skin + '/hit-' + order + '.png',
      '/static/core/assets/' + skin + '/a-stance-' + order + '.png',
      '/static/core/assets/' + skin + '/block-s-' + order + '.png',
      '/static/core/assets/' + skin + '/block-e-' + order + '.png',
      '/static/core/assets/' + skin + '/victory-' + order + '.png',
      '/static/core/assets/' + skin + '/falling-' + order + '.png'
    ],
    frames: [
      // x, y, width, height, imageIndex, regX, regY
      //stance
      [0, 0, 75, 129, 0, stanceDelta, 0],[75, 0, 75, 129, 0,  stanceDelta, 0],[150, 0, 75, 129, 0, stanceDelta, 0],[225, 0, 75, 129, 0, stanceDelta, 0],[300, 0, 75, 129, 0, stanceDelta, 0],[375, 0, 75, 129, 0, stanceDelta, 0],[450, 0, 75, 129, 0, stanceDelta, 0],[525, 0, 75, 129, 0, stanceDelta, 0],[600, 0, 75, 129, 0, stanceDelta, 0],
      //punch
      [0, 0, 108, 130, 1, 0, 0],[108, 0, 108, 130, 1, 0, 0],[216, 0, 108, 130, 1, 0, 0],[324, 0, 108, 130, 1, 0, 0],[432, 0, 108, 130, 1, 0, 0],[540, 0, 108, 130, 1, 0, 0],[648, 0, 108, 130, 1, 0, 0],[756, 0, 108, 130, 1, 0, 0],
      //kick
      [0, 0, 116, 132, 2, 0, 0],[116, 0, 116, 132, 2, 0, 0],[232, 0, 116, 132, 2, 0, 0],[348, 0, 116, 130, 2, 0, 0],[464, 0, 116, 130, 2, 0, 0],[580, 0, 116, 130, 2, 0, 0],[696, 0, 116, 130, 2, 0, 0],[812, 0, 116, 130, 2, 0, 0],[928, 0, 116, 130, 2, 0, 0],[1044, 0, 116, 130, 2, 0, 0],
      //hit
      [0, 0, 57, 127, 3, hitDelta, 0],[57, 0, 57, 127, 3, hitDelta, 0],[114, 0, 57, 127, 3, hitDelta, 0],[171, 0, 57, 127, 3, hitDelta, 0],
      //a-stance
      [0, 0, 73, 129, 4, stanceDelta ,0],[73, 0, 73, 129, 4, stanceDelta, 0],[146, 0, 73, 129, 4, stanceDelta, 0],[219, 0, 73, 129, 4, stanceDelta, 0],[292, 0, 73, 129, 4, stanceDelta, 0],[365, 0, 73, 129, 4, stanceDelta, 0],[438, 0, 73, 129, 4, stanceDelta, 0],[511, 0, 73, 129, 4, stanceDelta, 0],[584, 0, 73, 129, 4, stanceDelta, 0],
      //block-start
      [0, 0, 57, 129, 5, blockDelta ,0],
      [57, 0, 57, 129, 5, blockDelta ,0],
      [114, 0, 57, 129, 5, blockDelta ,0],
      //block-end
      [0, 0, 57, 129, 6, blockDelta ,0],
      [57, 0, 57, 129, 6, blockDelta ,0],

      //victory
      [0,   0, 97, 151, 7, victoryDelta, 20],
      [97,  0, 97, 151, 7, victoryDelta, 20],
      [194, 0, 97, 151, 7, victoryDelta, 20],
      [291, 0, 97, 151, 7, victoryDelta, 20],
      [388, 0, 97, 151, 7, victoryDelta, 20],
      [485, 0, 97, 151, 7, victoryDelta, 20],

      //falling
      [0,   0, 129, 131, 8, fallingDelta[0], 0],
      [129, 0, 129, 131, 8, fallingDelta[1], 0],
      [258, 0, 129, 131, 8, fallingDelta[2], -10],
      [387, 0, 129, 131, 8, fallingDelta[3], -30],
      [516, 0, 129, 131, 8, fallingDelta[4], -80],
      [645, 0, 129, 131, 8, fallingDelta[5], -110],

    ],
    animations: {
      stance: [0, 8, "stance", 1],
      punching: [9, 16, "waiting", 1],
      kicking: [17, 26, "waiting", 1],
      being_hit_by_kick: {
        frames: [31,32,33,34,35,27,28,30,30,30],
        next: "waiting",
        speed: 1
      },
      being_hit_by_punch: {
        frames: [31,32,27,27,32,27],
        next: "waiting",
        speed: 1
      },
      waiting: [31, 39, "waiting", 1],
      blocking: {
        frames: [40,41,42,42,42,42,42],
        next: "blocking_end",
        speed: 1
      },
      blocking_end: [43, 44, "waiting", 1],
      victory: [45, 49, "", 1],
      falling_by_kick: {
        frames: [31,32,33,34,35,27,52,53,54,55,56],
        next: "",
        speed: 1
      },
       falling_by_punch: {
        frames: [31,32,27,27,32,27,52,53,54,55,56],
        next: "",
        speed: 1
      }

    }
  };

  var animation = new createjs.BitmapAnimation(new createjs.SpriteSheet(sprites));

  this.setState = function(state) {
    if ($.inArray(state, staticStates) != -1 && prevState == state) {
      return;
    }

    if (state == 'kicking'){
      var kick = createjs.Sound.play("kick");
      kick.volume = 1;
    } else if (state == 'punching'){
      var punch = createjs.Sound.play("punch");
      punch.volume = 1;
    }

    if (sprites.animations[state]){
      animation.gotoAndPlay(state);
      prevState = state;
    }
  };

  this.getAnimation = function() {
    return animation;
  }
};
