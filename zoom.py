from requests import get as rget
from tkinter import Tk as tk
from tkinter import Label
from tkinter import Frame
from tkinter import Button
from tkinter.ttk import Treeview
from tkinter import messagebox as mb
from threading import Thread
from threading import active_count

#ID Учётных записей Zoom
#0Eicq62cQb6KJ6hpLcZrbg   IT ZRG
#IMrYcZQuSbi_Bdqhli5bsg   JSC
#vNvfbiNWSXyMzRJSqUQA7g   IT CAA
#w5OJUxmjSW27rzdUU3AFEg   IT PAD
#wk9hsLewTL-EmOjsYDRpNg   IT2
#yBlASHLiRE6NrXYlWlSzPA   IT PVS

#Заголовок с ключём аутентификации, берётся из веб-морды Zoom
headers_key = {'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6Imw2aWM3a3dKVEYyQUZqT1ZiVFVyeEEiLCJleHAiOjE2NDY4MjU2NDAsImlhdCI6MTY0MzgwMTc3M30.w6DPCWDILKx-mYdH5vEwCzY47T5K4EipURrn1wrOYpU'}
url_name = 'https://api.zoom.us/v2/users/'

PAD_id = 'w5OJUxmjSW27rzdUU3AFEg/'
JSC_id = 'IMrYcZQuSbi_Bdqhli5bsg/'
CAA_id = 'vNvfbiNWSXyMzRJSqUQA7g/'
IT2_id = 'wk9hsLewTL-EmOjsYDRpNg/'
PVS_id = 'yBlASHLiRE6NrXYlWlSzPA/'
ZRG_id = '0Eicq62cQb6KJ6hpLcZrbg/'

def Conf_info(tree, url_n, key, user_id):
    for i in tree.get_children(): tree.delete(i)
    #Запрос на просмотр встречь в конкретной учётке-----------------------------------------------------------------------------------------------
    zoom = rget( url_n + user_id +'meetings', 
          headers = key,
          #Параметр указывающий, что выводить нужно только предстоящие конференции
          params = {'type': 'upcoming'}
          )
          
    if int( zoom.status_code ) == 401:
        mb.showwarning("Ошибка", "Истёк врок действия токена")
    else:
        i = 0
        #Пробегаемся по Json-ам конференций, собираем и выводим нужную информацию
        for meet in zoom.json()['meetings']:
            #Название конференции
            conf_name = meet['topic']
            #Дата конференции
            conf_date = meet['start_time'].split('T')[0]
            #Час начала конференции
            start_hour = int( meet['start_time'].split('T')[1].split(':')[0] ) + 3
            #Минута начала конференции
            start_minet = meet['start_time'].split(':')[1]
            #Час окончания конференции
            end_hour = start_hour + meet['duration'] // 60
            #Минута окончания конференции
            end_minet = meet['duration'] % 60 + int( start_minet )
            #Если колличество минут становится больше час, то попровляю данные 
            if end_minet > 60: 
                end_minet = end_minet % 60
                end_hour += end_minet // 60
            tree.insert( parent = '', index = i, iid = i, text = '', values = ( conf_name, conf_date, str( start_hour ) + ':' + start_minet , str( end_hour ) + ':' + str( end_minet ), str( meet['duration'] // 60 ) + ' Час ' + str( meet['duration'] % 60 ) + ' Минут' ) )
            i += 1

def All_in_one():

    cout_th = active_count()
    
    if cout_th < 2:
        th = Thread( target = Conf_info, kwargs = { 'tree': PADtree,'url_n': url_name,'key': headers_key,'user_id':PAD_id } )
        th.start()
    
        th = Thread( target = Conf_info, kwargs = { 'tree': JSCtree,'url_n': url_name,'key': headers_key,'user_id':JSC_id } )
        th.start()
        
        th = Thread( target = Conf_info, kwargs = { 'tree': CAAtree,'url_n': url_name,'key': headers_key,'user_id':CAA_id } )
        th.start()
        
        th = Thread( target = Conf_info, kwargs = { 'tree': IT2tree,'url_n': url_name,'key': headers_key,'user_id':IT2_id } )
        th.start()
        
        th = Thread( target = Conf_info, kwargs = { 'tree': PVStree,'url_n': url_name,'key': headers_key,'user_id':PVS_id } )
        th.start()
        
        th = Thread( target = Conf_info, kwargs = { 'tree': ZRGtree,'url_n': url_name,'key': headers_key,'user_id':ZRG_id } )
        th.start()
    else:
        mb.showwarning("Предупреждение", "Нельзя так часто нажимать")
        

#zoom = requests.get(
    #'https://api.zoom.us/v2/users/', 
    #headers={'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6Imw2aWM3a3dKVEYyQUZqT1ZiVFVyeEEiLCJleHAiOjE2NDM0NDc1MDMsImlhdCI6MTY0MzM2MTEwNH0.BejSNMkJyuliIdeliN3P57Ro9KDnye_-iwQLuGvIVjI'})

#GUI------------------------------------------------------------------------------------------------------------------------------------------------

#Создаю окно
mywindow = tk()
mywindow.geometry('1150x600')
mywindow.title('Zoom-Радар')

frame1 = Frame(mywindow)
frame1.place(x = 0, y = 0, width = 550, height = 183)

label1 = Label( frame1, text = 'Zoom PAD', font = '16' )
label1.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
PADtree = Treeview(frame1, show = 'headings', columns = columns)
#Добавляю названия столбцов
PADtree.heading('name', text = 'Название')
PADtree.heading('date', text = 'Дата')
PADtree.column('date', width = 65)
PADtree.heading('st_time', text = 'Начало')
PADtree.column('st_time', width = 60)
PADtree.heading('en_time', text = 'Окончание')
PADtree.column('en_time', width = 65)
PADtree.heading('dura', text = 'Продолжительность')

frame2 = Frame(mywindow)
frame2.place(x = 0, y = 183, width = 550, height = 183)

label2 = Label( frame2, text = 'Zoom JSC', font = '16' )
label2.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
JSCtree = Treeview(frame2, show = 'headings', columns = columns)
#Добавляю названия столбцов
JSCtree.heading('name', text = 'Название')
JSCtree.heading('date', text = 'Дата')
JSCtree.heading('st_time', text = 'Начало')
JSCtree.heading('en_time', text = 'Окончание')
JSCtree.heading('dura', text = 'Продолжительность')
JSCtree.column('date', width = 65)
JSCtree.column('st_time', width = 60)
JSCtree.column('en_time', width = 65)

frame3 = Frame(mywindow)
frame3.place(x = 0, y = 366, width = 550, height = 183)

label3 = Label( frame3, text = 'Zoom CAA', font = '16' )
label3.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
CAAtree = Treeview(frame3, show = 'headings', columns = columns)
#Добавляю названия столбцов
CAAtree.heading('name', text = 'Название')
CAAtree.heading('date', text = 'Дата')
CAAtree.heading('st_time', text = 'Начало')
CAAtree.heading('en_time', text = 'Окончание')
CAAtree.heading('dura', text = 'Продолжительность')
CAAtree.column('date', width = 65)
CAAtree.column('st_time', width = 60)
CAAtree.column('en_time', width = 65)

frame4 = Frame(mywindow)
frame4.place(x = 600, y = 0, width = 550, height = 183)

label4 = Label( frame4, text = 'Zoom IT2', font = '16' )
label4.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
IT2tree = Treeview(frame4, show = 'headings', columns = columns)
#Добавляю названия столбцов
IT2tree.heading('name', text = 'Название')
IT2tree.heading('date', text = 'Дата')
IT2tree.heading('st_time', text = 'Начало')
IT2tree.heading('en_time', text = 'Окончание')
IT2tree.heading('dura', text = 'Продолжительность')
IT2tree.column('date', width = 65)
IT2tree.column('st_time', width = 60)
IT2tree.column('en_time', width = 65)

frame5 = Frame(mywindow)
frame5.place(x = 600, y = 183, width = 550, height = 183)

label5 = Label( frame5, text = 'Zoom PVS', font = '16' )
label5.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
PVStree = Treeview(frame5, show = 'headings', columns = columns)
#Добавляю названия столбцов
PVStree.heading('name', text = 'Название')
PVStree.heading('date', text = 'Дата')
PVStree.heading('st_time', text = 'Начало')
PVStree.heading('en_time', text = 'Окончание')
PVStree.heading('dura', text = 'Продолжительность')
PVStree.column('date', width = 65)
PVStree.column('st_time', width = 60)
PVStree.column('en_time', width = 65)

frame6 = Frame(mywindow)
frame6.place(x = 600, y = 366, width = 550, height = 183)

label6 = Label( frame6, text = 'Zoom ZRG', font = '16' )
label6.pack()

#Создаю переменную с id столбцов
columns = ('name', 'date', 'st_time', 'en_time', 'dura')
#Создаю таблицу
ZRGtree = Treeview(frame6, show = 'headings', columns = columns)
#Добавляю названия столбцов
ZRGtree.heading('name', text = 'Название')
ZRGtree.heading('date', text = 'Дата')
ZRGtree.heading('st_time', text = 'Начало')
ZRGtree.heading('en_time', text = 'Окончание')
ZRGtree.heading('dura', text = 'Продолжительность')
ZRGtree.column('date', width = 65)
ZRGtree.column('st_time', width = 60)
ZRGtree.column('en_time', width = 65)

button = Button( mywindow, 
    text = 'Обновить/вывести информацию о конференциях',
    command = All_in_one
    )
    
button.place(x = 450, y = 550)

PADtree.pack()

JSCtree.pack()

CAAtree.pack()

IT2tree.pack()

PVStree.pack()

ZRGtree.pack()

mywindow.mainloop()
    
