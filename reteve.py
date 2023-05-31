import tkinter as tk
import datetime

#Colores

gris_claro='#2F3136'
gris_oscuro='#252526'

#Definiciones de ventana

win=tk.Tk()
win.title(f'Reteve 1.0')
win.resizable(tk.FALSE,tk.FALSE)
win.geometry('800x600')
win.configure(bg=gris_claro)

#Variable de numero de cita global

contador_citas=1

#Lista de vehiculos disponibles para seleccionar

#Holajajaj

lista_vehiculos = [
    "Automóvil Partícular y Vehículo de Carga Liviana (Menor o Igual a 3500kg)",
    "Automóvil Partícular y Vehículo de Carga Liviana (Mayor a 3500kg pero menor a 8000kg)",
    "Vehículo de Carga Pesada y Cabezales (Mayor o igual a 8000kg)",
    "Taxis",
    "Autobuses, Buses y Microbuses",
    "Motocicletas",
    "Equipo Especial de Obras",
    "Equipo Especial Agricola"
]

#Label Acerca De

acerca_label = tk.Label(win, text='\nReteve\nVersion: 1.0\nFecha de Creacion: 19/06/2023\nAutor: Sebastián Guillén Guzmán',bg=gris_claro,fg='white')

def borrar_items():

    label_inicio.place_forget()
    boton_inicio.place_forget()

    boton_menu.place_forget()
    
    boton_programar.place_forget()
    boton_cancelar.place_forget()
    boton_ingreso.place_forget()
    boton_tablero.place_forget()
    boton_fallas.place_forget()
    boton_configuracion.place_forget()
    boton_ayuda.place_forget()
    boton_acerca.place_forget()
    boton_salir.place_forget()

    acerca_label.place_forget()    
    
    tipo_cita_label.place_forget()
    tipo_cita_primera.place_forget()
    tipo_cita_reinspeccion.place_forget()

    ingrese_placa_label.place_forget()
    numero_placa_entry.place_forget()

    tipo_vehiculo_label.place_forget()
    tipo_vehiculo_listbox.place_forget()

    marca_vehiculo_label.place_forget()
    marca_vehiculo_entry.place_forget()
    
    modelo_vehiculo_label.place_forget()
    modelo_vehiculo_entry.place_forget()

    propietario_label.place_forget()
    propietario_entry.place_forget()

    telefono_label.place_forget()
    telefono_entry.place_forget()

    correo_label.place_forget()
    correo_entry.place_forget()

    direccion_label.place_forget()
    direccion_entry.place_forget()

def menu_principal():
    borrar_items()

    boton_programar.place(relx=0.25,rely=0.25,anchor='center')
    boton_cancelar.place(relx=0.50,rely=0.25,anchor='center')
    boton_ingreso.place(relx=0.75,rely=0.25,anchor='center')
    boton_tablero.place(relx=0.25,rely=0.50,anchor='center')
    boton_fallas.place(relx=0.50,rely=0.50,anchor='center')
    boton_configuracion.place(relx=0.75,rely=0.50,anchor='center')
    boton_ayuda.place(relx=0.25,rely=0.75,anchor='center')
    boton_acerca.place(relx=0.50,rely=0.75,anchor='center')
    boton_salir.place(relx=0.75,rely=0.75,anchor='center')

#Clase de vehiculo

class Vehiculo:
    def __init__(self, numero_cita, tipo_cita, numero_placa, tipo_vehiculo, marca, modelo, propietario, telefono, correo, direccion, fecha_hora, estado):
        self.numero_cita = numero_cita
        self.tipo_cita = tipo_cita
        self.numero_placa = numero_placa
        self.tipo_vehiculo = tipo_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.propietario = propietario
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.fecha_hora = fecha_hora
        self.estado = estado

#Funcion para obtener el numero de cita que se debe agregar

def obtener_numero_cita():
    global contador_citas
    numero_cita = contador_citas
    contador_citas += 1
    return numero_cita

#Funciones para obtener fecha automatica

def generar_fechas_disponibles():
    fechas_disponibles = []
    fecha_actual = datetime.datetime.now()
    duracion_cita = datetime.timedelta(minutes=20)
    horario_inicio = datetime.datetime(fecha_actual.year, fecha_actual.month, fecha_actual.day, 6, 0)
    horario_fin = datetime.datetime(fecha_actual.year, fecha_actual.month+1, fecha_actual.day, 21, 0)

    fecha_actual += duracion_cita - datetime.timedelta(minutes=fecha_actual.minute % 20)
    for i in range(30):
        while fecha_actual <= horario_fin + duracion_cita and fecha_actual <= horario_inicio + datetime.timedelta(days=30):
            fechas_disponibles.append(fecha_actual)
            fecha_actual += duracion_cita
        dia = datetime.timedelta(days=1)
        fecha_actual += dia
    return fechas_disponibles

def seleccionar_fecha():
    seleccion_completa = tk.listbox.get(tk.listbox.curselection())
    seleccion_fecha = datetime.datetime.strptime(seleccion_completa, "%d/%m/%Y %H:%M")
    fecha = seleccion_fecha.date()
    hora = seleccion_fecha.time()
    print("Fecha seleccionada:", fecha)
    print("Hora seleccionada:", hora)

def fecha_automatica():
    global fechas_disponibles
    fechas_disponibles = generar_fechas_disponibles()
    for fecha in fechas_disponibles:
        lista_fechas.insert(tk.END, fecha.strftime("%d/%m/%Y %H:%M"))

#Funcion de programar citas

###Llama a todos los botones

#Funcion para desplegar la informacion del programa

def acerca_de():
    borrar_items()

    boton_menu.place(relx=0.05,rely=0.05,anchor='center')
    acerca_label.place(relx=0.5,rely=0.4, anchor='center')

#Boton y label inicio

if True:
    label_inicio=tk.Label(win,text='RETEVE',fg='white',bg=gris_claro,font='Dubai 100 underline')
    boton_inicio=tk.Button(win, text='ENTRAR AL SISTEMA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=menu_principal)

#Botones menu principal

if True:
    boton_menu=tk.Button(win, text='←', fg='white',bg = gris_claro,font ='Dubai 8 bold',command=menu_principal,width=3,height=1,border=0)

    boton_programar=tk.Button(win, text='PROGRAMAR CITAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_cancelar=tk.Button(win, text='CANCELAR CITAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_ingreso=tk.Button(win, text='INGRESO DE VEHICULOS A LA ESTACION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_tablero=tk.Button(win, text='TABLERO DE REVISION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_fallas=tk.Button(win, text='LISTA DE FALLAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_configuracion=tk.Button(win, text='CONFIGURACION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_ayuda=tk.Button(win, text='AYUDA', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_acerca=tk.Button(win, text='ACERCA DE', fg='white',bg = gris_claro,font ='Dubai 10 bold',command=acerca_de,border=0)
    boton_salir=tk.Button(win, text='SALIR', fg='white',bg = gris_claro,font ='Dubai 10 bold',command=lambda:(win.quit()),border=0)

#Widgets programar citas

if True:

    #Tipo de cita

    tipo_cita_var=tk.IntVar()
    tipo_cita_label=tk.Label(win, font ='Consolas 10', text = 'Indique el tipo de cita',fg='white',bg =gris_claro)
    tipo_cita_primera=tk.Checkbutton(win, text='Primera Cita', variable=tipo_cita_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=0)
    tipo_cita_reinspeccion=tk.Checkbutton(win, text='Reinspeccion', variable=tipo_cita_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=1)

    #Numero de placa

    numero_placa_var=tk.StringVar()
    ingrese_placa_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese su numero de placa',fg='white',bg =gris_claro)
    numero_placa_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=numero_placa_var)

    #Tipo de vehiculo

    tipo_vehiculo_var=tk.StringVar()
    tipo_vehiculo_label=tk.Label(win, font ='Consolas 10', text = 'Seleccione su tipo de vehiculo',fg='white',bg =gris_claro)
    tipo_vehiculo_listbox=tk.Listbox(win, height=9,listvariable=tipo_vehiculo_var)
    tipo_vehiculo_listbox.insert(0, *lista_vehiculos)

    #Marca del vehiculo

    marca_vehiculo_var=tk.StringVar()
    marca_vehiculo_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese la marca de su vehiculo',fg='white',bg =gris_claro)
    marca_vehiculo_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=marca_vehiculo_var)

    #Modelo del vehiculo

    modelo_vehiculo_var=tk.StringVar()
    modelo_vehiculo_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese el modelo de su vehiculo',fg='white',bg =gris_claro)
    modelo_vehiculo_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=modelo_vehiculo_var)

    #Propietario del vehiculo

    propietario_var=tk.StringVar()
    propietario_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese el nombre del propietario del vehiculo',fg='white',bg =gris_claro)
    propietario_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=propietario_var)

    #Telefono del propietario del vehiculo

    telefono_var=tk.StringVar()
    telefono_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese el telefono del propietario del vehiculo',fg='white',bg =gris_claro)
    telefono_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=telefono_var)

    #Correo electronico del propietario del vehiculo

    correo_var=tk.StringVar()
    correo_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese el correo del propietario del vehiculo',fg='white',bg =gris_claro)
    correo_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=correo_var)

    #Direccion del propietario del vehiculo

    direccion_var=tk.StringVar()
    direccion_label=tk.Label(win, font ='Consolas 10', text = 'Ingrese la direccion del propietario del vehiculo',fg='white',bg =gris_claro)
    direccion_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=direccion_var)

    #Fecha y hora de la cita

    tipo_fecha=tk.StringVar()
    fecha_var=tk.StringVar()
    hora_var=tk.StringVar()

    boton_fecha_manual=tk.Button(win, text='INGRESAR FECHA MANUALMENTE', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=lambda:print("Fecha manual"))
    boton_fecha_automatica=tk.Button(win, text='INGRESAR FECHA AUTOMATICAMENTE', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=lambda:print("Fecha automatica"))

        ##Si la fecha es manual

    fecha_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=fecha_var)
    hora_entry=tk.Entry(win,width=25,bg='white',fg='black',textvariable=hora_var)

        ##Si la fecha es automatica
    
    scrollbar = tk.Scrollbar(win)
    lista_fechas = tk.Listbox(win, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_fechas.yview)

    boton_seleccionar_fecha = tk.Button(win, text="Seleccionar", command=seleccionar_fecha)

# Agregar valores al ListBox



#Widgets que deben aparecer al inicio del programa

label_inicio.place(relx=0.5,rely=0.3,anchor='center')
boton_inicio.place(relx=0.5,rely=0.6,anchor='center')



win.mainloop()

