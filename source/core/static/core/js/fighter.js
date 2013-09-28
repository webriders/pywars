Pywars.Fighter = function (name, order) {
  name = name || 'scorpion';
  order = this.order = order || 1;

  var stanceDelta = order == 1 ? 0 : -35;
  var hitDelta =  order == 1 ? 0 : -55;

  var sprites = {
    "images": [
      '/static/core/assets/' + name + '/stance-' + order + '.png',
      '/static/core/assets/' + name + '/punch-' + order + '.png',
      '/static/core/assets/' + name + '/kick-' + order + '.png',
      '/static/core/assets/' + name + '/hit-' + order + '.png',
      '/static/core/assets/' + name + '/a-stance-' + order + '.png',
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
      [0, 0, 73, 129, 4, stanceDelta, 0],[73, 0, 73, 129, 4, stanceDelta, 0],[146, 0, 73, 129, 4, stanceDelta, 0],[219, 0, 73, 129, 4, stanceDelta, 0],[292, 0, 73, 129, 4, stanceDelta, 0],[365, 0, 73, 129, 4, stanceDelta, 0],[438, 0, 73, 129, 4, stanceDelta, 0],[511, 0, 73, 129, 4, stanceDelta, 0],[584, 0, 73, 129, 4, stanceDelta, 0],
    ],
    animations: {
      astance: [31, 39, "punch", 0.4],
      stance: [0, 8, "stance", 0.1],
      punch: [9, 16, "kick", 0.4],
      kick: [17, 26, "hit", 0.4],
      hit: [27, 30, "astance", 0.4]
    }
  };

  var animation = new createjs.BitmapAnimation(new createjs.SpriteSheet(sprites));

  this.play = function () {
    animation.gotoAndPlay("punch");
  };
  this.stance = function () {
    animation.gotoAndPlay("astance");
  };

  this.getAnimation = function() {
    return animation;
  }
};
