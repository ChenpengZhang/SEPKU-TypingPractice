// 全局变量，存储在用户本地，使得用户每次刷新后关卡保持一致
var currentLevel = parseInt(localStorage.getItem('currentLevel')) || 1;

// 使用AJAX请求获取目标文本
// 这个函数会在刷新的时候自动运行，负责获取最初的文本
$(document).ready(function() {
    $.ajax({
        url: '/update_target',
        type: 'POST',
        data: { level: currentLevel },
        success: function(response) {
            updateLevelInfo(response.text);
        }
    });
});

// 发送Ajax请求，获取指定关卡的文字内容
// 这个函数主要用来做关卡切换
function switchLevel(level) {
    $.ajax({
        url: '/update_target',
        type: 'POST',
        data:{ level: level },
        success: function(response) {
        // 更新当前关卡和文字内容
        currentLevel = level;
        localStorage.setItem('currentLevel', currentLevel);
        updateLevelInfo(response.text);
        // 显示文字内容到页面
        },
        error: function(xhr, status, error) {
        console.log('请求失败：', error);
        }
    });
}