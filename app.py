from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__, static_folder="static")

@app.route('/')
def inicio():
    try:
        with open ("posts.json", "r") as archivo:
            posts = json.load(archivo)
            return render_template('index.html', posts = posts)
    except FileNotFoundError:
        return render_template('index.html', posts = [])  
    except json.JSONDecodeError:
        return render_template('index.html', posts = [])    
@app.route('/crear')
def crear():
    return render_template('crear.html')
@app.route ('/guardar', methods = ['POST'])
def guardar():
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    try:
        with open("posts.json", "r") as archivo:
            posts = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []
    if len(posts) == 0:
        id = 1
    else:
        id = posts[-1]["id"] +1
    post_nuevo = {
        "titulo" : titulo,
        "contenido" : contenido,
        "id": id
        }
    posts.append(post_nuevo)
    with open ("posts.json", "w") as archivo:
        json.dump(posts, archivo, indent = 2)
    return redirect('/')
@app.route('/eliminar/<int:id>')
def eliminar_post(id):
    id = int(id)
    with open("posts.json", "r") as archivo:
        posts = json.load(archivo)
    for post in posts:
        if id == post['id']:
            posts.remove(post)
            break
    with open("posts.json", "w") as archivo:
        json.dump(posts, archivo, indent=2)
    return redirect('/')
@app.route('/editar/<int:id>', methods=['GET'])
def editar_post(id):
    with open("posts.json", "r") as archivo:
        posts = json.load(archivo)
    post_encontrado = []
    for post in posts:
        if id == post['id']:
            post_encontrado = post
            break
    return render_template('editar.html', post = post_encontrado)
@app.route('/editar/<int:id>', methods = ['POST'])
def editar_post_post(id):
    with open("posts.json", "r") as archivo:
        posts = json.load(archivo)
    for post in posts:
        if post['id'] == id:
            post_encontrado = post
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    post_encontrado["titulo"] = request.form['titulo']
    post_encontrado["contenido"] = request.form['contenido']
    with open("posts.json", "w") as archivo:
        json.dump(posts, archivo, indent=2)
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

