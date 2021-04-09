import lxml
import lxml.html as html
from lxml import etree
import requests


def create_xml():
    # Получаем данные html со страницы, указанной в parse;
    parser = etree.HTMLParser(encoding='utf-8')
    parsed_boy = etree.parse('http://localhost:8000/cgi-bin/test_script1.py', parser = parser)

    # С помощью xpath можно получить все дочерние узлы, указанного тега,
    # (// означает, что нужно просто найти такой тег, / - чтобы указать после какого тега располагается нужный),
    # Индексация от 1, чтобы пропустить заголовки;
    list_tr = parsed_boy.xpath('//tr')[1:]

    # Раскомментировать, чтобы посмотреть, как находятся записи в таблице
    # for tr in list_tr:
    #     td = tr.xpath('td/text()')
    #     print(td)

    # Процесс создания xml документа.
    # В данном случае создается главный тег page, который и помещается в основу документа;
    page = etree.Element('Таблица')
    doc = etree.ElementTree(page)

    # Строим древовидную структуру документа.
    # SubElement значит, что этот элемент является дочерним по отношению к указанному,
    # В данном примере page;
    bodyElt = etree.SubElement(page, 'Значения_таблицы')

    # Получив значения во всех tr, можно пройтись по ним и записать в соответствующие
    # переменные. Запись нужна для того, чтобы добавить дочерний узел к values.
    for tr in list_tr:
        v = tr.xpath('td/text()')
        values = etree.SubElement(bodyElt, 'Запись')
        maker = etree.SubElement(values, 'Изготовитель')
        maker.text = v[1]
        type = etree.SubElement(values, 'Тип')
        type.text = v[2]
        name = etree.SubElement(values, 'Название')
        name.text = v[3]
        price = etree.SubElement(values, 'Цена')
        price.text = v[4]
        discount = etree.SubElement(values, 'Скидка')
        discount.text = v[5]
        price_with_discount = etree.SubElement(values, 'Цена_со_скидкой')
        price_with_discount.text = v[6]
        delivery = etree.SubElement(values, 'Доставка')
        delivery.text = v[7]

    # После цикла у нас получилась структура, которую теперь нужно записать в файл.
    # Encoding и decode делаются для того, чтобы корректно передать русские символы.
    # Но decode, вообще говоря, нужен всегда;
    outfile = open('output_table.xml', 'w', encoding='utf-8')
    outfile.write(etree.tostring(doc, encoding='utf-8', xml_declaration=True, pretty_print=True).decode('utf-8'))


create_xml()


print("Content-type: text/html\n")
print('<script>location.href="test_script1.py"</script>')