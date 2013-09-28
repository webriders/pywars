pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template

    init: function() {
        this.state = 'waiting';

        var self = this;
        setInterval(function() { self.updateState() }, 3 * 1000);
    },

    updateState: function() {
        var self = this;

        $.get(this.stateUrl, function(data) {
            if (self.state == 'waiting' && data.state == 'round')
                self.startGame();
            else if (self.state == 'round' && data.state == 'finish')
                self.finishGame();
            else
                self.renderRound(data.roundNumber);

            self.state = data.state;
        });
    },

    startGame: function() {
        console.log("Start game....");
    },

    renderRound: function(roundNumber) {

    },

    finishGame: function() {

    }
};
