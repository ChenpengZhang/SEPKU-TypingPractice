//更新关卡信息
function updateLevelInfo(text_start, text_end) {
    editor.value = text_start;  //更新起始文字
    hidden.value = text_start;  //同步更新隐藏的不带光标的文本数据
    document.getElementById('targetText').textContent = text_end;  //更新目标文字
    finish = false;  //刷新关卡状态为未完成
    document.getElementById('result').innerText = '';  //重置结果框
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


var cursorPos = 0;  //光标位置
var insertMode = false;  //是否处于输入状态
var editor = document.getElementById('editor');  //文本指针（会闪烁）
var hidden = document.getElementById('hiddenText'); //隐藏文本指针，隐藏文本是不带光标的文本
var isHidden = false;
var steps = 0;


document.addEventListener('keydown', function(event) {
    if (insertMode){  //如果是处于输入模式那么就按顺序输入
        if (event.key == "Escape"){
            quitInsertMode();
            steps++;
        }else if ((event.keyCode >= 65 && event.keyCode <= 90) || // 大写字母 A-Z
                (event.keyCode >= 97 && event.keyCode <= 122) || // 小写字母 a-z
                (event.keyCode >= 48 && event.keyCode <= 57) || // 数字 0-9
                (event.keyCode === 32)){
            hidden.textContent = insertStr(hidden.textContent, event.key, cursorPos);
            console.log(hidden.textContent);
            underCursor = event.key;
            steps++;
        }
    }
    else{  //其他情况下就按照这些字母本身的规则运动
        switch (event.key) {
            case "h":
                moveCursorLeft();
                break;
            case "j":
                // moveCursorDown();
                break;
            case "k":
                // moveCursorUp();
                break;
            case "l":
                moveCursorRight();
                break;
            case "i":
                toInsertMode();
                break;
            default:
                break;
        };
        steps++;
    }
    updateSteps();
});

function moveCursorLeft(){
    if (cursorPos > 0){
        cursorPos--;
    }
}

function moveCursorRight(){
    if (cursorPos < editor.textContent.length){
        cursorPos++;
    }
}

function replaceStr(str, char, pos) {
    if (pos < 0 || pos >= str.length) {
      // 如果指定位置超出字符串的范围，则返回原始字符串
      return str;
    }
    // 将字符串转换为字符数组
    let chars = str.split('');
    // 在指定位置替换字符
    chars[pos] = char;
    // 将字符数组转换回字符串
    return chars.join('');
}

function insertStr(str, char, pos) {
    // 检查传递的参数是否有效
    if (pos < 0 || pos >= str.length) {
      return str; // 如果指定位置无效，则返回原始字符串
    }
    // 将字符串分成两个部分，并插入指定字符
    let left = str.substring(0, pos);
    let right = str.substring(pos);
    return left + char + right;
  }

function toInsertMode(){
    insertMode = true;
    document.getElementById("mode").textContent = "--insert--";
    console.log(insertMode);
}

function quitInsertMode(){
    insertMode = false;
    document.getElementById("mode").textContent = "----";
}

function updateSteps(){
    document.getElementById("steps").textContent = steps.toString() + " steps";
}

function flicker(){
    if (isHidden){
        editor.textContent = hidden.textContent;
    }else {
        editor.textContent = replaceStr(hidden.textContent, "_", cursorPos);
    }
    isHidden = !isHidden;
}

setInterval(flicker, 500);