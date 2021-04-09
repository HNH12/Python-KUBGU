#!/usr/bin/env python3
import work_with_sqlLit as sql3

con = sql3.create_connect('mydatabase.db')
rows = sql3.output_table_products(con)

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="../styles.css">
            <title>Добавление новой покупки</title>
        </head>
        <body>
            <form class='form-add' action='processing_new_item.py'>
                <div class='product-list'>
                    <label>Товар</label>
                    <select name='list_product' required> """)

for row in rows:
    print("<option>")
    for field in row:
        print(field,end=' ')
    print("</option>\n")

print("""
                    </select>
                </div>
                <div class='div-discount'>
                    <div class='div-discount-second'>
                        <input class='discount' name='discount-name' type='number' placeholder='0' min='0' max='100'>
                        <label>%</label>
                    </div>
                    <label >Скидка</label>
                </div>
                <div class='checkbox-div'>
                    <input class='checkBox' name='list_address' type='checkbox' onchange='processing_delivery()'>
                    <label for='list_address'>Доставка</label>
                </div>
                <input class='address' name='country' type='text' placeholder='страна'>
                <input class='address' name='city' type='text' placeholder='город'>
                <input class='address' name='street' type='text' placeholder='улица'>
                <input type='submit' value='Добавить'>
            </form>
            
            <script type="text/javascript" src='../first_script.js'></script>
        </body>
        </html>
""")
