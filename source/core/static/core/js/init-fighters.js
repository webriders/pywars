
function initFighters() {
  var f1 = new Pywars.Fighter('scorpion', 1);
  var f2 = new Pywars.Fighter('scorpion', 2);
  Pywars.Arena.initStage();
  setTimeout(function(){
    Pywars.Arena.addFighter(f1);
  }, 500);
  Pywars.Arena.addFighter(f2);
}