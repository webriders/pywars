$(function () {
  var f1 = new pywars.Fighter('scorpion', 1);
  var f2 = new pywars.Fighter('scorpion', 2);

  pywars.Arena.initStage();
  pywars.Arena.addFighter(f2);
  pywars.Arena.addFighter(f1);

  for (var i in SCENARIO) {
    var round = SCENARIO[i];
    console.log(round)
    pywars.Arena.play($.parseJSON(round['scene']));
  }

  $('#stage').on('scenario.end', function () {
  })
})
