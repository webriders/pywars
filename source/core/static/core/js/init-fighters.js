$(function(){
  var f1 = new pywars.Fighter('scorpion', 1);
  var f2 = new pywars.Fighter('scorpion', 2);
  pywars.Arena.initStage();

  pywars.Arena.addFighter(f2);
  pywars.Arena.addFighter(f1);

  setTimeout(function(){
    pywars.Arena.play(jQuery.extend({},SCENARIO))



  }, 1000);

  setTimeout(function(){
    pywars.Arena.play(jQuery.extend({},SCENARIO))
}, 7000);

  $('#stage').on('scenario.end', function(){
  })
})
