
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Límite máximo de cada fotografía: 8 MB
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/analizar", methods=["POST"])
def analizar():
    if "imagen" not in request.files:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    archivo = request.files["imagen"]

    if not archivo.filename:
        return jsonify({"error": "Selecciona una fotografía"}), 400

    try:
        datos = archivo.read()

        # Validar que sea una imagen real
        imagen = Image.open(BytesIO(datos))
        imagen.verify()

        # Leer sus características
        imagen = Image.open(BytesIO(datos))

        if imagen.format not in ["JPEG", "PNG", "WEBP"]:
            return jsonify({"error": "Formato no permitido"}), 400

        ancho, alto = imagen.size

        if ancho * alto > 20_000_000:
            return jsonify({"error": "La imagen tiene demasiados píxeles"}), 400

        return jsonify({
            "mensaje": "Fotografía recibida correctamente",
            "formato": imagen.format,
            "ancho": ancho,
            "alto": alto,
            "estado": "validada"
        })

    except Exception:
        return jsonify({"error": "No se pudo procesar la fotografía"}), 400


@app.errorhandler(413)
def archivo_demasiado_grande(error):
    return jsonify({"error": "La fotografía supera el límite de 8 MB"}), 413


if __name__ == "__main__":
    app.run(debug=True)
