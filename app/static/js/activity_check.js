const servers = document.querySelector(".select_server")
const date_1 = document.querySelector(".date_1")
const date_2 = document.querySelector(".date_2")
const memeber_players = document.querySelector(".player_list")
const btn_select_server = document.querySelector(".server_list")
const activity_players = document.querySelector(".activity_list")
let server = ''
let member_list = ''
let player_in_activity = []


const get_players = () => {
	if (typeof players === 'undefined') {
	    const players = JSON.parse(http_get('http://127.0.0.1:5000/api/get_activity_data'))
	    return players
	}
	return players
}


function http_get(url) {
	var xmlHttp = new XMLHttpRequest()
	xmlHttp.open("GET", url, false)
	xmlHttp.send(null)
	return xmlHttp.responseText
}


function http_post(url, data) {
	var xmlHttp = new XMLHttpRequest()
	xmlHttp.open("POST", url, true)
	xmlHttp.setRequestHeader("Content-Type", "application/json")
	xmlHttp.send(JSON.stringify(data))
	xmlHttp.onreadystatechange = function () {
	    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
	    	update_activity_data(JSON.parse(xmlHttp.responseText))
		}
	}
}


const update_activity_data = (local_data) => {
	if (local_data) {
		activity_players.innerHTML = get_player_activity(player_in_activity, local_data)
	} else {
		http_post('http://127.0.0.1:5000/api/get_activity_check', {
			'server': btn_select_server.textContent,
			'players': player_in_activity,
			'date_1': date_1.value,
			'date_2': date_2.value
		})
	}
}


const get_player_activity = function(player_list, local_data) {
	data = {...local_data}
	activity = ''
	for (check_player in player_list) {
		if (!(data.hasOwnProperty(player_list[check_player]))) {
			data[player_list[check_player]] = {
				'local': 0,
				'global': 0,
				'private': 0,
				'warn': 0,
				'mute': 0,
				'kick': 0,
				'ban': 0,
				'avg': '00:00<br>00:00',
				'total': '00:00<br>00:00'
			}
		}
	}
	for (player in player_list) {
		if (Number(player) == 0) {
			activity += '<div class="activity_player" style="border-top: 0">'
		} else if (Number(player) + 1 == player_list.length && player_list.length < 8) {
			activity += '<div class="activity_player" style="border-bottom: 1px solid #888888">'
		} else {
			activity += '<div class="activity_player">'
		}
		if ('avatar' in players['all_players'][player_list[player]] && players['all_players'][player_list[player]]['avatar']) {
			path_image = `http://127.0.0.1:5000/static/css/images/users/${player_list[player]}/avatar.png`
		} else {
			path_image = `https://skins.mcskill.net/?name=${player_list[player]}&mode=5&fx=64&fy=64`
		}
		activity += `
			<button class="player_button" onclick="delete_player('${player_list[player]}')"><div class="player">
				<img src="${path_image}">
				<div class="name" style="color: ${player_list[player], players['all_players'][player_list[player]]['color']}">${player_list[player]}</div>
				<div class="arrow">🡸</div>
			</div></button>
			<div class="local">${{...data}[player_list[player]]['local']}</div>
			<div class="global">${{...data}[player_list[player]]['global']}</div>
			<div class="pm">${{...data}[player_list[player]]['private']}</div>
			<div class="warn">${{...data}[player_list[player]]['warn']}</div>
			<div class="mute">${{...data}[player_list[player]]['mute']}</div>
			<div class="kick">${{...data}[player_list[player]]['kick']}</div>
			<div class="ban">${{...data}[player_list[player]]['ban']}</div>
			<div class="avg">${{...data}[player_list[player]]['avg']}</div>
			<div class="total">${{...data}[player_list[player]]['total']}</div>
		</div>
		`
	}
	return activity
}


const distribution_players = function(player_list) {
	member_list = ''
	server = btn_select_server.textContent
	activity_players.innerHTML = get_player_activity(player_list, {})
	for (player in players['all_players']) {
		if (!player_list.includes(player)) {
			if ('avatar' in players['all_players'][player] && players['all_players'][player]['avatar']) {
				path_image = `http://127.0.0.1:5000/static/css/images/users/${player}/avatar.png`
			} else {
				path_image = `https://skins.mcskill.net/?name=${player}&mode=5&fx=64&fy=64`
			}
			member_list += `
				<button class="player_button" onclick="add_player('${player}')"><div class="player">
				    <img src="${path_image}">
				    <div class="name" style="color: ${players['all_players'][player]['color']}">${player}</div>
				    <div class="arrow">🡺</div>
				</div></button>
			`
		}
	}
	memeber_players.innerHTML = member_list
	update_activity_data()
}


const add_player = function(player) {
	player_in_activity.push(player)
	distribution_players(player_in_activity)
}


const delete_player = function(player) {
	player_in_activity.splice(player_in_activity.indexOf(player), 1)
	distribution_players(player_in_activity)
}


const select_server = function(server) {
	servers.innerHTML = ''
	servers.id = 'hidden'
	btn_select_server.innerHTML = server
	date_1.value = players['servers'][server]['dates'][2]
	date_1.min = players['servers'][server]['dates'][0]
	date_1.max = players['servers'][server]['dates'][1]
	date_2.value = players['servers'][server]['dates'][1]
	date_2.min = players['servers'][server]['dates'][0]
	date_2.max = players['servers'][server]['dates'][1]
	player_in_activity = []
	for (player in players['servers'][server]['staff']) {
		if (players['all_players'][players['servers'][server]['staff'][player]]['view']) {
			player_in_activity.push(players['servers'][server]['staff'][player])
		}
	}
	for (server in players['servers']) {
		if (server != btn_select_server.innerHTML) {
			servers.innerHTML += `<button class="server" onclick="select_server('${server}')">${server}</button>`
		}
	}
	setTimeout(() => servers.id = '', 1)
	distribution_players(player_in_activity)
}


players = get_players()
for (server in players['servers']) {
	servers.innerHTML += `<button class="server" onclick="select_server('${server}')">${server}</button>`
}
select_server('HitechCraft_Titan')
document.querySelector(".date_1").addEventListener('change', (event) => {
  distribution_players(player_in_activity)
})
document.querySelector(".date_2").addEventListener('change', (event) => {
  distribution_players(player_in_activity)
})
