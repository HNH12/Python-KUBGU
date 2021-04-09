# import lxml
# import lxml.html as html
# from lxml import etree
# import requests
# import work_with_sqlLit as sql3
#
#
# # Тут поставь везде print, чтобы разобраться, как работает эта функция;
# def get_values_from_xml():
#     doc = etree.parse('new_record_in_table.xml')
#     root = doc.getroot()
#     all_values = list()
#
#     for e in root:
#         values = list()
#         for r in e:
#             values.append(r.text)
#         all_values.append(values)
#
#     return(all_values)
#
#
# # Добавление записи в базу данных;
# def add_record(values):
#     con = sql3.create_connect('mydatabase.db')
#     for value in values:
#         addresses = value[6].split(', ')
#         sql3.add_record_table_sales(con, value[0], value[1], value[2], float(value[3]), float(value[4]),
#                                     addresses[0], addresses[1], addresses[2])
#
#
# add_record(get_values_from_xml())
#
#
# print("Content-type: text/html\n")
# print('<script>location.href="test_script1.py"</script>')

a = [1,2,3]

print("arr^ {0}".format(a))