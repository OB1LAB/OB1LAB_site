let players = JSON.parse(http_get('http://127.0.0.1:5000/api/get_activity_data'))


function http_get(url) {
  var xmlHttp = new XMLHttpRequest()
  xmlHttp.open("GET", url, false)
  xmlHttp.send(null)
  return xmlHttp.responseText
}


function update_page(url) {
    var xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", url, true)
    xmlHttp.send(null)
    xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
          document.querySelector(".root").innerHTML = xmlHttp.responseText
          document.title = document.querySelector(".title").innerHTML
          if (document.querySelector(".jsScript")) {
            var script = document.createElement('script')
            script.setAttribute('src', document.querySelector(".jsScript").querySelector('script').src)
            document.head.appendChild(script)
          }
          update_href()
        }
    }
}


function on_href(event) {
    event.preventDefault()
    if (window.location.href != this.href) {
        history.pushState(null, null, this.href)
        update_page(this.href)
    }
}


function update_href() {
    let Anchors = document.getElementsByTagName("a")
    for (var i = 0; i < Anchors.length ; i++) {
        Anchors[i].addEventListener("click", on_href, false)
    }
}


update_href()
window.onpopstate = function(event) {
    update_page(window.location.href)
}
