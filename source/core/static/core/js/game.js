pywars = window.pywars || {};


pywars.game = {
    stateUrl: '', // will be defined inside template

    init: function() {
        this.field = $('#game-field');
        this.editor = this.field.find('.game-editor textarea');

        this.initEditor();
    },

    initEditor: function() {
        CodeMirror.fromTextArea(this.editor[0], {
            lineNumbers: true,
            theme: 'ambiance',
            width: '100%',
            height: '100%'
        });
    }
};
