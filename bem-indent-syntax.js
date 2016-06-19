'use strict';

var stdin = require('get-stdin'),
    bis = require('bem-indent-syntax');

stdin().then(function(textBeforeCaret) {
    try {
        process.stdout.write(bis.stringify(textBeforeCaret));
    } catch(err) {
        console.error(err);
    }
});
