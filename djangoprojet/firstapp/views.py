from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from . import work_with_sqlLit as sql3


def index(request):
    if request.method == 'GET':
        con = sql3.create_connect("mydatabase.db")
        rows = sql3.output_full_table(con)
        arr_all = list()
        for row in rows:
            arr = list()
            for i in range(7):
                if i == 5:
                    arr.append(str(row[i]) + ' %')
                else:
                    arr.append(row[i])
            if row[7] == None:
                arr.append('Нет доставки')
            else:
                arr.append('{0}, {1}, {2}'.format(row[7], row[8], row[9]))
            arr_all.append(arr)

        data = {'array':arr_all}
        return render(request,'table.html', context=data)
    else:
        if 'app-btn' in request.POST:
            return redirect('appa')
        elif 'chg-btn' in request.POST:
            return redirect('chan')



class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    field_order = ["age", "name"]


class AppendForm(forms.Form):
    name = forms.CharField()
    field_order = ["name"]


def index1(request):
    if request.method == 'POST':
        list_product = request.POST.get('list_product')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street = request.POST.get('street')
        addresses = [None if country == '' else country,
                     None if city == '' else city,
                     None if street == '' else street]
        p = list_product.split()
        con = sql3.create_connect('mydatabase.db')
        sql3.add_record_table_sales(con, p[1], p[2], p[3], float(p[4]), 0, addresses[0], addresses[1],
                                    addresses[2])
        return redirect('table')
    else:
        con = sql3.create_connect('mydatabase.db')
        rows = sql3.output_table_products(con)
        return render(request, "test.html", {"fields": rows})


def index2(request):
    if request.method == 'GET':
        con = sql3.create_connect("mydatabase.db")
        rows = sql3.output_full_table(con)
        arr_all = list()
        for row in rows:
            arr = list()
            for i in range(7):
                if i == 5:
                    arr.append(str(row[i]) + ' %'+"|")
                else:
                    arr.append(str(row[i]) + '|')
            if row[7] == None:
                arr.append('Нет доставки')
            else:
                arr.append('{0}, {1}, {2}'.format(row[7], row[8], row[9]))
            arr_all.append(arr)

        data = {'array': arr_all}
        return render(request, 'index.html', data)
    else:
        list_s = request.POST.get('list-sales')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street = request.POST.get('street')
        id = list_s.split('| ')[0]
        con = sql3.create_connect("mydatabase.db")
        sql3.update_record_table_sales(con,country,city,street,id)
        return redirect('table')