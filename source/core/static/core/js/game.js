pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template
    submitCodeUrl: '',
    newRoundsUrl: '',

    init: function() {
        this.joinForm = $("#join-game-form");
        this.codeForm = $("#code-form");
        this.gameField = $("#game-field");
        this.codeEditorField = $('#code-editor');
        this.codeEditor = this.initCodeEditor();

        this.state = 'waiting';
        this.lastRound = 0;

        var self = this;
        setInterval(function() { self.updateState() }, 3 * 1000);

        this.joinForm.submit(function(e) {
            e.preventDefault();
            self.joinGame();
        });

        this.codeForm.submit(function(e) {
            e.preventDefault();
            var code = self.codeEditor.getValue();

            $.post(self.submitCodeUrl, $(this).serialize(), function(data) {
                console.log(data);
            });
        });
    },

    initCodeEditor: function() {
        return CodeMirror.fromTextArea(this.codeEditorField[0], {
            lineNumbers: true,
            theme: 'ambiance'
        });
    },

    updateState: function() {
        var self = this;

        $.get(this.stateUrl, function(data) {
            if (data.state != self.state) {
                switch (data.state) {
                    case 'round':
                        self.startGame();
                        break;
                    case 'finished':
                        self.finishGame();
                }
            }

            if (data.state == 'round' && self.lastRound != data.round) {
                self.renderRound(data.round);
            }

            self.state = data.state;
        });
    },

    initArena: function() {
        var f1 = new pywars.Fighter('scorpion', 1);
        var f2 = new pywars.Fighter('scorpion', 2);

        pywars.Arena.initStage();

        pywars.Arena.addFighter(f2);
        pywars.Arena.addFighter(f1);
    },

    startGame: function() {
        this.joinForm.hide();
        this.gameField.fadeIn();
        this.codeEditor.refresh();
        this.initArena();
    },

    joinGame: function() {
        var joinUrl = this.joinForm.attr('action'),
            self = this;

        $.post(joinUrl, this.joinForm.serialize(), function() {
            self.startGame();
        });
    },

    renderRound: function(roundNumber) {
        var self = this;

        var url = this.newRoundsUrl.replace('0', this.lastRound.toString());
        self.lastRound = roundNumber;

        $.get(url, {}, function(data) {

                var round = data[0];
                console.log(round)
                pywars.Arena.play($.parseJSON(round['scene']));

        });
    },

    finishGame: function() {

    }
};
