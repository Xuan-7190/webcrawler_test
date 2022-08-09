$('#combinations_list').change(function () {
    // 取得select option的長度
    var length = $('#combinations_list').val();
    // 取得要加入到的div
    var container = $('#input_number');
    // 每次先清空div
    container.empty();
    // 依照選擇的option增加input text數量
    for(var i=1; i<=length; i++) {
        container.append('<input type="number" name="number' + i + '" value="" min="1" max="39" required />');
    }
})