pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template
    submitCodeUrl: '',
    newRoundsUrl: '',
    player1: 'player1',
    player2: 'player2',
    userRole: 'observer',

    init: function() {
        this.isRendering = false;
        this.gameMessage = $("#game-message");
        this.joinForm = $("#join-game-form");
        this.codeForm = $("#code-form");
        this.gameField = $("#game-field");
        this.codeEditorField = $('#code-editor');
        this.codeEditor = this.initCodeEditor();

        this.state = 'waiting';
        this.lastRound = 0;

        this.current_round = 0;
        this.submitted_round = 0;

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
                if (data.status == 'success') {
                    self.disableCodeForm();
                    self.submitted_round = self.lastRound;
                }
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
                            self.finishGame(data.winner); /* finish only after all rendering performed */
                            self.state = data.state;
                        }

                }
            }

            if(data.round != self.submitted_round && self.isRendering == false) {
                console.log(self.isRendering)
                self.enableCodeform();
            }
            if(data.round != self.current_round && data.round !=0 && self.isRendering == false) {
                pywars.messages.info('Round ' + data.round + ' started');
                self.current_round = data.round;
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

        $('#stage').on('scenarios.end', function(){
            self.isRendering = false;
        });
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

    finishGame: function(winner) {
        var self = this;

        this.gameField.addClass('readonly');

        var winnerMessageBlock = this.gameField.find('.game-winner'),
            winnerMessage = winnerMessageBlock.find('.message .placeholder');

        if (winner) {
            if((self.userRole == 'player1' && winner == self.player1) || (self.userRole == 'player2' && winner == self.player2))
                $('.share-message.winner').show();
            else if(self.userRole != 'observer')
                $('.share-message.looser').show();
            else
                $('.share-message.observer').show();

            winnerMessage.text(winnerMessage.text().replace('username', winner));
        }
        else {
            winnerMessage.text("Seems like you both are good enough. Tie!");
            $('.share-message.observer').show();
        }


        winnerMessageBlock.fadeIn(400, function() {
            $(window).trigger('resize');
        });
    },

    disableCodeForm: function() {
        if (this.codeEditor) {
            this.codeEditor.setOption('readOnly', 'nocursor');
            this.codeForm.css('opacity', 0.3);
        }
    },

    enableCodeform: function() {
        if (this.codeEditor) {
            this.codeEditor.setOption('readOnly', false);
            this.codeForm.css('opacity', 1);
        }
    }
};
