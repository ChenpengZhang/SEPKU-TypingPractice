// 使用AJAX请求获取目标文本
$(document).ready(function() {
    $.ajax({
        url: '/update_target',
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            if (response.status === 'success') {
                updateTargetText(response.text);
            }
        }
    });
});