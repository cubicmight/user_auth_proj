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
    let steps = document.getElementById("steps").value;
    console.log("number of steps is " + steps);
    fetch('/' + direction + '/' + user + '/' + steps)
        .then(response => {
            return response.json();

        })
        .then(result => {
            console.log(result);
            fetchlogs();

        })
}





setInterval(fetchlogs, 5000);