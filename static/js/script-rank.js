$(document).ready(function() {
    $.ajax({
        url: '/get_sorted_Userlist',
        type: 'POST',
        success: function(response) {
            var data = JSON.parse(response.text);
            showRanking(data);
        }
    });
});

const userUl = document.getElementById("user-list");

function showRanking(userList){
    for (var i = 0; i < userList.length; ++i){
        const tr = document.createElement("tr");
        tr.innerHTML = 
        `<th scope="row">${i + 1}</th>
        <td>${userList[i][0]}</td>
        <td>${userList[i][1]}</td>
        <td>100%</td>`;
        userUl.appendChild(tr);
    }
}