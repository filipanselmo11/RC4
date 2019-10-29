from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessao():
    return render_template('sessao.html')

def msgRecebida(methods=['GET', 'POST']):
    print('Mensagem recebida')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('Meu envento recebido: ' + str(json))
    socketio.emit('my response', json, callback=msgRecebida)
   

if __name__ == '__main__':
    socketio.run(app, debug=True)

 