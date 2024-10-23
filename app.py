#app.py
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


# Página principal: muestra la lista de productos
@app.route("/", methods=['GET', 'POST'])
def gestion_productos():
    if 'productos' not in session:
        session['productos'] = []
    productos = session.get('productos', [])
    return render_template("productoslist.html", productos=productos)


# Genera un nuevo ID para los productos
def generar_id():
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) + 1
    else:
        return 1


# Registrar un nuevo producto
@app.route("/registro", methods=['GET', 'POST'])
def registrar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        nuevo_producto = {
            'id': generar_id(),
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        if 'productos' not in session:
            session['productos'] = []
        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('gestion_productos'))

    return render_template('registro.html')


# Editar un producto existente
@app.route("/editarlist/<int:id>", methods=['GET', 'POST'])
def editarlist(id):
    lista_productos = session.get('productos', [])
    producto = next((i for i in lista_productos if i['id'] == id), None)
    if not producto:
        return redirect(url_for('gestion_productos'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('gestion_productos'))

    return render_template('editarproduc.html', producto=producto)


# Eliminar un producto
@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    lista_productos = session.get('productos', [])
    producto = next((i for i in lista_productos if i['id'] == id), None)
    if producto:
        session['productos'].remove(producto)
        session.modified = True
    return redirect(url_for('gestion_productos'))


if __name__ == "__main__":
    app.run(debug=True)