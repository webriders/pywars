pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template
    submitCodeUrl: '',

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

    startGame: function() {
        this.joinForm.hide();
        this.gameField.fadeIn();
        this.codeEditor.refresh();
    },

    joinGame: function() {
        var joinUrl = this.joinForm.attr('action'),
            self = this;

        $.post(joinUrl, this.joinForm.serialize(), function() {
            self.startGame();
        });
    },

    renderRound: function(roundNumber) {
    },

    finishGame: function() {

    }
};
