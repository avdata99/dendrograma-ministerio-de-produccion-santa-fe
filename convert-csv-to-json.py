"""
PY3
Convertir el CSV derivado de lo que libera el municipio al JSON que usa la visualizacion
"""
import requests
import tempfile
import json
import csv


# original
csv_online = 'https://docs.google.com/feeds/download/spreadsheets/Export?key={key}&exportFormat={format}&gid={gid}'.format(key='1xuI1TQ0wO2l8Q-3xRbzDFEsHxnJsq2wxdWpVBteXUMk', format='csv', gid='96957613')
csv_origen = "dendrograma/funcionarios.csv"
# descargar
r = requests.get(csv_online)
tf = open(csv_origen, 'w')
tf.write(r.content.decode("utf-8"))
tf.close()  # borra el temporal

# destino
json_destino = "dendrograma/funcionarios.json"

resultados = {"count": 0, "results": []}

with open(csv_origen) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		# objeto funconario
		func = {}

		func["id"] = row["id"]
		func["funcionario"] = {}
		func["funcionario"]["nombre"] = row["Nombre"]
		func["funcionario"]["apellido"] = ""
		func["funcionario"]["nombrepublico"] = row["Nombre"]
		func["funcionario"]["franjaetaria"] = ""
		func["funcionario"]["genero"] = row["genero"]
		func["funcionario"]["edad"] = 0
		func["funcionario"]["url"] = ""
		func["funcionario"]["foto"] = {"original": "images/default_profile.jpg", "thumbnail_32x32": "images/default_profile.jpg", "thumbnail":"images/default_profile.jpg"}
		func["funcionario"]["uniqueid"] = ""
		func["cargo"] = {}
		func["cargo"]["id"] = row["id"]
		func["cargo"]["categoria"] = {}
		func["cargo"]["categoria"]["id"] = row["id"]  # no usamos
		func["cargo"]["categoria"]["nombre"] = row["Cargo"]  # no usamos
		func["cargo"]["categoria"]["requiere_declaracion_jurada"] = True  # no usamos
		func["cargo"]["categoria"]["nombre_corto"] = row["Cargo"]  # no usamos
		func["cargo"]["categoria"]["orden"] = 10
		func["cargo"]["nombre"] = row["Cargo"]

		if row["depende_de"] == "" or row["depende_de"] == "0":
			row["depende_de"] = None

		func["cargo"]["depende_de"] = row["depende_de"]
		func["cargo"]["electivo"] = False  # no usamos
		func["cargo"]["superioresids"] = []  # no usamos
		func["cargo"]["oficina"] = row["Telefono"]
		func["fecha_inicio"] = ""
		func["fecha_fin"] = ""
		func["decreto_nro"] = None
		func["decreto_pdf"] = ""

		resultados["results"].append(func)
		resultados["count"] += 1


to_file = json.dumps(resultados)

f = open(json_destino, 'w')
f.write(to_file)
f.close()
