$(document).ready(function () {
    $.ajax({
        url: '/get_practice_record',
        type: 'POST',
        dataType: "json",
        data: { user_id: user_id, level_id: -1},
        success: function (response) {
            showRanking(response['data']);
        }
    });
});

const userUl = document.getElementById("user-list");

function showRanking(recordList) {
    for (var i = 0; i < recordList.length; ++i) {
        const tr = document.createElement("tr");
        const date = new Date(recordList[i][2])
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        tr.innerHTML =
            `<th scope="row">${recordList[i][0]}</th>
        <td>${formatTime(recordList[i][1])}</td>
        <td>${year}.${month}.${day}--${hours}:${minutes}</td>
        <td>${recordList[i][3] + "%"}</td>`;
        userUl.appendChild(tr);
    }
}


function formatTime(milliseconds) {
    var totalSeconds = Math.floor(milliseconds / 1000);
    var minutes = Math.floor(totalSeconds / 60);
    var seconds = totalSeconds % 60;
    var milliseconds = milliseconds % 1000;

    return padZero(minutes) + ':' +
        padZero(seconds) + '.' +
        padThreeZeroes(milliseconds);
}

function padZero(num) {
    return ('00' + num).slice(-2);
}

function padThreeZeroes(num) {
    return ('000' + num).slice(-3);
}