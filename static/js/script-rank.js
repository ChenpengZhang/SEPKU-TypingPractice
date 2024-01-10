var currentLevel = parseInt(localStorage.getItem('currentLevel')) || 1;
console.log(currentLevel);

$(document).ready(function() {
    $.ajax({
        url: '/get_sorted_Userlist',
        type: 'POST',
        dataType: "json",
        data: { level: currentLevel },
        success: function(response) {
            showRanking(response['data']);
        }
    });
});

const userUl = document.getElementById("user-list");

function showRanking(userList){
    for (var i = 0; i < userList.length; ++i){
        const tr = document.createElement("tr");
        tr.innerHTML = 
        `<th scope="row">${i + 1}</th>
        <td>${userList[i][2]}</td>
        <td>${formatTime(userList[i][0])}</td>
        <td>${userList[i][1] + "%"}</td>`;
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