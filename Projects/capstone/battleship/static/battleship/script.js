document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#select-user')) {
        document.querySelector('#select-user').onsubmit = (event) => {
            event.preventDefault();
            loadcheckboxes(cnt=0);
        }
    }
    if(document.querySelector('#players-names')){
        const playerF = document.querySelector('#players-names')
        playerF.onsubmit = (event) => {
            event.preventDefault();
            var players = [playerF.querySelector('#p1').value, playerF.querySelector('#p2').value]
            var mainform = document.querySelector('div#attackdiv').querySelector('form')
            var res = loadcheckboxes(cnt=0, players=players, mapform=mainform, submit_val="SHOOT!", push=false, heading="Attack")
            console.log(res)
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
        var columns = '';
        for (var col=0; col<maximum; col++){
            columns += `<td id=${col}><input type="checkbox" name="R${row} C${col}" id="R${row}C${col}" value=1></td>`;
        }
        tbody.innerHTML += `<tr id="${row}">${columns}</tr>`;
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

function getCords() {
    const tds = document.querySelctor('table').querySelectorAll('td');
    inps = [];
    var coordinates = [];
    tds.forEach(td => { inps.push(td.querySelector('input')); });
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

function play_game(map) {
    tds = document.querySelectorAll('td')
    inps = []
    var coordinate = {};
    var position;
    tds.forEach(td=>{inps.push(td.querySelector('input'))})
    ipns.forEach(inp=>{
        if (inp.checked){
            coordinate['column']=inp.parentElement.id;
            coordinate['row']=inp.parentElement.parentElement.id;
            position = inp;
            }
            position.disable=true;
        })
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
