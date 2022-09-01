modal = document.querySelector('.modal')
permissions = document.getElementsByClassName('permission')
html_role_list = document.querySelector('.player_list')
selected_role = ''
role_list = {}
http_post('http://127.0.0.1:5000/api/get_roles', {
	'selected_role': 'Да это костыль, и чо',
	'csrf_token': document.querySelector("#csrf_token").value
})


function update_role(permission, act, state) {
	var xmlHttp = new XMLHttpRequest()
	xmlHttp.open("POST", 'http://127.0.0.1:5000/api/update_role', true)
	xmlHttp.setRequestHeader("Content-Type", "application/json")
	xmlHttp.send(JSON.stringify({
		'role': selected_role,
		'permission': permission,
		'act': act,
		'state': state,
		'selected_role': 'Да это костыль, и чо',
		'csrf_token': document.querySelector("#csrf_token").value
	}))
}


function http_post(url, data) {
	var xmlHttp = new XMLHttpRequest()
	xmlHttp.open("POST", url, true)
	xmlHttp.setRequestHeader("Content-Type", "application/json")
	xmlHttp.send(JSON.stringify(data))
	xmlHttp.onreadystatechange = function () {
		if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
			role_list = JSON.parse(xmlHttp.responseText)
			if (!selected_role) {
				for (role in role_list) {
					select_role(role)
					break
				}
			}
		}
	}
}


function update_roles() {
	roles = ''
	for (role in role_list) {
		if (selected_role == role) {
			roles += `<button id="selected_role">${role}</button>`
		} else {
			roles += `<button onclick="select_role('${role}')">${role}</button>` // Здесь же ещё будет кнопка удалить с подтверждением
		}
	}
	roles += `<button onclick="create_role()" style="margin-bottom: 10px">Создать</button>`
	html_role_list.innerHTML = roles
}


function create_role() {
	modal.id = ''
}


function delete_role() {
	if (confirm('Ты уверен что хочешь удалить роль ' + selected_role + '?')) {
		console.log('Да')
	}
}


function select_role(role) {
	selected_role = role
	update_roles(selected_role)
	for (var perm = 0; perm < permissions.length ; perm++) {
		if (role_list[selected_role].includes(permissions[perm].querySelector('input').id)) {
			permissions[perm].querySelector('input').checked = true
		} else {
			permissions[perm].querySelector('input').checked = false
		}
	}
}


for (var i = 0; i < permissions.length ; i++) {
	permissions[i].querySelector('input').addEventListener('change', (event) => {
		update_role(event.srcElement.id, 'update_role', event.target.checked)
	})
}
window.onclick = function(event) {
	if (event.target == modal) {
		modal.id = 'hidden'
	}
}
