document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#select-user')){
        document.querySelector('#select-user').onsubmit = () => {
            loadcheckboxes();
            return false;
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

function loadcheckboxes(cnt=0, 
        players=[
            document.querySelector('#select-users').querySelector('span').innerText, 
            document.querySelector('#select-users').querySelector('#select-players').value], 
        mapform = document.querySelector('#mapform'), submit_val="Create Map", push=true) {
    makecheckboxes(players[cnt], mapform, submit_val);
    document.querySelector('#player-name').innerText = `Make your map ${players[cnt]}`;
    document.querySelector('#mapform').onsubmit = () => createmap(index = cnt, push);
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
var match_id;
function createmap(index=0, push=true, players=[document.querySelector('#select-users').querySelector('span').innerText, document.querySelector('#select-users').querySelector('#select-players').value]) {
    map = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ];
    const coordinates = getCords();
    coordinates.forEach(coordinate=>{
        const row = coordinate['row'];
        const column = coordinate['column'];
        map[row][column] = 1;
    })    
    if (push==true) {
        if (index == 0) result = pushMap(map=map, players=players, index=index)
        else if (index == 1) result = pushMap(map=map, players=players, index=index, match_id=match_id) 
        result.then(res=>{
            match_id = res
            if (index == 0) {
            loadcheckboxes(cnt=1)
            } else if (index == 1) {
                location.href = `play?match=${match_id}`
            }
        })
    } else {
        return map
    }
    return false;
}

async function pushMap(map, players, index, match_id=false) {
    var response;
    if (match_id){
        response = await fetch(`/matches/create/${match_id}`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                "player": players[index],
                "map": map,
            })
        });
    } else {
        response = await fetch(`/matches/create`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                "player": players[index],
                "map": map,
            })
        });
    }
    const result_1 = await response.json();
    return result_1["match_id"];
}
function get_params() {
    const params = new URLSearchParams(window.location.search);
    var game = params.get('match')
    return {"match_id":game}
}

function main(){
    spans = document.querySelectorAll('span');
    const players = [spans.querySelector('#p1'), spans.querySelector('#p2')]
}

function game(match_id, player, type="Unknown") {
    var map;
    var { coordinate, position } = getCords();
    const row = coordinate['row']
    const column = coordinate['column']
    fetch(`/matches/${match_id}/${player}`).then(response=>response.json()).then(data=>{
        map = data["opponentMap"];
        turns = data["turns"];
        hits = data["hits"];
        if (hits < 4){
            if (map[row][column]) {
                map[row][column] = 0;
                updatePlayerData(data, turns=data["turns"]+1, hits=data["hits"]+1, map=map, type=type)
                label.innerText = 'HIT!!';
                position.style.backgroundColor =  'green'; 
            } else {
                label.innerText = 'MISS';
                position.style.backgroundColor = 'red';
            }
            position.disable=true;
        }
    })
}

function getCords() {
    const tds = document.querySelectorAll('td');
    inps = [];
    var coordinates = [];
    tds.forEach(td => { inps.push(td.querySelector('input')); });
    ipns.forEach(inp => {
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

function updatePlayerData(data, turns=data["turns"], hits=data["hits"], map=data["opponentMap"], type=data["Unknown"]) {
    var new_data;
    fetch(`/matches/${data["match"]}/${data["user"]}`, {
        method: "PUT",
        headers: { 'X-CSRFToken': csrftoken },
        body: JSON.stringify({
            "turns": turns,
            "opponentMap": map,
            "hits":hits,
            "type":type
        })
    })
    .then(response => response.json())
    .then(x => {new_data=x})
    return new_data;
}
