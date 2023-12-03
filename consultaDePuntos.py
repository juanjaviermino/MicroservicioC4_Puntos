from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_puntos(ps_identificacion):
    url = "https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp"
    params = {
        "ps_tipo_identificacion": "CED",
        "ps_identificacion": ps_identificacion
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        puntos_element = soup.find("td", class_="titulo1", width="30")
        if puntos_element and "javascript:consulta_puntos();" in str(puntos_element):
            puntos = puntos_element.get_text(strip=True)
            return puntos
        else:
            return "Puntos not found on the page"

    except requests.RequestException as e:
        return f"Error: {e}"

@app.route('/get_license_points', methods=['GET'])
def get_license_points():
    cedula = request.args.get('cedula')
    if not cedula:
        return jsonify({"Error": "Cédula is required"}), 400
    result = get_puntos(cedula)
    return jsonify({"Puntos": result})

if __name__ == '__main__':
    app.run()
