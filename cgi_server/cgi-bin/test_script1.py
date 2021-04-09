#!/usr/bin/env python3
import work_with_sqlLit as sql3


con = sql3.create_connect("mydatabase.db")
rows = sql3.output_full_table(con)


print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="../styles.css">
            <title>Обработка данных форм</title>
        </head>
        <body>""")
print(
    """
    <table class='table-html'>
    <caption>Таблица покупок</caption>
    <tr>
        <th>Номер покупки</th>
        <th>Изготовитель продукта</th>
        <th>Тип продукта</th>
        <th>Название продукта</th>
        <th>Цена (до скидки)</th>
        <th>Скидка</th>
        <th>Цена после скидки</th>
        <th>Адрес доставки</th>
    </tr> 
    """)

for row in rows:
    print("<tr>")
    for i in range(7):
        print("<td>{0}</td>\n".format(row[i]))
    if row[7] == None:
        print("<td>Нет доставки</td>\n")
    else:
        print("<td>{0}, {1}, {2}</td>\n".format(row[7], row[8], row[9]))

    print("</tr>\n")

print("""
    </table>
    
    <div class='main-form'>
        <input value='Добавить новую запись' type='button' onclick='page_add()'>
        <input value='Добавить запись из xml' type='button' onclick='add_from_xml()'>
    </div>
    
    <script>
        function page_add() {
            location.href = 'add_new_script.py' 
        }
        function add_from_xml() {
            location.href = 'add_from_xml.py' 
        }
    </script>
    
    </body>
    </html>
""")

con.close()