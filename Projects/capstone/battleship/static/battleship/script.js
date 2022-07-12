document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#select-user')) {
        document.querySelector('#select-user').onsubmit = (event) => {
            event.preventDefault();
            loadcheckboxes(cnt = 0);
        }
    }
    if (document.querySelector('#players-names')) {
        const playerF = document.querySelector('#players-names')
        playerF.onsubmit = (event) => {
            event.preventDefault();
            var players = [playerF.querySelector('#p1').value, playerF.querySelector('#p2').value]
            var mainform = document.querySelector('div#attackdiv').querySelector('form')
            loadcheckboxes(cnt = 0, players = players, mapform = mainform, submit_val = "SHOOT!", push = false, heading = "Attack")
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
var match_id;

function loadcheckboxes(cnt = 0, players = false, mapform = false, submit_val = "Create Map", push = true, heading = false) {
    if (!players) players = [document.querySelector('#select-users').querySelector('span').innerText, document.querySelector('#select-users').querySelector('#select-players').value];
    if (!mapform) mapform = document.querySelector('#mapform')
    var player = players[cnt];
    var index = cnt;
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
        var columns = '';
        for (var col = 0; col < maximum; col++) {
            columns += `<td id=${col}><input type="checkbox" name="R${row} C${col}" id="R${row}C${col}" value=1></td>`;
        }
        tbody.innerHTML += `<tr id="${row}">${columns}</tr>`;
    }
    if (!heading) document.querySelector('#player-name').innerText = `Make your map ${players[cnt]}`;
    else document.querySelector('#player-name').innerText = `${heading} ${players.slice(cnt - 1)[0]}`
    mapform.onsubmit = (event) => {
        event.preventDefault();
        map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ];
        var coordinates = getCords();
        coordinates.forEach(coordinate => {
            const row = coordinate['row'];
            const column = coordinate['column'];
            map[row][column] = 1;
        })
        if (push) {
            console.log(true)
            if (index == 0) result = pushMap(map = map, players = players, index = index)
            else if (index == 1) result = pushMap(map = map, players = players, index = index, match_id = match_id)
            result.then(res => {
                match_id = res
                if (index == 0) {
                    loadcheckboxes(cnt = 1)
                } else if (index == 1) {
                    location.href = `play?match=${match_id}`
                }
            })
        } else {
            console.log(false);
            const label = document.querySelector('#label');
            const hits_label = document.querySelector('#hits');
            const turns_label = document.querySelector('#turns');
            var row = coordinates[0]['row']
            var column = coordinates[0]['column']
            var position = coordinates[0]['position']
            const match_id = parseInt(get_params('match'));
            fetch(`/matches/${match_id}/${player}`)
                .then(response => response.json())
                .then(data => {
                    var map = data['opponentMap'];
                    var turns = data['turns'];
                    var hits = data['hits'];
                        if (map[row][column] == 1) {
                            map[row][column] = 0;
                            label.innerText = 'HIT!!';
                            position.parentElement.style.backgroundColor = 'green';
                            hits += 1;
                            hits_label.innerText = `${hits} Hits`;
                        } else {
                            label.innerText = 'MISS';
                            position.parentElement.style.backgroundColor = 'red';
                        }
                        turns += 1;
                        turns_label.innerText = `${turns} Turns`;
                        
                        position.checked = false;
                        position.disabled = true;
                    updatePlayerData(data = data, hits = hits, turns = turns, map = map)
                    if (hits==4 && cnt==0) loadcheckboxes(cnt=1, players=players,mapform=mapform, submit_val = "SHOOT!", push = false, heading = "Attack")
                    else if (hits == 4 && cnt == 1) location.href = `/gameover?match=${match_id}`
                })
        }
    };
}

function play_game(match_id, player) {
    var coordinate = getCords();
    var row = coordinate[0]['row'];
    var column = coordinate[0]['column'];
    const label = document.querySelector('#label');
    const hits_label = document.querySelector('#hits');
    const turns_label = document.querySelector('#turns');
    var position = coordinate[0]['position']
    fetch(`/matches/${match_id}/${player}`)
        .then(response => response.json())
        .then(data => {
            var map = data['opponentMap'];
            var turns = data['turns'];
            var hits = data['hits'];
            if (map[row][column] == 1) {
                map[row][column] = 0;
                label.innerText = 'HIT!!';
                position.parentElement.style.backgroundColor = 'green';
                hits += 1;
                hits_label.innerText = `${hits} Hits`;
            } else {
                label.innerText = 'MISS';
                position.parentElement.style.backgroundColor = 'red';
            }
            turns += 1;
            turns_label.innerText = `${turns} Turns`;
            updatePlayerData(data = data, hits = hits, turns = turns, map = map)
            position.checked = false;
            position.disabled = true;
        })
    return hits;
}

async function pushMap(map, players, index, match_id = false) {
    var response;
    if (match_id) {
        response = await fetch(`/matches/create/${match_id}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                "player": players[index],
                "map": map,
            })
        });
    } else {
        response = await fetch(`/matches/create`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                "player": players[index],
                "map": map,
            })
        });
    }
    const result_1 = await response.json();
    return result_1["match_id"];
}

function getCords() {
    const tds = document.querySelector('table').querySelectorAll('td');
    inps = [];
    tds.forEach(td => { inps.push(td.querySelector('input')); });
    var coordinates = [];
    inps.forEach(inp => {
        if (inp.checked) {
            var coordinate = {};
            coordinate['column'] = inp.parentElement.id;
            coordinate['row'] = inp.parentElement.parentElement.id;
            coordinate['position'] = inp;
            coordinates.push(coordinate);
        }
    });
    return coordinates;
}



function updatePlayerData(data, hits = data['hits'], turns = data['turns'], map = data['opponentMap'], type = data['type']) {
    var newData;
    fetch(`/matches/${data['match']}/${data['user']}`, {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrftoken },
        body: JSON.stringify({
            "opponentMap": map,
            "type": type,
            "turns": turns,
            "hits": hits
        })
    })
        .then(response => response.json())
        .then(x => { newData = x })
}

function get_params(parameter) {
    const params = new URLSearchParams(window.location.search);
    var val = params.get(parameter)
    return val;
}