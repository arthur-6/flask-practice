from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # passo a função Flask com o nome do arquivo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # //// absolute path | /// relative path
db = SQLAlchemy(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # função Column para definir uma coluna, passando o tipo de dado de parâmetros
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id # printar uma Task postada

@app.route('/', methods=['POST', 'GET']) # rota de requisição, com os metodos POST e GET pela API
def index():
    if request.method == 'POST': # caso o método de requisição seja POST
        task_content = request.form['content'] # defino uma variável recebendo o form de id 'content' presente no index.html
        new_task = Todo(content=task_content) # crio uma instância da classe Todo (database) passando o Model como o conteúdo da variável

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Erro ao adicionar tarefa.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # pego todas os registros do database e ordeno por data criada
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>') # rota de requisição com o método DELETE
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # caso não consiga dar o get dá 404

    try:
        db.session.delete(task_to_delete) 
        db.session.commit()
        return redirect('/')
    except:
        return 'Erro ao deletar tarefa'

@app.route('/update/<int:id>', methods=['GET', 'POST']) # rota de requisição com o método UPDATE
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        
        try:
            db.session.commit() # passo apenas o commit pq nao estou adicionando um novo, apenas alterando
            return redirect('/')
        except:
            return 'Erro ao editar tarefa'
    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)