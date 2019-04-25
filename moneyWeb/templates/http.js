function httpGET(url, callback) {
    const http = new XMLHttpRequest();
    http.open("GET", url, true);
    http.onreadystatechange=(e)=>{
        if (http.readyState == 4 && http.status == 200)
            callback(http.responseText);
    }
    http.send();
}

function httpPOST(url, json) {
    const http = new XMLHttpRequest();
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http.send(JSON.stringify(json));
}

function inputToParagraph(msg) {
    document.getElementById("Paragraph").innerHTML = msg;
}

function httpGETparagraph(url) {
    const http = new XMLHttpRequest();
    http.open("GET", url, true);
    http.onreadystatechange=(e)=>{
        if (http.readyState == 4 && http.status == 200)
            document.getElementById("Paragraph").innerHTML = http.responseText;
    }
    http.send();
}