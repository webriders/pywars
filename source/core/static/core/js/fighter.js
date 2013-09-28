pywars = pywars || {};
pywars.Fighter = function (playerName, order) {
  order = this.order = order || 1;
  this.playerName = playerName || 'Player 1';
  var skin =  'scorpion';
  var stanceDelta = order == 1 ? 0 : -35;
  var hitDelta =  order == 1 ? 0 : -55;

  var staticStates = ['waiting', 'blocking'];
  var prevState;

  var sprites = {
    "images": [
      '/static/core/assets/' + skin + '/stance-' + order + '.png',
      '/static/core/assets/' + skin + '/punch-' + order + '.png',
      '/static/core/assets/' + skin + '/kick-' + order + '.png',
      '/static/core/assets/' + skin + '/hit-' + order + '.png',
      '/static/core/assets/' + skin + '/a-stance-' + order + '.png',
      '/static/core/assets/' + skin + '/block-s-' + order + '.png',
      '/static/core/assets/' + skin + '/block-e-' + order + '.png'
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
      [0, 0, 57, 129, 5, stanceDelta ,0],[57, 0, 57, 129, 5, stanceDelta ,0],[114, 0, 57, 129, 5, stanceDelta ,0],
      //block-end
      [0, 0, 57, 129, 6, stanceDelta ,0],[57, 0, 57, 129, 6, stanceDelta ,0]
    ],
    animations: {
      stance: [0, 8, "stance", 0.1],
      punching: [9, 16, "waiting", 0.4],
      kicking: [17, 26, "waiting", 0.5],
      being_hit: {
        frames: [27,28,29,30,30,30,29,28],
        next: "waiting",
        speed: 0.4
      },
      waiting: [31, 39, "waiting", 0.4],
      blocking: {
        frames: [40,41,42,42,42,42,42,42],
        next: "blocking_end",
        speed: 0.4
      },
      blocking_end: [43, 44, "waiting", 0.4]
    }
  };

  var animation = new createjs.BitmapAnimation(new createjs.SpriteSheet(sprites));

  this.setState = function(state) {
    if ($.inArray(state, staticStates) != -1 && prevState == state) {
      return;
    }

    if (animation.currentAnimation == 'blocking') {
      animation.gotoAndPlay('blocking_end');
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
