from utils import Blueprint, render_template, flash, redirect, url_for, request, db, current_user, login_required, jsonify
from forms import form_pedido
import os
from models import Persona,Venta, Pizza
from datetime import datetime


"""
se que con el solo hecho de colocar el login requiered debe de redireccionar, pero no entiendo por que no me redirecciona y no entido el porqeu, asi que decidi implementar la logiga del flask login
pero con un dettale, que el login requiered lo aplico con el current user
"""

pizza_bp = Blueprint('pizza',__name__, template_folder='templates')
@pizza_bp.route('/pizza/')
@login_required
def index():
    
    form = form_pedido()
    print(f"Usuario logueado: {current_user.is_authenticated}")  

    # Leer los datos de las pizzas almacenadas en el archivo de texto
    pedidos = []
    if os.path.exists('pedido.txt'):
        with open('pedido.txt', 'r') as file:
            for linea in file.readlines():
                # Cargar los datos de cada pizza en una lista
                datos = linea.strip().split(',')
                pedidos.append(datos)
        with open('pedido.txt', 'r') as file:
            lineas = file.readlines()
        # Tomamos los primeros 3 campos de la primera línea como datos del cliente
        if lineas:
            persona_data = lineas[0].strip().split(',')
            nombre = persona_data[0]
            direccion = persona_data[1]
            telefono = persona_data[2]

    return render_template('index.html', form=form, data=pedidos)

@pizza_bp.route('/pizza/', methods=['POST'])
@login_required
def preparar_pedido():
    
    form = form_pedido()
    if form.validate_on_submit():
        nombre = form.nombre.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        tamanio = form.tamanio.data
        ingredientes = []  # Lista de ingredientes seleccionados
        if form.jamon.data:
            ingredientes.append('jamon')
        if form.pina.data:
            ingredientes.append('pina')
        if form.champi.data:
            ingredientes.append('champi')
        num = form.num_pizza.data
        valor = 0

        # Determinación del valor por tamaño
        if tamanio == 'chica':
            valor = 40
        elif tamanio == 'mediana':
            valor = 80
        elif tamanio == 'grande':
            valor = 120
        
        valor += 10 * len(ingredientes)  # Añadir el costo de los ingredientes seleccionados
        
        operacion = valor * int(num)
        
        # Guardamos el pedido en el archivo de texto
        with open('pedido.txt', 'a') as file:
            file.write(f'{nombre},{direccion},{telefono},{tamanio},{",".join(ingredientes)},{num},{operacion}\n')

        flash(f"Pizza agregada: {tamanio} con {', '.join(ingredientes)}, cantidad: {num}, subtotal: ${operacion}", "success")

    return redirect(url_for('pizza.index'))

@pizza_bp.route('/quitar')
@login_required
def quitar():

    form = form_pedido()

    indice = int(request.args.get('numero'))

    # Leemos el archivo y eliminamos la línea correspondiente
    if os.path.exists('pedido.txt'):
        with open('pedido.txt', 'r') as file:
            lineas = file.readlines()

        if 0 <= indice < len(lineas):
            lineas.pop(indice)

        # Escribimos el archivo de nuevo sin la pizza eliminada
        with open('pedido.txt', 'w') as file:
            file.writelines(lineas)

    flash("Pizza eliminada exitosamente", "danger")
    return redirect(url_for('pizza.index'))

@pizza_bp.route('/terminar', methods=['POST'])
@login_required
def terminar():
    if current_user.is_authenticated == False:
        return redirect('/')
    form = form_pedido()

    # Inicializar el total
    total = 0
    persona_data = None

    # Leer las pizzas del archivo y calcular el total
    with open('pedido.txt', 'r') as file:
        lineas = file.readlines()

        # Tomamos los primeros 3 campos de la primera línea como datos del cliente
        if lineas:
            persona_data = lineas[0].strip().split(',')
            nombre = persona_data[0]
            direccion = persona_data[1]
            telefono = persona_data[2]
        
        os.system('cls')
        print(lineas)
        # Crear y guardar la persona (cliente)
        persona = Persona(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
        )
        db.session.add(persona)
        db.session.commit()  # Guardar la persona en la base de datos
        # Crear la venta primero, sin asociar pizzas aún
        venta = Venta(total=total, persona_id=persona.id)
        db.session.add(venta)
        db.session.commit()  # Guardar la venta en la base de datos y obtener el id
        os.system('cls')
#joel,pp,123456,mediana,jamon,pina,champi,2,220
        print(venta)
        # Iterar sobre las líneas del archivo para calcular el total y guardar las pizzas
        for linea in lineas:  # Comenzamos desde la segunda línea para las pizzas
            campos = linea.strip().split(',')
            
            tamanio = campos[3]
            num = int(campos[-2])  # Número de pizzas
            subtotal = float(campos[-1])  # Subtotal por pizza

            ingredientes = campos[4:-2]

            # Sumar el subtotal de la pizza
            total += subtotal  # Actualizar el total con el subtotal de cada pizza
            os.system('cls')
            print(ingredientes)
            # Guardar la pizza en la base de datos, asociada a la venta
            nueva_pizza = Pizza(
                tamanio=tamanio,
                ingredientes=','.join(ingredientes),  # Guardar los ingredientes como cadena
                cantidad=num,
                venta_id=venta.id  # Asociar la pizza a la venta
            )
            db.session.add(nueva_pizza)

        # Actualizar el total de la venta en la base de datos
        venta.total = total
        db.session.commit()  # Guardar el total actualizado

    flash(f"El total de tu pedido es: ${total}", "success")

    # Limpiar el archivo de texto después de procesar el pedido
    with open('pedido.txt', 'w') as file:
        file.truncate(0)

    return redirect(url_for('pizza.index'))

@pizza_bp.route('/ventas', methods=['POST'])
@login_required
def ventas():
    if current_user.is_authenticated == False:
        return redirect('/')
    form = form_pedido()
    fecha_str = request.form.get('fechatotal')

    if fecha_str:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        # Buscar ventas del día seleccionado
        ventas = Venta.query.filter(db.func.date(Venta.fecha) == fecha.date()).all()
    else:
        periodo = request.form.get('periodo')
        fecha = datetime.now()

        if periodo == 'dia':
            # Buscar ventas del día actual
            ventas = Venta.query.filter(db.func.date(Venta.fecha) == fecha.date()).all()
        elif periodo == 'mes':
            # Buscar ventas del mes actual
            ventas = Venta.query.filter(
                db.func.extract('month', Venta.fecha) == fecha.month,
                db.func.extract('year', Venta.fecha) == fecha.year
            ).all()
        else:
            ventas = []

    total_ventas = sum([venta.total for venta in ventas])

    return render_template('index.html', form=form, ventas=ventas, total_ventas=total_ventas)

