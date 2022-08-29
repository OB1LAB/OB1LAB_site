html_role_list = document.querySelector('.player_list')
role_list = {}
http_post('http://127.0.0.1:5000/api/get_roles', {
    'selected_role': 'test',
    'csrf_token': document.querySelector("#csrf_token").value
})


function http_post(url, data) {
	var xmlHttp = new XMLHttpRequest()
	xmlHttp.open("POST", url, true)
	xmlHttp.setRequestHeader("Content-Type", "application/json")
	xmlHttp.send(JSON.stringify(data))
	xmlHttp.onreadystatechange = function () {
	    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
	    	role_list = JSON.parse(xmlHttp.responseText)
	    	update_roles()
		}
	}
}


function update_roles() {
    roles = ''
    for (role in role_list) {
        roles += `<button onclick="select_role('${role}')">${role}</button>` // Здесь же ещё будет кнопка удалить с подтверждением
    }
    roles += `<button onclick="select_role('Создать')">Создать</button>`
    html_role_list.innerHTML = roles
}


function select_role(role) {
    console.log(role)
}
