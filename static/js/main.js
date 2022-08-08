const players = JSON.parse(http_get('https://ob1lab.xyz/api/getPlayers'));
const servers_dates = JSON.parse(http_get('https://ob1lab.xyz/api/getServersDates'));
const junior_staff = JSON.parse(http_get('https://ob1lab.xyz/api/getJuniorStaff'));
const view_player_list = document.querySelector(".get_players")
const suggBox = document.querySelector(".autocom_box");
const source = document.getElementById("source");
const server_select = document.querySelector(".server_list");
const server_selected = document.querySelector(".server_selected");
const date1 = document.querySelector(".date1").querySelector('input');
const date2 = document.querySelector(".date2").querySelector('input');
const result = document.querySelector(".output_data")
const view_activity_players = document.querySelector(".view_activity_players")
let view_servers = true
let scanning = false
let searched_players = []
let view_player_in_list = []
let set_table = ''


function http_get(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function http_post(url, data) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("POST", url, true);
	xmlHttp.send(JSON.stringify(data));
	xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
	      view_activity(JSON.parse(xmlHttp.responseText));
	    }
	};
}


const view_activity = function(data) {
	scanning = false;
	set_table = '<tr><td>Ник</td><td>Локал</td><td>Глобал</td><td>Личка</td><td>Варн</td><td>Мут</td><td>Кик</td><td>Бан</td><td>Средний онлайн (Ваниш)</td><td>Общий онлайн (Ваниш)</td></tr>'
	for (player in data) {
		set_table += '<tr><td>'+data[player]['show_nick']+'</td><td>'+data[player]['local']+'</td><td>'+data[player]['global']+'</td><td>'+data[player]['private']+'</td><td>'+data[player]['warn']+'</td><td>'+data[player]['mute']+'</td><td>'+data[player]['kick']+'</td><td>'+data[player]['ban']+'</td><td>'+data[player]['average_online_time']+'</td><td>'+data[player]['online_time']+'</td></tr>'
	}
	result.id = "active";
	view_activity_players.innerHTML = set_table;
}


const get_activity = function(data) {
	if (!scanning) {
		scanning = true;
		result.id = "deactive";
		view_activity_players.innerHTML = '';
		http_post('https://ob1lab.xyz/api/getActivity', {
			'server': server_selected.value,
			'players': view_player_in_list,
			'date1': date1.value,
			'date2': date2.value
		})	
	}
}


const close_table = function() {
	result.id = "deactive";
	view_activity_players.innerHTML = '';
}


const view_players = function(players_output) {
	var view = ''
	for (var player in players_output) {
		view += '<div class="player"><div class="avatar" style="background-image: url(https://skins.mcskill.net/?name='+players_output[player]+'&amp;mode=5&amp;fx=43&amp;fy=43);"></div><div class="name"><div class="staff" id='+players[players_output[player]]+'>'+players_output[player]+'</div></div><button onclick=delete_player("'+players_output[player]+'") class="staff">×</button></div>';
	}
	view_player_list.innerHTML = view;
}


const delete_player = function(player) {
	view_player_in_list.splice(view_player_in_list.indexOf(player), 1);
	searched_players.push(player);
	input_handler();
	view_players(view_player_in_list);
}


const add_player = function(player) {
	view_player_in_list.push(player);
	searched_players.splice(searched_players.indexOf(player), 1);
	input_handler();
	view_players(view_player_in_list);
	view_player_list.scrollTo(0, 999999);
}


const view_sugg = function(is_view, players_output=null) {
	if(is_view && typeof(is_view)=='boolean'){
		suggBox.innerHTML = players_output;
		suggBox.id = "active";
 	} else{
		suggBox.innerHTML = '';
		suggBox.id = "deactive";
	}
}


const select_server = function() {
	if (view_servers){
		server_select.id = "active";
		view_servers = false;
	}else {
		server_select.id = "deactive";
		view_servers = true;
	}
}


const padTo2Digits = function(num) {
  return num.toString().padStart(2, '0');
}

const formatDate = function(date) {
  return [
  	date.getFullYear(),
  	padTo2Digits(date.getMonth() + 1),
    padTo2Digits(date.getDate())
  ].join('-');
}


function getMonday(d) {
  d = new Date(new Date());
  var day = d.getDay(),
      diff = d.getDate() - day + (day == 0 ? -6:1);
  return new Date(d.setDate(diff));
}


const select_server_value = function(server) {
	var now = new Date()
	var first_day = formatDate(getMonday())
	server_selected.innerHTML = server;
	server_selected.value = server;
	date1.min = servers_dates[server][0]
	date1.max = servers_dates[server][servers_dates[server].length-1]
	date2.min = servers_dates[server][0]
	date2.max = servers_dates[server][servers_dates[server].length-1]
	if (servers_dates[server].includes(first_day)) {
		date1.value = first_day
	}else {
		date1.value = servers_dates[server][0]
	}
	date2.value = servers_dates[server][servers_dates[server].length-1]
	view_servers = false;
  select_server();
  view_player_in_list = [...junior_staff[server]]
  view_players(view_player_in_list);
}


const view_searched_players = function() {
	var players_output = ''
	for (var player in searched_players) {
		players_output += '<button class="player" onclick="add_player(\''+searched_players[player]+'\')"><div class="avatar" style="background-image: url(https://skins.mcskill.net/?name='+searched_players[player]+'&amp;mode=5&amp;fx=43&amp;fy=43);"></div><div class="name"><div class="staff" id='+players[searched_players[player]]+'>'+searched_players[player]+'</div></div></button>';
	}
	if (players_output){
		view_sugg(true, players_output);
	}else{
		view_sugg(false);
	}
}


const input_handler = function() {
	searched_players = []
	view_servers = false;
	select_server();
	if (source.value){
		var count = 0
		for (var player in players) {
			if(player.toLowerCase().includes(source.value.toLowerCase()) && !view_player_in_list.includes(player)){
				searched_players.push(player)
				count += 1;
				if (count == 10){
					break;
				}
			}
		}
		view_searched_players()
	}else{
		view_sugg(false)
	}
}


source.addEventListener("focus", input_handler);
source.addEventListener("input", input_handler);
source.addEventListener("propertychange", input_handler);
window.addEventListener('click', function(e){
  if (!document.querySelector('.select_server').contains(e.target)) {
	view_servers = false;
	select_server();
  }
  if (!document.querySelector('.search_list').contains(e.target) && !['staff', 'player'].includes(e.target.className)){
    view_sugg(false);
    source.value = '';
  }else if (source.value){
  	document.querySelector('.search_input').focus();
  }else {
  }
});


select_server_value(server_selected.value)
