from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

#Configuração de conexão PostgreSQL
engine = create_engine("postgresql://admin:123@localhost:5432/PIUNIVESP2022")
db = scoped_session(sessionmaker(bind=engine))
app.secret_key = '12345678'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='PIUNIVESP2022',
                            user='admin',
                            password='123')
    return conn

#Função para encontrar ID de postagens individuais
def get_post(post_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM "PIUNIVESP2022.public.posts" WHERE post_id = id').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


#Página inicial
@app.route('/')
def index():
    exibe = db.execute('SELECT * FROM retornos').fetchall()
    return render_template('index.html', Res=exibe)


#Página tipos de contato
@app.route('/db')
def tipo():
    exibe = db.execute('SELECT * FROM tipos').fetchall()
    return render_template('db.html', tipos=exibe)


#Página de informação do grupo
@app.route('/sobre')
def sobreNos():
    return render_template('sobre.html')


#Página de aprofundamento do tema
@app.route('/aprofundando')
def aprofundando():
    return render_template('aprofundando.html')


#Retorno individual de postagens
@app.route('/<int:id>')
def post():
    post = get_post()
    return render_template('post.html', post=post)


#Criação de postagens
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        contato = request.form.get('contato')
        bairro = request.form.get('bairro')
        db.execute("INSERT INTO posts (contato, bairro) VALUES (:contato, :bairro)" , {"contato": contato, "bairro": bairro})
        db.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

