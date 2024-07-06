from flask import Flask, jsonify, request
from app.models import Cliente

app = Flask(__name__)

@app.route('/')
def index():
    response = {"message": "Hola mundo desde API Flask"}
    return jsonify(response)

@app.route('/api/clientes/<int:id_cliente>', methods=['GET'])
def get_cliente(id_cliente):
    try:
        cliente = Cliente.get_by_id_cliente(id_cliente)
        if not cliente:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        return jsonify(cliente.serialize())
    except Exception as e:
        print(f"Error al obtener cliente: {e}")
        return jsonify({'error': 'Error al obtener cliente'}), 500

@app.route('/api/clientes', methods=['GET'])
def get_all_clientes():
    try:
        clientes = Cliente.get_all()
        list_clients = [cliente.serialize() for cliente in clientes]
        return jsonify(list_clients)
    except Exception as e:
        print(f"Error al obtener todos los clientes: {e}")
        return jsonify({'error': 'Error al obtener todos los clientes'}), 500

@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos no proporcionados'}), 400
        
        # Validar que todos los campos requeridos están presentes
        required_fields = ['nombre', 'apellido', 'correo', 'telefono']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo "{field}" es requerido'}), 400

        # Crear el nuevo cliente
        new_cliente = Cliente(
            nombre=data['nombre'],
            apellido=data['apellido'],
            correo=data['correo'],
            telefono=data['telefono'],
            id_cliente=data['id_cliente']  # Asignar el ID proporcionado manualmente
        )
        
        # Guardar el cliente en la base de datos
        new_cliente.save()

        return jsonify({'message': 'Cliente creado con éxito'}), 201
    except KeyError as ke:
        return jsonify({'error': f'Campo faltante en la solicitud: {str(ke)}'}), 400
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return jsonify({'error': f'Error al crear cliente: {str(e)}'}), 500


@app.route('/api/clientes/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    try:
        cliente = Cliente.get_by_id_cliente(id_cliente)
        if not cliente:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos no proporcionados'}), 400
        
        # Actualizar los campos del cliente
        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.apellido = data.get('apellido', cliente.apellido)
        cliente.correo = data.get('correo', cliente.correo)
        cliente.telefono = data.get('telefono', cliente.telefono)
        
        cliente.save()
        return jsonify({'message': 'Cliente actualizado correctamente'})
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return jsonify({'error': 'Error al actualizar cliente'}), 500

@app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    try:
        cliente = Cliente.get_by_id_cliente(id_cliente)
        if not cliente:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        
        cliente.delete()
        return jsonify({'message': 'Cliente eliminado correctamente'})
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        return jsonify({'error': 'Error al eliminar cliente'}), 500

if __name__ == '__main__':
    app.run(debug=True)
