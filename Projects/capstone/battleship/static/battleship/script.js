document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#select-user').onsubmit = () => loadcheckboxes()
});

var players = [document.querySelector('#select-users').querySelector('span').innerText, document.querySelector('#select-users').querySelector('#select-players').value]

function loadcheckboxes() {
    var cnt = 0;
    makecheckboxes(cnt)
    return false;
}

function makecheckboxes(index) {
    mapform = document.querySelector('#mapform')
    mapform.innerHTML = `<table><tbody></tbody></table><input type="hidden" value="${players[index]}"><input type="submit" value="Create Map">`;
    var tbody = mapform.querySelector('tbody');
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
    document.querySelector('#player-name').innerText = `Make your map ${players[index]}`
    document.querySelector('#mapform').onsubmit = () => createmap(index)
}

function createmap(index) {
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
    
    pushMap(map, players[index]);
    if (index == 0) {
        makecheckboxes(1)
        document.querySelector('#mapform').onsubmit = () => createmap(1)
    }
    return false;
}
function pushMap(map, player) {
    fetch('/maps/create', {
        method: 'POST',
        body: JSON.stringify({
            "user": player,
            "map": map
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

