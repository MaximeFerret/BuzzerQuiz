pip install flask-socketio
pip install eventlet

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete'
socketio = SocketIO(app, cors_allowed_origins="*")  # 允许跨域

@app.route('/')
def index():
    return render_template('index.html')  # 前端页面

# 当客户端连接时触发
@socketio.on('connect')
def handle_connect():
    print('🔗 Un utilisateur est connecté.')
    emit('server_message', {'msg': 'Bienvenue sur le quiz!'})

# 加入房间
@socketio.on('join_room')
def handle_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    emit('server_message', {'msg': f"{username} a rejoint la salle {room}"}, to=room)

# 发送答题倒计时
@socketio.on('start_countdown')
def start_countdown(data):
    room = data['room']
    time_left = data.get('time', 30)  # 默认30秒
    while time_left > 0:
        emit('countdown', {'time_left': time_left}, to=room)
        socketio.sleep(1)
        time_left -= 1
    emit('countdown_end', {'msg': 'Temps écoulé!'}, to=room)

# 处理用户提交答案
@socketio.on('submit_answer')
def handle_answer(data):
    username = data['username']
    answer = data['answer']
    room = data['room']
    # 可以在此处验证答案正确性
    emit('server_message', {'msg': f"{username} a répondu : {answer}"}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)