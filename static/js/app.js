let gameSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/game/' + gamePK + '/');

gameSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    if (reload || data['reload']) {
        location.reload();
        return;
    }
    let game = data['game'];
    player = data['player'];
    let i = data['i'];
    let j = data['j'];
    let row = data['row'];
    let col = data['col'];
    if (game == gamePK) {
        console.log("receive(" + i + "," + j + "," + row + "," + col + ") => " + player);
        console.log(data['s'])
        if (data['game_type'] === 'cf') {
            row = data['s'][2];
        } else if (data['game_type'] === 'uttt') {
            enabled_games = document.querySelectorAll('.enabled-game');
            for (let game of enabled_games) {
                game.className = "ttt-game-board";
                for (let row of game.children) {
                    for (let anchor of row.children) {
                        anchor.className = "no-link";
                    }
                }
            }
            if (data['ai']) {
                next_game = document.querySelector('#game-' + data['s'][0] + '-' + data['s'][1]);
            } else {
                next_game = document.querySelector('#game-' + i + '-' + j);
            }
            next_game.className = next_game.className + ' enabled-game';
            for (let row of next_game.children) {
                for (let anchor of row.children) {
                    anchor.className = "ttt-link";
                }
            }
        }
        fillSquare(player, i, j, row, col)
        player = 3 - player
        if (data['ai']) {
            if (data['game_type'] === 'ttt') {
                fillSquare(player, data['s'][0], data['s'][1])
            } else if (data['game_type'] === 'uttt') {
                fillSquare(player, data['s'][0], data['s'][1], data['s'][2], data['s'][3])
            } else if (data['game_type'] === 'cf') {
                fillSquare(player, '', '', data['s'][0], data['s'][1])
            }
            player = 3 - player
        }
    }
};

gameSocket.onclose = function(e) {
    console.error('Game socket closed unexpectedly');
    // location.reload()
};

sendToSocket = function(i='', j='', row='', col='') {
    console.log('#cell-' + i + '-' + j + '-' + row + '-' + col)
    if (document.querySelector('#cell-' + i + '-' + j + '-' + row + '-' + col)
        .parentNode.className != 'no-link') {
        console.log("send(" + i + "," + j + "," + row + "," + col + ") => " + player);
        gameSocket.send(JSON.stringify({
            'game': gamePK,
            'player': player,
            'i': i,
            'j': j,
            'row': row,
            'col': col,
        }));
    }
};

fillSquare = function(player, i='', j='', row='', col='') {
    console.log("fill(" + i + "," + j + "," + row + "," + col + ") => " + player);
    cell = document.querySelector('#cell-' + i + '-' + j + '-' + row + '-' + col);
    if (player === 1) {
        cell.innerHTML = icon1;
    } else {
        cell.innerHTML = icon2;
    }
};