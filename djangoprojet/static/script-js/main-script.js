function processing_delivery(e) {
    var ch = document.getElementsByClassName('checkBox')[0];
    if (ch.checked) {
        var fields = document.getElementsByClassName('address');
        for (field of fields) {
            field.style.opacity = "1";
            field.disabled = 0;
            field.required = 1;
        }
    }
    else {
        var fields = document.getElementsByClassName('address');
        for (field of fields) {
            field.value = '';
            field.style.opacity = "0";
            field.disabled = 1;
            field.required = 0;
        }
    }
}