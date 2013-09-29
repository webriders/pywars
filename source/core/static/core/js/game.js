pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template
    submitCodeUrl: '',
    newRoundsUrl: '',
    player1: 'player1',
    player2: 'player2',

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
        self.updateState();

        this.joinForm.submit(function(e) {
            e.preventDefault();
            self.joinGame();
        });

        this.codeForm.submit(function(e) {
            e.preventDefault();
            self.disableCodeForm();
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
            self.player1 = data.player1_name;
            self.player2 = data.player2_name;

            self.renderCode(data.current_code);

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
        var f1 = new pywars.Fighter(this.player1, 1);
        var f2 = new pywars.Fighter(this.player2, 2);

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
            pywars.Arena.play($.parseJSON(round['scene']));

        });
    },

    finishGame: function() {
        alert('game is finished');
    },

    renderCode: function(code) {
        var self = this;

        if(code == null)
            self.enableCodeform();
        else {
            self.codeEditor.setValue(code);
            self.disableCodeForm();
        }
    },

    disableCodeForm: function() {
        var self = this;

        self.codeEditor.setOption('readOnly', 'nocursor');
        self.codeForm.css('opacity', 0.3);
    },

    enableCodeform: function() {
        var self = this;

        self.codeEditor.setOption('readOnly', false);
        self.codeForm.css('opacity', 1);
    }
};
