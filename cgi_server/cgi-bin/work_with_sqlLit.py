import sqlite3


def create_connect(option):
    try:
        con = sqlite3.connect(option)
        return con
    except:
        print('Неверный формат')


def output_full_table(con):
    cursor = con.cursor()
    cursor.execute(
        "SELECT s.id, p.maker, p.type, p.name,p.price,s.discount, s.price, a.country, a.city, a.street "
        "FROM sales as s "
        "JOIN products as p ON s.id_product = p.id "
        "LEFT OUTER JOIN addresses as a ON s.id_address = a.id "
    )
    rows = cursor.fetchall()
    return rows


def create_table_sales(con):
    con.execute("CREATE TABLE IF NOT EXISTS sales (id integer PRIMARY KEY NOT NULL,"
                "id_product integer, id_address integer, discount REAL, price REAL,"
                "FOREIGN KEY(id_product) REFERENCES products(id), "
                "FOREIGN KEY(id_address) REFERENCES address(id))")
    con.commit()


def add_record_table_sales(con, maker, type, name, price, discount=0, country=None, city=None, street=None):
    full_product = True
    full_address = True if (country is not None and city is not None and street is not None) else False

    id_product = None
    id_address = None

    cursor = con.cursor()
    cursor.execute(
        "SELECT id FROM products WHERE maker = ? AND type = ? AND name = ? AND price = ?",
        [maker, type, name, price]
    )
    product = cursor.fetchall()
    if len(product) == 0:
        full_product = False
    else:
        id_product = product[0][0]
    cursor.close()

    if full_address:
        add_record_table_addresses(con, country, city, street)
        cursor = con.cursor()
        cursor.execute(
            "SELECT id FROM addresses WHERE country = ? AND city = ? AND street = ?",
            [country, city, street]
        )
        address = cursor.fetchall()
        id_address = address[0][0]
        cursor.close()

    if full_product:
        con.execute(
            "INSERT INTO sales(id_product,id_address,discount,price) " 
            "VALUES (?,?,?,?)",
            [id_product, id_address, discount, price - price*discount*0.01]
        )
        con.commit()


def delete_record_table_sales(con, user_id):
    con.execute(
        "DELETE FROM sales WHERE id = ?",
        [user_id]
    )
    con.commit()


def update_record_table_sales(con, *args):
    con.execute(
        "UPDATE addresses SET country = ?, city = ?, street = ? "
        "WHERE id = (SELECT id_address FROM sales WHERE id = ?)",
        args
    )
    con.commit()


def output_table_sales(con):
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM sales"
    )
    rows = cursor.fetchall()
    return rows


def create_table_products(con):
    con.execute("CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY NOT NULL,"
                "maker TEXT, type TEXT, name TEXT, price REAL)")
    con.commit()


def add_record_table_products(con, *args):
    con.execute(
        "INSERT INTO products(maker,type,name,price)" 
        "SELECT ?,?,?,?" 
        "WHERE NOT EXISTS"
        "(SELECT 1 FROM products WHERE maker = ? AND type = ? "
        "AND name = ? AND price = ?)",
        args + args)
    con.commit()


def output_table_products(con):
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM products"
    )
    rows = cursor.fetchall()
    return rows


def create_table_addresses(con):
    con.execute("CREATE TABLE IF NOT EXISTS addresses (id integer PRIMARY KEY NOT NULL,"
                "country TEXT, city TEXT, street TEXT)")
    con.commit()


def add_record_table_addresses(con, *args):
    con.execute(
        "INSERT INTO addresses(country,city,street)"
        "SELECT ?,?,?"
        "WHERE NOT EXISTS"
        "(SELECT 1 FROM addresses WHERE country = ? AND city = ? "
        "AND street = ?)",
        args + args)
    con.commit()


def output_table_addresses(con):
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM addresses"
    )
    rows = cursor.fetchall()
    return rows


def main():
    con = create_connect('mydatabase.db')
    print('1. Вывести таблицу\n2. Внести данные в таблицу\n3. Изменить данные в таблице\n0. Выход\n')
    answer = input('Введите ответ: ')
    while(answer != '0'):
        if answer == '1':
            rows = output_full_table(con)
            for row in rows:
                print(*row)
            print()
        elif answer == '2':
            print('\nВведите даные:')
            maker = input('    Производитель: ')
            type = input('    Тип: ')
            name = input('    Название: ')
            price = float(input('    Цена: '))
            discount = input('    Скидка: ')
            ans_del = input('    С доставкой? (1/0): ')
            if (ans_del == '1'):
                country = input('        Введите страну: ')
                city = input('        Введите город: ')
                street = input('        Введите улицу: ')
                add_record_table_sales(con, maker, type, name, price, float(discount), country, city, street)
            else:
                add_record_table_sales(con, maker, type, name, price, float(discount))
            print()
        elif answer == '3':
            id = input('    Введите id: ')
            country = input('    Страна: ')
            city = input('    Город: ')
            street = input('    Улица: ')
            update_record_table_sales(con, country, city, street, id)

        print('1. Вывести таблицу\n2. Внести данные в таблицу\n3. Изменить данные в таблице\n0. Выход\n')
        answer = input('Введите ответ: ')
    con.close()


if __name__ == '__main__':
    main()