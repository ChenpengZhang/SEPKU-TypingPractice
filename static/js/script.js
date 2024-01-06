//更新关卡信息
function updateLevelInfo(text) {
    document.getElementById('inputText').value = '';  //重置输入框
    stopTimer();
    document.getElementById('timer').innerText = '00:00:000';  //重置计时器
    document.getElementById('targetText').textContent = text;  //更新目标文字
    document.getElementById('originalText').textContent = text;  //更新初始的文字，这个文字仅用于计算，不显示
    finish = false;  //刷新关卡状态为未完成
    document.getElementById('result').innerText = '';  //重置结果框
}

//关卡是否结束的判断
var finish = false;

//用户打字后的一系列反应
function detectInput() {
    if (finish) return;  //如果已经过关那么直接返回
    var correctNum = highlightMistakes();
    var correctRate = displayRate(correctNum);
    invokeTimer();
    if (isFinished()){
        var time = stopTimer();
        document.getElementById('result').innerText = 'Complete!';
        sendStats(user_id, time, correctRate, currentLevel);
        finish = true;
    }
}

//计算返回并显示用户正确率
function displayRate(correctNum){
    //显示部分还没写
    var originalWords = document.getElementById('originalText').textContent.split(" ");
    var acc = 100 * correctNum / originalWords.length;
    document.getElementById('accuracy').innerText = acc.toFixed(2) + "%";
    return acc
}

//判断用户是否结束输入部分
function isFinished(){
    var inputWords = document.getElementById('inputText').value.split(" ");
    var originalWords = document.getElementById('originalText').textContent.split(" ");
    var inlen = inputWords.length;
    var orlen = originalWords.length;
    return (inlen == orlen && (inputWords[inlen - 1].length == originalWords[orlen - 1].length)) || inlen > orlen;
    //完成条件是用户输入了和目标文段一样长的文本且最后一个单词打到了和目标一样的长度
    //这样保证了计时的准确性
}

//暗黑模式切换部分
function toggleDarkMode(){
    var styleLight = document.getElementById('style-light');
    var styleDark = document.getElementById('style-dark');

    if (styleDark.disabled) {
        // 切换到暗黑模式
        styleLight.disabled = true;
        styleDark.disabled = false;
        document.getElementById('modeswitch').textContent = "白色模式"
    } else {
        // 切换回浅色模式
        styleLight.disabled = false;
        styleDark.disabled = true;
        document.getElementById('modeswitch').textContent = "暗黑模式"
    }
}


//错误矫正部分
function highlightMistakes() {
    var inputWords = document.getElementById('inputText').value.split(" ");
    var targetWords = document.getElementById('targetText').textContent.split(" ");
    var correctWordNum = 0;
    var highlightedText = "";
    for (var i = 0; i < targetWords.length; i++) {
        if (inputWords[i] == targetWords[i] && inputWords[i] != "") {  //这里加了一个非空判断，因为可能会在末尾分割出一个空字符串
            highlightedText += "<span style='color: green'>" + targetWords[i] + "</span> "  //如果输入正确那么就显示绿色
            correctWordNum += 1;  //并记录正确
        } else if(i >= inputWords.length || inputWords[i] == null) {
            highlightedText += targetWords[i] + " ";  //如果还没输入到这个地方那么显示黑色
        } else {
            var correctPosition = longestSequence(reverseString(targetWords[i]), reverseString(inputWords[i]));  
            //这里是为了避免动态规划总是优先规划到最后一个字符的bug，因此直接将两个字符串都翻转了
            //返回值是（正确的字符位置）的翻转值
            var separated = targetWords[i].split("");
            for (var j = 0; j < correctPosition.length; ++j){
                separated[separated.length - correctPosition[j]] = "<span style='color: green;'>" + separated[separated.length - correctPosition[j]] + "</span>";
            }
            highlightedText += ("<span style='color: red;'>" + separated.join('') + "</span> ");
            //如果输入到一半，那么没有输入的是红色，输入的是绿色，并且用动态规划的最长相同字串来进行染色
        }
    }
    document.getElementById('targetText').innerHTML = highlightedText;
    return correctWordNum;
}

function reverseString(str){
    return str.split("").reverse().join("");
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
        var milliseconds = elapsedTime % 1000;
        var seconds = Math.floor(elapsedTime / 1000);
        var minutes = Math.floor(seconds / 60);

        // 格式化时间为 mm:ss:SSS 的形式
        var formattedTime = ("0" + minutes).slice(-2) + ":" + ("0" + (seconds % 60)).slice(-2) + ":" + ("00" + milliseconds).slice(-3);

        document.getElementById("timer").innerText = formattedTime;
        return elapsedTime;
    }
}

function invokeTimer() {
    if (!timerStarted) {
        startTimer();
    }
}

function stopTimer(){
    var time = updateTimer();
    timerStarted = false;
    return time;
}

setInterval(updateTimer, 7); // 每7毫秒更新计时器