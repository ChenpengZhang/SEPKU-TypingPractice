//更新文字部分
function updateTargetText(text) {
    var targetTextElement = document.getElementById('targetText');
    targetTextElement.textContent = text;
}

//用户打字后的一系列反应
function detectInput() {
    highlightMistakes();
    invokeTimer();
}

//错误矫正部分
function highlightMistakes() {
    var inputWords = document.getElementById('inputText').value.split(" ");
    var targetWords = document.getElementById('targetText').textContent.split(" ");
    var highlightedText = "";
    for (var i = 0; i < targetWords.length; i++) {
        if (inputWords[i] == targetWords[i]) {
            highlightedText += "<span style='color: green'>" + targetWords[i] + "</span> "  //如果输入正确那么就显示绿色
        } else if(i >= inputWords.length || inputWords[i] == null) {
            highlightedText += targetWords[i] + " ";  //如果还没输入到这个地方那么显示黑色
        } else {
            var correctPosition = longestSequence(targetWords[i], inputWords[i]);
            var separated = targetWords[i].split("");
            for (var j = 0; j < correctPosition.length; ++j){
                separated[correctPosition[j] - 1] = "<span style='color: green;'>" + separated[correctPosition[j] - 1] + "</span>";
            }
            highlightedText += ("<span style='color: red;'>" + separated.join('') + "</span> ");
            //如果输入到一半，那么没有输入的是红色，输入的是绿色，并且用动态规划的最长相同字串来进行染色
        }
    }
    document.getElementById('targetText').innerHTML = highlightedText;
}

function longestSequence(text1, text2) {
    const m = text1.length, n = text2.length;
    const dp = new Array(m + 1).fill(0).map(() => new Array(n + 1).fill(0));
    let path = [];
    for (let i = 0; i < m + 1; i++) {
        path.push([]);
        for (let j = 0; j < n + 1; j++) {
            path[i].push([]);
        }
    }
    for (let i = 1; i <= m; i++) {
        const c1 = text1[i - 1];
        for (let j = 1; j <= n; j++) {
            const c2 = text2[j - 1];
            if (c1 === c2) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                path[i][j] = path[i - 1][j - 1].slice();
                path[i][j].push(i);
            } else {
                if (dp[i - 1][j] >= dp[i][j - 1]){
                    dp[i][j] = dp[i - 1][j];
                    path[i][j] = path[i - 1][j].slice();
                } else {
                    dp[i][j] = dp[i][j - 1];
                    path[i][j] = path[i][j - 1].slice();
                }
            }
        }
    }
    return path[m][n];
}

//计时部分
var timerStarted = false;
var startTime;

function startTimer() {
    startTime = new Date().getTime();
    timerStarted = true;
}

function updateTimer() {
    if (timerStarted) {
        var currentTime = new Date().getTime();
        var elapsedTime = currentTime - startTime;
        var seconds = Math.floor(elapsedTime / 1000);
        var minutes = Math.floor(seconds / 60);

        // 格式化时间为 mm:ss 的形式
        var formattedTime = ("0" + minutes).slice(-2) + ":" + ("0" + (seconds % 60)).slice(-2);

        document.getElementById("timer").innerText = formattedTime;
  }
}

function invokeTimer() {
    if (!timerStarted) {
        startTimer();
    }
}

setInterval(updateTimer, 1000); // 每秒更新计时器