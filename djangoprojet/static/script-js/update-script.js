function WriteSelectedItem() {
    selected_item = document.getElementById("select-sale")
    sale_arr  = selected_item[selected_item.options.selectedIndex].value.split('| ');
    inputs = document.getElementsByClassName('product-input');
    for (var i = 1; i < inputs.length; i++) {
        inputs[i-1].value = sale_arr[i];
    }
    address = sale_arr[sale_arr.length-1].split(', ');
    console.log(address[0]);
    if (address[0] != 'Нет доставки') {
        for (var i = 6; i < 9; i++) {
            inputs[i].value = address[i - 6];
        }
    }
    else {
        for (var i = 6; i < 9; i++) {
            inputs[i].value = '';
        }
    }
}

WriteSelectedItem()