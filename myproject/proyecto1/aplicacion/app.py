from flask import Flask, render_template, request, url_for, redirect
from os import listdir
from flask_bootstrap import Bootstrap5
from aplicacion.forms import formcalculadora, UploadForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "ClaveSecretaParaFormularios"
@app.route('/')
def inicio():
#    return render_template("inicio.html")
    lista=[]
    for file in listdir(app.root_path+"/static/img"):
        lista.append(file)
    return render_template("inicio2.html",lista=lista)

@app.route('/upload', methods=['get', 'post'])
def upload():
    form= UploadForm() # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/"+filename)
        return redirect(url_for('inicio'))
    return render_template('upload.html', form=form)

@app.route("/calculadora_post", methods=["get", "post"])
def calculadora_post():
    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        operador = request.form.get("operador")
        
        try:
            resultado = eval(num1 + operador + num2)
        except:
            return render_template("error.html", 
                                 error="No puedo realizar la operación")
        
        return render_template("resultado.html", 
                             num1=num1, num2=num2, operador=operador, 
                             resultado=resultado)
    else:
        return render_template("calculadora_post.html")
    
@app.route("/calculadora_post_wtf", methods=["get", "post"])
def calculadora_post_wtf():
    form = formcalculadora(request.form)
    if form.validate_on_submit():
        num1 = form.num1.data
        num2 = form.num2.data
        operador = form.operador.data
        try:
            # Se convierte a string para asegurar la concatenación antes del eval
            resultado = eval(str(num1) + operador + str(num2))
        except:
            return render_template("error.html", 
                                 error="No puedo realizar la operación")
        
        return render_template("resultado.html", 
                             num1=num1, num2=num2, 
                             operador=operador, resultado=resultado)
    else:
        return render_template("calculadora_post_wtf.html", form=form)