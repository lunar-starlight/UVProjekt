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
    let p = data['player'];
    let i = data['i'];
    let j = data['j'];
    let row = data['row'];
    let col = data['col'];
    if (game == gamePK) {
        console.log("receive(" + i + "," + j + ") => " + p);
        fillSquare(p, i, j, row, col)
        player = 3 - p
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
        console.log("send(" + i + "," + j + ") => " + player);
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

fillSquare = function(player, i, j, row, col) {
    console.log("fill");
    cell = document.querySelector('#cell-' + i + '-' + j + '-' + row + '-' + col);
    if (player === 1) {
        cell.innerHTML = icon1;
    } else {
        cell.innerHTML = icon2;
    }
};