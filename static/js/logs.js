const logs = document.getElementById("logs");


function http_get(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}


function update() {
    logs.innerHTML = http_get(window.location.href.replace('parser', 'html'));
    window.scrollTo(0, document.body.scrollHeight);
}


setInterval((update), 1000);
