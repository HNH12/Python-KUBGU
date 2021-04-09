#!/usr/bin/env python3
import cgi
import work_with_sqlLit as sql3

form = cgi.FieldStorage()
checkbox = form.getfirst("list_address")
country = form.getfirst('country')
discount = int(form.getfirst('discount-name', 0))
city = form.getfirst('city')
street = form.getfirst('street')
addresses = [None if country == '' else country,
             None if city == '' else city,
             None if street == '' else street]


product = form.getfirst("list_product")
p = product.split()

con = sql3.create_connect('mydatabase.db')
sql3.add_record_table_sales(con, p[1], p[2], p[3], float(p[4]), discount, addresses[0], addresses[1], addresses[2])

print("Content-type: text/html\n")
print('<script>location.href="test_script1.py"</script>')