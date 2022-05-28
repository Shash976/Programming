document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#select-user')){
    document.querySelector('#select-user').onsubmit = () => {
        loadcheckboxes();
        return false;
    }
});
users = [document.querySelector('#select-users').querySelector('span').innerText, document.querySelector('#select-users').querySelector('#select-players').value];
function loadcheckboxes(cnt=0, players=users, mapform = document.querySelector('#mapform'), submit_val="Create Map") {
    makecheckboxes(players[cnt], mapform, submit_val);
    document.querySelector('#player-name').innerText = `Make your map ${players[cnt]}`;
    document.querySelector('#mapform').onsubmit = () => createmap(index = cnt);
}

function makecheckboxes(player, mapform, submit_val) {
    mapform.innerHTML =
    `<table id="maptable">
        <tbody></tbody>
    </table>
    <input type="hidden" name="player" id="player" value="${player}">
    <input type="submit" value="${submit_val}">`;
    table = mapform.querySelector('#maptable');
    table.innerHTML = '<tbody></tbody>';
    var tbody = table.querySelector('tbody');
    const maximum = 4;
    for (var row = 0; row < maximum; row++) {
        tbody.innerHTML += `<tr id="${row}"></tr>`;
    }
    trs = tbody.querySelectorAll('tr');
    trs.forEach(tr => {
        for (var col = 0; col < maximum; col++) {
            tr.innerHTML += `<td id=${col}><input type="checkbox" name="R${tr.id} C${col}" id="R${tr.id}C${col}" value=1></td>`;
        }
    });
}
maps = []
function createmap(index=0, push=true, players=users) {
    map = [];
    tds = document.querySelectorAll('td');
    const inps = [];
    var coordinates = [];
    const maximum = 4;
    for (var r = 0; r < maximum; r++) {
        row = [];
        for (var c = 0; c < maximum; c++) {
            row.push(0);
        }
        map.push(row);
    }
    tds.forEach(td => {
        var inp = td.querySelector('input');
        if (inp.checked) {
            inps.push(inp);
        }
    });
    inps.forEach(ship => {
        var column = ship.parentElement.id;
        var row = ship.parentElement.parentElement.id;
        var coordinate = { "row": row, "column": column };
        coordinates.push(coordinate);
        map[coordinate["row"]][coordinate["column"]] = 1;
    });
    maps.push(JSON.stringify(map))    
    if (push==true) {
        pushMap(map, players[index]);
        if (index == 0) {
            loadcheckboxes(cnt=1)
            document.querySelector('#mapform').onsubmit = () => createmap(index=1)
        } else if (index == 1) {
            location.href = `play?p1=${players[0]}&p1m=${maps[0]}&p2=${players[1]}&p2m=${maps[1]}`
        }
    }    
    return false;
}
function pushMap(map, player) {
    fetch('/maps/create', {
        method: 'POST',
        body: JSON.stringify({
            "player": player,
            "map": map,
            "index": users.indexOf(player)
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}
function play_game(map, player) {
    
}