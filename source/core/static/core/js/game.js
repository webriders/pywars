pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template
    submitCodeUrl: '',
    newRoundsUrl: '',
    player1: 'player1',
    player2: 'player2',
    userRole: 'observer',

    init: function() {
        if (this.userRole == 'observer')
            return;

        this.isRendering = false;
        this.gameMessage = $("#game-message");
        this.joinForm = $("#join-game-form");
        this.codeForm = $("#code-form");
        this.gameField = $("#game-field");
        this.codeEditorField = $('#code-editor');
        this.codeEditor = this.initCodeEditor();

        this.state = 'waiting';
        this.lastRound = 0;

        var self = this;

        this.initArena();
        this.updateState();
        setInterval(function() { self.updateState() }, 3 * 1000);

        this.joinForm.submit(function(e) {
            e.preventDefault();
            self.joinGame();
        });

        this.codeForm.submit(function(e) {
            e.preventDefault();

            $.post(self.submitCodeUrl, $(this).serialize(), function(data) {
                self.disableCodeForm();
                self.submitted_round = self.lastRound;
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
            self.player1 = data.players[0]
            self.player2 = data.players[1];

            if(data.round != self.submitted_round)
                self.enableCodeform();

            if (self.lastRound != data.round) {
                self.renderRound(data.round);
            }

            if (data.state != self.state) {
                switch (data.state) {
                    case 'round':
                        self.startGame();
                        self.state = data.state;
                        break;
                    case 'finished':
                        if(self.isRendering == false) {
                            self.finishGame(); /* finish only after all rendering performed */
                            self.state = data.state;
                        }

                }
            }
        });
    },

    initArena: function() {
        var self = this;

        var f1 = new pywars.Fighter(this.player1, 1);
        var f2 = new pywars.Fighter(this.player2, 2);

        pywars.Arena.initStage();

        pywars.Arena.addFighter(f2);
        pywars.Arena.addFighter(f1);

        $('#stage').on('scenarios.end', function(){ self.isRendering = false; });
    },

    startGame: function() {
        this.gameMessage.hide();
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

        var url = this.newRoundsUrl.replace('/0/', '/'+this.lastRound.toString()+'/');
        self.lastRound = roundNumber;
        self.isRendering = true;

        $.get(url, {}, function(data) {
            for(var i in data) {
                var round = data[i];
                pywars.Arena.play($.parseJSON(round['scene']));
            }
        });
    },

    finishGame: function() {
        alert('game is finished');
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
