let players = JSON.parse(http_get('http://127.0.0.1:5000/api/get_activity_data'));
let Anchors = document.getElementsByTagName("a");


function http_get(url) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}


function update_page(url, data) {
    if (window.location.href === url) {
      return
    }
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", url, true);
    xmlHttp.send(JSON.stringify(data));
    xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
          history.pushState(null, null, url);
          window.history.pushState("object or string", "Title", url);
          document.querySelector(".root").innerHTML = xmlHttp.responseText
          if (document.querySelector(".jsScript")) {
            var script = document.createElement('script');
            script.setAttribute('src', document.querySelector(".jsScript").querySelector('script').src);
            document.head.appendChild(script);
          }
        }
    };
}


for (var i = 0; i < Anchors.length ; i++) {
    Anchors[i].addEventListener("click", 
        function (event) {
          event.preventDefault()
          update_page(this.href, null)
        },
    true
    );
}
