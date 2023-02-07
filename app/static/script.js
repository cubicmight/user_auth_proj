function fetchlogs() {
    fetch('/logs')
        .then(response => {
            return response.json();

        })
        .then(moves => {
            document.getElementById("logs").value = moves;

        })
}

function moves(direction, num, user) {
    fetch('/' + direction + '/' + user + '/' + num)
        .then(response => {
            return response.json();

        })
        .then(result => {
            console.log(result);
            fetchlogs();

        })
}



setInterval(fetchlogs, 5000);