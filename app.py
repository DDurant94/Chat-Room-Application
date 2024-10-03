from web_socket_server import WebSocketServer, socketio, app
from flask import render_template,request

app = WebSocketServer().create_app()
message_storage = {}
connected_users = {}
  
@socketio.on('message')
def handle_message(data):
  user = data['user']
  message = data['message']
  print(f'Received message from {user}: {message}')
  
  if user not in message_storage:
    message_storage[user] = []
  message_storage[user].append(message)
    
  socketio.emit('message', data)
  
@socketio.on('get_user_messages')
def handle_get_user_messages(data):
  user = data['user']
  user_messages = message_storage.get(user, [])
  socketio.emit('get_user_messages', {'user': user, 'messages': user_messages})
  
@socketio.on('join')
def handle_join(data):
    user = data['user']
    sid = request.sid
    connected_users[sid] = user
    print(f'{user} has joined the chat')
    socketio.emit('join', {'user': user})
  
@socketio.on('connect')
def handle_connect():
  print('Client connected')
  
@socketio.on('disconnect')
def handle_disconnect():
  sid = request.sid
  user = connected_users.pop(sid)
  print(f'{user} has left the chat')
  print('Client disconnected')
  socketio.emit('leave', {'user': user})

@app.route('/')
def index():
  return render_template('JoinRoom.html')
  
if __name__ == '__main__':
  socketio.run(app)