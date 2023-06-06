import tkinter as tk
from tkinter import messagebox
import datetime
from validate_email_address import validate_email
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from email import encoders

#Colores

gris_claro='#2F3136'
gris_oscuro='#252526'
rosado_error='#ffbba8'

#Anchor de ventana

centro='center'

#Definiciones de ventana

win=tk.Tk()
win.title(f'Reteve 1.0')
win.resizable(tk.FALSE,tk.FALSE)
win.geometry('800x600')
win.configure(bg=gris_claro)

#Variable de numero de cita global

contador_citas=1

#Lista de las fechas que pueden ser programadas, se actualiza con la funcion generar fechas

fechas_programables=[]

#Lista de las fechas que ya estan programadas

fechas_programadas=[]

#Lista de citas programadas, por efectos de eficiencia aun no esta implementado en arbol

citas_programadas=[]

arbol_citas=[]

#Diccionario de configuracion y vehiculos y sus tarifas

configuracion={'lineas_trabajo':6,
'hora_inicial':6,
'hora_final':21,
'minutos_cita':20,
'dias_reinspeccion':30,
'fallas_graves':4,
'meses_citas':1,
'iva':13.0}

tabla_tarifas = {
    "Automóvil Partícular y Vehículo de Carga Liviana (Menor o Igual a 3500kg)": 10920,
    "Automóvil Partícular y Vehículo de Carga Liviana (Mayor a 3500kg pero menor a 8000kg)": 14380,
    "Vehículo de Carga Pesada y Cabezales (Mayor o igual a 8000kg)": 14380,
    "Taxis": 11785,
    "Autobuses, Buses y Microbuses": 14380,
    "Motocicletas": 7195,
    "Equipo Especial de Obras": 14380,
    "Equipo Especial Agrícola": 6625
}

tarifas_entries={}

tarifas_labels=[]

#Lista de vehiculos disponibles para seleccionar

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

    #Botones de inicio

    label_inicio.place_forget()
    boton_inicio.place_forget()

    #Boton de volver al menu

    boton_menu.place_forget()
    
    #Botones de menu principal

    boton_programar.place_forget()
    boton_cancelar.place_forget()
    boton_ingreso.place_forget()
    boton_tablero.place_forget()
    boton_fallas.place_forget()
    boton_configuracion.place_forget()
    boton_ayuda.place_forget()
    boton_acerca.place_forget()
    boton_salir.place_forget()

    #Label de informacion de acerca de

    acerca_label.place_forget()    
    
    #Botones de programar citas

    boton_paso_adelante.place_forget()
    boton_paso_atras.place_forget()

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

    tipo_fecha_label.place_forget()
    boton_fecha_automatica.place_forget()
    boton_fecha_manual.place_forget()

    amd_label.place_forget()
    year_entry.place_forget()
    mes_entry.place_forget()
    dia_entry.place_forget()

    hm_label.place_forget()
    hora_entry.place_forget()
    minuto_entry.place_forget()

    listbox_fechas.place_forget()
    scrollbar_fechas.place_forget()
    boton_seleccionar_fecha.place_forget()

    #Botones de configuracion

    lineas_label.pack_forget()
    lineas_entry.pack_forget()
    hora_inicial_label.pack_forget()
    hora_inicial_entry.pack_forget()
    hora_final_label.pack_forget()
    hora_final_entry.pack_forget()
    minutos_cita_label.pack_forget()
    minutos_cita_entry.pack_forget()
    dias_reinspeccion_label.pack_forget()
    dias_reinspeccion_entry.pack_forget()
    fallas_graves_label.pack_forget()
    fallas_graves_entry.pack_forget()
    meses_citas_label.pack_forget()
    meses_citas_entry.pack_forget()
    iva_label.pack_forget()
    iva_entry.pack_forget()

    for i in tarifas_entries:
        tarifas_entries[i].pack_forget()
    for i in tarifas_labels:
        i.pack_forget()

    tarifas_label.pack_forget()

    boton_aplicar.pack_forget()

def menu_principal():
    borrar_items()

    boton_programar.place(relx=0.25,rely=0.25,anchor=centro)
    boton_cancelar.place(relx=0.50,rely=0.25,anchor=centro)
    boton_ingreso.place(relx=0.75,rely=0.25,anchor=centro)
    boton_tablero.place(relx=0.25,rely=0.50,anchor=centro)
    boton_fallas.place(relx=0.50,rely=0.50,anchor=centro)
    boton_configuracion.place(relx=0.75,rely=0.50,anchor=centro)
    boton_ayuda.place(relx=0.25,rely=0.75,anchor=centro)
    boton_acerca.place(relx=0.50,rely=0.75,anchor=centro)
    boton_salir.place(relx=0.75,rely=0.75,anchor=centro)

#Clase de vehiculo

class vehiculo:
    def __init__(self, numero_cita, tipo_cita, numero_placa, tipo_vehiculo, marca, modelo, propietario, telefono, correo, direccion, fecha,hora, estado):
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
        self.fecha= fecha
        self.hora = hora
        self.estado = estado
    def __repr__(self) -> str:
        return f'Vehiculo\nNumero Cita: {self.numero_cita}\nTipo de Cita: {self.tipo_cita}\nNumero de Placa: {self.numero_placa}\nTipo de Vehiculo: {self.tipo_vehiculo}\nMarca: {self.marca}\nModelo: {self.modelo}\nPropietario: {self.propietario}\nTelefono: {self.telefono}\nCorreo: {self.correo}\nDireccion: {self.direccion}\nFecha: {self.fecha}\nHora: {self.hora}\nEstado: {self.estado}'

#Funcion de programar citas

def programar_citas():
    numero_cita=obtener_numero_cita()
    paso_tipo_cita()

#Funcion para obtener el numero de cita que se debe agregar

def obtener_numero_cita():
    global contador_citas
    numero_cita = contador_citas
    contador_citas += 1
    return numero_cita

#Funcion para llamar cada paso de la programacion de citas

def paso_tipo_cita():
    borrar_items()
    
    boton_paso_adelante.config(command=paso_numero_placa)

    tipo_cita_label.place(relx=0.5,rely=0.3,anchor=centro)
    tipo_cita_primera.place(relx=0.35,rely=0.4,anchor=centro)
    tipo_cita_reinspeccion.place(relx=0.65,rely=0.4,anchor=centro)

    boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_numero_placa():
    borrar_items()

    boton_paso_adelante.config(command=paso_tipo_vehiculo)
    boton_paso_atras.config(command=paso_tipo_cita)

    ingrese_placa_label.place(relx=0.5,rely=0.3,anchor=centro)
    numero_placa_entry.place(relx=0.5,rely=0.4,anchor=centro)

    boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
    boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_tipo_vehiculo():
    if numero_placa_entry.get()=='':
        numero_placa_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un numero de placa antes de ir al siguiente paso')
        paso_numero_placa()
    elif len(numero_placa_entry.get()) not in range(1,9):
        numero_placa_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: El numero de placa debe tener entre 1 y 8 caracteres')
        paso_numero_placa()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_marca)
        boton_paso_atras.config(command=paso_numero_placa)

        tipo_vehiculo_label.place(relx=0.5,rely=0.3,anchor=centro)
        tipo_vehiculo_listbox.place(relx=0.5,rely=0.6,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_marca():
    global tipo_vehiculo_var
    try:
        if tipo_vehiculo_listbox.get(tipo_vehiculo_listbox.curselection())!='':
            borrar_items()

            boton_paso_adelante.config(command=paso_modelo)
            boton_paso_atras.config(command=paso_tipo_vehiculo)

            marca_vehiculo_label.place(relx=0.5,rely=0.3,anchor=centro)
            marca_vehiculo_entry.place(relx=0.5,rely=0.4,anchor=centro)

            boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
            boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
            boton_menu.place(relx=0.05,rely=0.05,anchor=centro)
    except:
        messagebox.showerror('Error','Error: Debe seleccionar un tipo de vehiculo antes de ir al siguiente paso')
        paso_tipo_vehiculo()
    
def paso_modelo():
    if marca_vehiculo_entry.get()=='':
        marca_vehiculo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar una marca de vehiculo antes de ir al siguiente paso')
        paso_marca()
    elif len(marca_vehiculo_entry.get()) not in range(3,16):
        marca_vehiculo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: La marca del vehiculo debe tener entre 3 y 15 caracteres')
        paso_marca()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_propietario)
        boton_paso_atras.config(command=paso_marca)

        modelo_vehiculo_label.place(relx=0.5,rely=0.3,anchor=centro)
        modelo_vehiculo_entry.place(relx=0.5,rely=0.4,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_propietario():
    if modelo_vehiculo_entry.get()=='':
        modelo_vehiculo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un modelo de vehiculo antes de ir al siguiente paso')
        paso_modelo()
    elif len(modelo_vehiculo_entry.get()) not in range(1,16):
        modelo_vehiculo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: El modelo del vehiculo debe tener entre 1 y 15 caracteres')
        paso_modelo()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_telefono)
        boton_paso_atras.config(command=paso_modelo)

        propietario_label.place(relx=0.5,rely=0.3,anchor=centro)
        propietario_entry.place(relx=0.5,rely=0.4,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_telefono():
    if propietario_entry.get()=='':
        propietario_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un nombre de propietario antes de ir al siguiente paso')
        paso_propietario()
    elif len(propietario_entry.get()) not in range(6,41):
        propietario_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: El nombre del propietario del vehiculo debe tener entre 6 y 40 caracteres')
        paso_propietario()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_correo)
        boton_paso_atras.config(command=paso_propietario)

        telefono_label.place(relx=0.5,rely=0.3,anchor=centro)
        telefono_entry.place(relx=0.5,rely=0.4,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_correo():
    if telefono_entry.get()=='':
        telefono_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un numero de telefono antes de ir al siguiente paso')
        paso_telefono()
    elif len(telefono_entry.get()) > 20:
        telefono_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: El telefono del propietario debe tener 20 caracteres')
        paso_telefono()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_direccion)
        boton_paso_atras.config(command=paso_telefono)

        correo_label.place(relx=0.5,rely=0.3,anchor=centro)
        correo_entry.place(relx=0.5,rely=0.4,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_direccion():
    existe=validate_email(correo_entry.get(),verify=True)
    if correo_entry.get()=='':
        correo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un correo antes de ir al siguiente paso')
        paso_correo()
    elif not existe:
        correo_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar un correo valido')
        paso_correo()
    else:
        borrar_items()

        boton_paso_adelante.config(command=paso_fecha)
        boton_paso_atras.config(command=paso_correo)

        direccion_label.place(relx=0.5,rely=0.3,anchor=centro)
        direccion_entry.place(relx=0.5,rely=0.4,anchor=centro)

        boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_fecha():
    global fechas_programables
    if direccion_entry.get()=='':
        direccion_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: Debe ingresar una direccion antes de ir al siguiente paso')
        paso_direccion()
    elif len(direccion_entry.get()) not in range(10,41):
        direccion_entry.config(bg=rosado_error)
        messagebox.showerror('Error','Error: La direccion del propietario debe tener entre 10 y 40 caracteres')
        paso_direccion()
    else:
        generar_fechas_disponibles()
        borrar_items()

        boton_paso_adelante.config(command=paso_programar)
        boton_paso_atras.config(command=paso_direccion)

        tipo_fecha_label.place(relx=0.5,rely=0.3,anchor=centro)
        boton_fecha_manual.place(relx=0.4,rely=0.4,anchor=centro)
        boton_fecha_automatica.place(relx=0.6,rely=0.4,anchor=centro)

        boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
        boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_fecha_manual():
    global tipo_fecha

    tipo_fecha='m'

    borrar_items()

    amd_label.place(relx=0.5,rely=0.2,anchor=centro)
    year_entry.place(relx=0.45,rely=0.3,anchor=centro)
    mes_entry.place(relx=0.51,rely=0.3,anchor=centro)
    dia_entry.place(relx=0.55,rely=0.3,anchor=centro)

    hm_label.place(relx=0.5,rely=0.4,anchor=centro)
    hora_entry.place(relx=0.47,rely=0.5,anchor=centro)
    minuto_entry.place(relx=0.53,rely=0.5,anchor=centro)

    boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
    boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_fecha_automatica():
    global tipo_fecha,fechas_disponibles

    tipo_fecha='a'

    borrar_items()

    fechas_disponibles = generar_fechas_disponibles()
    listbox_fechas.place(relx=0.5,rely=0.4,height=235,anchor=centro)
    scrollbar_fechas.place(relx=0.6,rely=0.4,height=235,anchor=centro)

    boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)
    boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)
    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)

def paso_programar():
    if tipo_fecha=='m':
        if year_entry.get()=='' or not year_entry.get().isdigit:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            hora_entry.config(bg=rosado_error)
            minuto_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar un numero que represente un año antes de continuar')
            paso_fecha_manual()
        elif mes_entry.get()==''or not mes_entry.get().isdigit:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar un numero que represente un mes antes de continuar')
            paso_fecha_manual()
        elif dia_entry.get()==''or not dia_entry.get().isdigit:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar un numero que represente un dia antes de continuar')
            paso_fecha_manual()
        elif hora_entry.get()==''or not hora_entry.get().isdigit:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            hora_entry.config(bg=rosado_error)
            minuto_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar un numero que represente una hora antes de continuar')
            paso_fecha_manual()
        elif minuto_entry.get()==''or not minuto_entry.get().isdigit:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            hora_entry.config(bg=rosado_error)
            minuto_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar un numero que represente un minuto antes de continuar')
            paso_fecha_manual()
        fecha_str = f'{year_entry.get()}-{mes_entry.get()}-{dia_entry.get()}'
        hora_str=f'{hora_entry.get()}:{minuto_entry.get()}'
        fecha_hora_str=f'{year_entry.get()}-{mes_entry.get()}-{dia_entry.get()} {hora_entry.get()}:{minuto_entry.get()}'
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            hora=datetime.datetime.strptime(hora_str,"%H:%M")
        except:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            hora_entry.config(bg=rosado_error)
            minuto_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar una fecha valida')
            paso_fecha_manual()
        
        fecha_hora=datetime.datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        if fecha_hora_str not in fechas_programables:
            year_entry.config(bg=rosado_error)
            mes_entry.config(bg=rosado_error)
            dia_entry.config(bg=rosado_error)
            hora_entry.config(bg=rosado_error)
            minuto_entry.config(bg=rosado_error)
            messagebox.showerror('Error','Error: Debe ingresar una fecha valida')
            paso_fecha_manual()
    else:
        fecha_hora_str,fecha_str,hora_str=seleccionar_fecha()
    print(fecha_hora_str,fecha_hora_str in fechas_programables)
    for i in fechas_programables:
        if i==fecha_hora_str:
            fechas_programables.remove(i)
            fechas_programadas.append(i)

    numero_cita = obtener_numero_cita()
    tipo_cita = tipo_cita_var.get()
    numero_placa = numero_placa_entry.get()
    tipo_vehiculo = tipo_vehiculo_listbox.get('active')
    marca = marca_vehiculo_entry.get()
    modelo = modelo_vehiculo_entry.get()
    propietario = propietario_entry.get()
    telefono = telefono_entry.get()
    correo = correo_entry.get()
    direccion = direccion_entry.get()
    fecha,hora=fecha_str,hora_str
    estado = "PENDIENTE"

    cita = vehiculo(numero_cita, tipo_cita, numero_placa, tipo_vehiculo, marca, modelo, propietario, telefono, correo, direccion, fecha,hora, estado)
    for i in citas_programadas:
        if i.fecha == cita.fecha and i.numero_placa==cita.numero_placa:
            if i.tipo_cita == cita.tipo_cita:
                messagebox.showerror('Error','Error, no puede agendar una cita para el mismo vehiculo el mismo dia')
                paso_fecha()
            else:
                if i.tipo_cita==0 and cita.tipo_cita==1:
                    if int(i.hora[:2])>int(cita.hora):
                        pass
                    else:
                        if int(i.hora[:2])==int(cita.hora[:2]):
                            if int(i.hora[3:6])<=int(cita.hora[3:6]):
                                messagebox.showerror('Error','Error, no puede agendar una cita de reinspeccion para el mismo vehiculo el mismo dia si la fecha y hora es anterior a la primera cita')
                                paso_fecha()

    

    print(cita)
    citas_programadas.append(cita)
    print(citas_programadas)
    agregar_cita_abb(cita)
    enviar_email_cita(cita)
    messagebox.showinfo("Cita programada", "La cita ha sido programada correctamente, se ha enviado un comprobante a su direccion de correo electronico")
    menu_principal() 

#Funcion para enviar el correo comprobante de cita

def enviar_email_cita(cita):
    try:
        msg = MIMEMultipart()
    # setup the parameters of the message 
        password = "npglayqvauxdpyhq"
        msg['From'] = "emailsproyectopython@gmail.com"
        msg['To'] = cita.correo
        msg['Subject'] = "Comprobante cita RETEVE"

        texto=f'Hola, {cita.propietario}, usted ha agendado una cita en RETEVE para su vehiculo el dia {cita.fecha} a las {cita.hora}'
        msg.attach(MIMEText(texto, 'plain'))
        # create server 
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail 
        server.login(msg['From'], password)
        # send the message via the server. 
        server.send_message(msg)
        server.quit()
        print ('Email enviado exitosamente')   
    except:
        print('Ha ocurrido un error con la comunicacion al servidor, verifique su conexion a internet')

#Funcion para agregar la cita al arbol

def agregar_cita_abb(cita, nodo=None):
    if nodo is None:
        return {'cita': cita, 'izquierda': None, 'derecha': None}

    fecha_hora_cita = datetime.strptime(cita.fecha + ' ' + cita.hora, '%Y-%m-%d %H:%M')
    fecha_hora_nodo = datetime.strptime(nodo['cita'].fecha + ' ' + nodo['cita'].hora, '%Y-%m-%d %H:%M')

    if fecha_hora_cita < fecha_hora_nodo:
        nodo['izquierda'] = agregar_cita_abb(cita, nodo['izquierda'])
    else:
        nodo['derecha'] = agregar_cita_abb(cita, nodo['derecha'])
    
    return nodo

def generar_fechas_disponibles():
    print(configuracion['minutos_cita'])
    global fechas_programables
    fechas_disponibles = []
    fecha_actual = datetime.datetime.now()
    duracion_cita = datetime.timedelta(minutes=configuracion['minutos_cita'])
    horario_inicio = datetime.datetime.combine(fecha_actual.date(), datetime.time(configuracion['hora_inicial'], 0))
    horario_fin = datetime.datetime.combine((fecha_actual + datetime.timedelta(days=30*configuracion['meses_citas'])).date(), datetime.time(configuracion['hora_final'], 1))
    horario_fin_dia_siguiente = horario_fin + datetime.timedelta(days=1)

    fecha_actual += duracion_cita - datetime.timedelta(minutes=fecha_actual.minute % configuracion['minutos_cita'])

    while fecha_actual <= horario_fin_dia_siguiente:
        if fecha_actual.time() >= horario_inicio.time() and fecha_actual.time() <= horario_fin.time():
            if fecha_actual not in fechas_programadas:
                fechas_disponibles.append(fecha_actual)
        fecha_actual += duracion_cita

    for fecha in fechas_disponibles:
        fechas_programables.append(str(fecha)[:16])
        listbox_fechas.insert(tk.END, fecha.strftime("%d/%m/%Y %H:%M"))

    return fechas_disponibles

def seleccionar_fecha():
    seleccion_completa = listbox_fechas.get(listbox_fechas.curselection())
    seleccion_fecha = datetime.datetime.strptime(seleccion_completa, "%d/%m/%Y %H:%M")
    fecha = seleccion_fecha.date()
    hora = seleccion_fecha.time()
    return str(seleccion_fecha)[:16],str(fecha),str(hora)[:-3]

def fecha_automatica():
    global fechas_disponibles
    fechas_disponibles = generar_fechas_disponibles()
    for fecha in fechas_disponibles:
        listbox_fechas.insert(tk.END, fecha.strftime("%d/%m/%Y %H:%M"))

#Funcion de configuracion del programa

def configuracion_pt1():
    borrar_items()

    boton_paso_adelante.config(command=configuracion_pt2)

    # espacio=tk.Label(win, text=" ", bg=gris_claro, fg="white", font='Dubai 10', anchor="w")
    # espacio.pack(padx=10, pady=5)

    lineas_label.pack(padx=10, pady=3)
    lineas_entry.pack(padx=10, pady=3)
    

    hora_inicial_label.pack(padx=10, pady=3)
    hora_inicial_entry.pack(padx=10, pady=3)
    

    hora_final_label.pack(padx=10, pady=3)
    hora_final_entry.pack(padx=10, pady=3)
    

    minutos_cita_label.pack(padx=10, pady=3)
    minutos_cita_entry.pack(padx=10, pady=3)
    

    dias_reinspeccion_label.pack(padx=10, pady=3)
    dias_reinspeccion_entry.pack(padx=10, pady=3)
    

    fallas_graves_label.pack(padx=10, pady=3)
    fallas_graves_entry.pack(padx=10, pady=3)
    

    meses_citas_label.pack(padx=10, pady=3)
    meses_citas_entry.pack(padx=10, pady=3)
    

    iva_label.pack(padx=10, pady=3)
    iva_entry.pack(padx=10, pady=3)
    

    boton_paso_adelante.place(relx=0.9,rely=0.95,anchor=centro)

    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)
    boton_menu.lift()

def configuracion_pt2():
    borrar_items()

    boton_paso_atras.config(command=configuracion_pt1)

    for vehiculo, tarifa in tabla_tarifas.items():
        label = tk.Label(win, text=vehiculo, bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
        label.pack(padx=10, pady=1)
        tarifas_labels.append(label)
        entry = tk.Entry(win,font='Dubai 12',justify='center')
        entry.insert(0, tarifa)
        entry.pack(padx=10, pady=1)
        tarifas_entries[vehiculo] = entry

    boton_aplicar.pack(padx=10, pady=10)

    tarifas_label.pack(fill="x", padx=10, pady=5)

    boton_paso_atras.place(relx=0.1,rely=0.95,anchor=centro)

def aplicar_configuracion():
    global tabla_tarifas, configuracion
    lineas_trabajo = lineas_entry.get()
    hora_inicial = hora_inicial_entry.get()
    hora_final = hora_final_entry.get()
    minutos_cita = minutos_cita_entry.get()
    dias_reinspeccion = dias_reinspeccion_entry.get()
    fallas_graves = fallas_graves_entry.get()
    meses_citas = meses_citas_entry.get()
    iva = iva_entry.get()

    for vehiculo, entry in tarifas_entries.items():
        tabla_tarifas[vehiculo] = entry.get()
    
    # Lógica adicional para guardar la configuración
    
    # Ejemplo de impresión de los valores obtenidos
    print("Cantidad de líneas de trabajo:", lineas_trabajo)
    print("Hora inicial:", hora_inicial)
    print("Hora final:", hora_final)
    print("Minutos por cada cita de revisión:", minutos_cita)
    print("Cantidad máxima de días para reinspección:", dias_reinspeccion)
    print("Cantidad de fallas graves para sacar vehículo de circulación:", fallas_graves)
    print("Cantidad de meses para desplegar citas:", meses_citas)
    print("% de Impuesto al Valor Agregado (IVA) sobre la tarifa:", iva)
    print("Tabla de Tarifas:")
    for vehiculo, tarifa in tabla_tarifas.items():
        print(f"{vehiculo}: {tarifa}")

    # Validar los valores ingresados
    if not lineas_trabajo.isdigit() or int(lineas_trabajo) < 1 or int(lineas_trabajo) > 25:
        messagebox.showerror("Error", "Ingrese una cantidad válida de líneas de trabajo (entre 1 y 25).")
        return
    if not hora_inicial.isdigit() or int(hora_inicial) < 0 or int(hora_inicial) > 23:
        messagebox.showerror("Error", "Ingrese una hora inicial válida (entre 0 y 23).")
        return
    if not hora_final.isdigit() or int(hora_final) < 0 or int(hora_final) > 23 or int(hora_final) < int(hora_inicial):
        messagebox.showerror("Error", "Ingrese una hora final válida (entre 0 y 23, mayor o igual a la hora inicial).")
        return
    if not minutos_cita.isdigit() or int(minutos_cita) < 5 or int(minutos_cita) > 45:
        messagebox.showerror("Error", "Ingrese una cantidad válida de minutos por cita (entre 5 y 45).")
        return
    if not dias_reinspeccion.isdigit() or int(dias_reinspeccion) < 1 or int(dias_reinspeccion) > 60:
        messagebox.showerror("Error", "Ingrese una cantidad válida de días para reinspección (entre 1 y 60).")
        return
    if not fallas_graves.isdigit() or int(fallas_graves) <= 0:
        messagebox.showerror("Error", "Ingrese una cantidad válida de fallas graves (mayor a 0).")
        return
    if not meses_citas.isdigit() or int(meses_citas) < 1 or int(meses_citas) > 12:
        messagebox.showerror("Error", "Ingrese una cantidad válida de meses para desplegar citas (entre 1 y 12).")
        return
    try:
        iva = float(iva)
        if iva < 0 or iva > 20:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingrese un valor válido de IVA (entre 0 y 20).")
        return

    configuracion['lineas_trabajo']=int(lineas_trabajo)
    configuracion['hora_inicial']=int(hora_inicial)
    configuracion['hora_final']=int(hora_final)
    configuracion['minutos_cita']=int(minutos_cita)
    configuracion['dias_reinspeccion']=int(dias_reinspeccion)
    configuracion['fallas_graves']=int(fallas_graves) 
    configuracion['meses_citas']=int(meses_citas) 
    configuracion['iva']=float(iva) 

    messagebox.showinfo("Configuración guardada", "La configuración del sistema ha sido guardada correctamente.")
    print(configuracion)

#Funcion para desplegar la informacion del programa

def acerca_de():
    borrar_items()

    boton_menu.place(relx=0.05,rely=0.05,anchor=centro)
    acerca_label.place(relx=0.5,rely=0.4, anchor=centro)

#Boton y label inicio

if True:
    label_inicio=tk.Label(win,text='RETEVE',fg='white',bg=gris_claro,font='Dubai 100 underline')
    boton_inicio=tk.Button(win, text='ENTRAR AL SISTEMA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=menu_principal)

#Botones menu principal

if True:
    boton_menu=tk.Button(win, text='←', fg='white',bg = gris_claro,font ='Dubai 8 bold',command=menu_principal,width=3,height=1,border=0)

    boton_programar=tk.Button(win, text='PROGRAMAR CITAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0,command=programar_citas)
    boton_cancelar=tk.Button(win, text='CANCELAR CITAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_ingreso=tk.Button(win, text='INGRESO DE VEHICULOS A LA ESTACION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_tablero=tk.Button(win, text='TABLERO DE REVISION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_fallas=tk.Button(win, text='LISTA DE FALLAS', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_configuracion=tk.Button(win, text='CONFIGURACION', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0,command=configuracion_pt1)
    boton_ayuda=tk.Button(win, text='AYUDA', fg='white',bg = gris_claro,font ='Dubai 10 bold',border=0)
    boton_acerca=tk.Button(win, text='ACERCA DE', fg='white',bg = gris_claro,font ='Dubai 10 bold',command=acerca_de,border=0)
    boton_salir=tk.Button(win, text='SALIR', fg='white',bg = gris_claro,font ='Dubai 10 bold',command=lambda:(win.quit()),border=0)

#Widgets programar citas

if True:

    #Paso atras y paso adelante

    boton_paso_atras=tk.Button(win, text='← ANTERIOR', fg='white',bg = gris_claro,font ='Dubai 8 bold',command=menu_principal,border=0)
    boton_paso_adelante=tk.Button(win, text='SIGUIENTE →', fg='white',bg = gris_claro,font ='Dubai 8 bold',command=menu_principal,border=0)

    #Tipo de cita

    tipo_cita_var=tk.IntVar()
    tipo_cita_label=tk.Label(win, font ='Dubai 20', text = 'Indique el tipo de cita',fg='white',bg =gris_claro)
    tipo_cita_primera=tk.Checkbutton(win,font='Dubai 20', text='Primera Cita', variable=tipo_cita_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=0)
    tipo_cita_reinspeccion=tk.Checkbutton(win,font='Dubai 20', text='Reinspeccion', variable=tipo_cita_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=1)

    #Numero de placa

    numero_placa_var=tk.StringVar()
    ingrese_placa_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese su numero de placa',fg='white',bg =gris_claro)
    numero_placa_entry=tk.Entry(win,width=8,font='Dubai 20',bg='white',fg='black',textvariable=numero_placa_var)

    #Tipo de vehiculo

    tipo_vehiculo_var=tk.StringVar()
    tipo_vehiculo_label=tk.Label(win, font ='Dubai 20', text = 'Seleccione su tipo de vehiculo',fg='white',bg =gris_claro)
    tipo_vehiculo_listbox=tk.Listbox(win, height=8,width=67,bg=gris_oscuro,fg='white',font='Dubai 15',border=0,borderwidth=0,listvariable=tipo_vehiculo_var)
    tipo_vehiculo_listbox.insert(0, *lista_vehiculos)

    #Marca del vehiculo

    marca_vehiculo_var=tk.StringVar()
    marca_vehiculo_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese la marca de su vehiculo',fg='white',bg =gris_claro)
    marca_vehiculo_entry=tk.Entry(win,width=15,bg='white',font='Dubai 20',fg='black',textvariable=marca_vehiculo_var)

    #Modelo del vehiculo

    modelo_vehiculo_var=tk.StringVar()
    modelo_vehiculo_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese el modelo de su vehiculo',fg='white',bg =gris_claro)
    modelo_vehiculo_entry=tk.Entry(win,width=15,bg='white',font='Dubai 20',fg='black',textvariable=modelo_vehiculo_var)

    #Propietario del vehiculo

    propietario_var=tk.StringVar()
    propietario_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese el nombre del propietario del vehiculo',fg='white',bg =gris_claro)
    propietario_entry=tk.Entry(win,width=40,bg='white',fg='black',font='Dubai 20',textvariable=propietario_var)

    #Telefono del propietario del vehiculo

    telefono_var=tk.StringVar()
    telefono_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese el telefono del propietario del vehiculo',fg='white',bg =gris_claro)
    telefono_entry=tk.Entry(win,width=20,bg='white',font='Dubai 20',fg='black',textvariable=telefono_var)

    #Correo electronico del propietario del vehiculo

    correo_var=tk.StringVar()
    correo_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese el correo del propietario del vehiculo',fg='white',bg =gris_claro)
    correo_entry=tk.Entry(win,width=25,bg='white',font='Dubai 20',fg='black',textvariable=correo_var)

    #Direccion del propietario del vehiculo

    direccion_var=tk.StringVar()
    direccion_label=tk.Label(win, font ='Dubai 20', text = 'Ingrese la direccion del propietario del vehiculo',fg='white',bg =gris_claro)
    direccion_entry=tk.Entry(win,width=40,bg='white',font='Dubai 20',fg='black',textvariable=direccion_var)

    #Fecha y hora de la cita


    year_var=tk.StringVar()
    mes_var=tk.StringVar()
    dia_var=tk.StringVar()

    hora_var=tk.StringVar()
    minuto_var=tk.StringVar()

    tipo_fecha_label=tk.Label(win, font ='Dubai 20', text = 'Como desea ingresar la fecha de su cita?',fg='white',bg =gris_claro)
    boton_fecha_manual=tk.Button(win, text='MANUALMENTE', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=paso_fecha_manual)
    boton_fecha_automatica=tk.Button(win, text='AUTOMATICAMENTE', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=paso_fecha_automatica)

        ##Si la fecha es manual

    amd_label=tk.Label(win, font ='Dubai 20', text = 'Año/Mes/Dia',fg='white',bg =gris_claro)

    year_entry=tk.Entry(win,width=4,bg='white',fg='black',font='Dubai 20',textvariable=year_var)
    mes_entry=tk.Entry(win,width=2,bg='white',fg='black',font='Dubai 20',textvariable=mes_var)
    dia_entry=tk.Entry(win,width=2,bg='white',fg='black',font='Dubai 20',textvariable=dia_var)

    hm_label=tk.Label(win, font ='Dubai 20', text = 'Horas/Minutos',fg='white',bg=gris_claro)
    hora_entry=tk.Entry(win,width=2,bg='white',font='Dubai 20',fg='black',textvariable=hora_var)
    minuto_entry=tk.Entry(win,width=2,bg='white',font='Dubai 20',fg='black',textvariable=minuto_var)

        ##Si la fecha es automatica
    
    scrollbar_fechas = tk.Scrollbar(win)
    listbox_fechas = tk.Listbox(win,font='Dubai 10', yscrollcommand=scrollbar_fechas.set)
    scrollbar_fechas.config(command=listbox_fechas.yview)

    boton_seleccionar_fecha = tk.Button(win, text="Seleccionar",font='Dubai 20',bg=gris_oscuro,fg='white', command=seleccionar_fecha)

#Widgets configuracion parte 1

if True:

    lineas_label = tk.Label(win, text="Cantidad de líneas de trabajo en la estación:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    lineas_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    lineas_entry.insert(0,configuracion['lineas_trabajo'])

    hora_inicial_label = tk.Label(win, text="Hora inicial:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    hora_inicial_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    hora_inicial_entry.insert(0,configuracion['hora_inicial'])
    
    hora_final_label = tk.Label(win, text="Hora final:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    hora_final_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    hora_final_entry.insert(0,configuracion['hora_final'])
    
    minutos_cita_label = tk.Label(win, text="Minutos por cada cita de revisión:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    minutos_cita_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    minutos_cita_entry.insert(0,configuracion['minutos_cita'])
    
    dias_reinspeccion_label = tk.Label(win, text="Cantidad máxima de días para reinspección:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    dias_reinspeccion_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    dias_reinspeccion_entry.insert(0,configuracion['dias_reinspeccion'])
    
    fallas_graves_label = tk.Label(win, text="Cantidad de fallas graves para sacar vehículo de circulación:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    fallas_graves_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    fallas_graves_entry.insert(0,configuracion['fallas_graves'])
    
    meses_citas_label = tk.Label(win, text="Cantidad de meses para desplegar citas:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    meses_citas_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    meses_citas_entry.insert(0,configuracion['meses_citas'])

    iva_label = tk.Label(win, text="% de Impuesto al Valor Agregado (IVA) sobre la tarifa:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")
    iva_entry = tk.Entry(win,width=20,justify='center', font='Dubai 10')
    iva_entry.insert(0,configuracion['iva'])

#Widgets configuracion parte 2

if True:

    tarifas_label = tk.Label(win, text="Tabla de Tarifas:", bg=gris_claro, fg="white", font='Dubai 12', anchor="w")

    boton_aplicar = tk.Button(win, text="APLICAR", command=aplicar_configuracion, font='Dubai 12')
    
#Widgets que deben aparecer al inicio del programa

label_inicio.place(relx=0.5,rely=0.3,anchor=centro)
boton_inicio.place(relx=0.5,rely=0.6,anchor=centro)

win.mainloop()

#TODO: Funcion cancelar citas