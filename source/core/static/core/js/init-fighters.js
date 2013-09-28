$(function(){
  var f1 = new Pywars.Fighter('scorpion', 1);
  var f2 = new Pywars.Fighter('scorpion', 2);
  Pywars.Arena.initStage();

Pywars.Arena.addFighter(f2);
Pywars.Arena.addFighter(f1);

  setTimeout(function(){
    Pywars.Arena.play(SCENARIO)
  }, 500);

})
