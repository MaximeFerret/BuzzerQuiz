from flask import request
from flask_login import current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from ..business_object.quiz import Quiz, Question
from ..business_object.db import db


socketio = SocketIO()

# Stockage des joueurs et de leurs scores en mémoire
players = {}
active_quizzes = {}


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']

    # Vérifier si le code de quiz existe
    quiz = Quiz.query.filter_by(code=room).first()
    if not quiz:
        emit('error', {'msg': 'Code de quiz invalide'})
        return

    # Vérifier si le joueur n'est pas déjà dans la partie
    if username in players and players[username]['room'] == room:
        emit('error', {'msg': 'Ce pseudo est déjà utilisé dans cette partie'})
        return

    join_room(room)
    players[username] = {'score': 0, 'room': room}

    # Émettre l'événement à tous les clients dans la salle
    emit('player_joined', {'username': username}, room=room)
    emit('status', {'msg': f'{username} a rejoint la partie!'}, room=room)


@socketio.on('buzz')
def on_buzz(data):
    username = data['username']
    room = data['room']

    # Émettre l'événement de buzz à l'hôte
    emit('buzz', {'username': username}, room=room)


@socketio.on('correct_answer')
def on_correct_answer(data):
    username = data['username']
    room = data['room']

    # Vérifier si le joueur existe et mettre à jour son score
    if username in players and 'score' in players[username]:
        players[username]['score'] += 100
        print(f"Score updated for {username}: {players[username]['score']}")

        # Émettre le nouveau score à tous les joueurs de la salle
        emit('correct_answer', {
            'username': username,
            'score': players[username]['score']
        }, room=room, broadcast=True)


@socketio.on('wrong_answer')
def on_wrong_answer(data):
    username = data['username']
    room = data['room']

    emit('wrong_answer', {'username': username}, room=room)


@socketio.on('can_buzz')
def on_can_buzz(data):
    room = data['room']
    emit('can_buzz', {}, room=room)


@socketio.on('start_game')
def on_start_game(data):
    room = data['room']
    quiz = Quiz.query.filter_by(code=room).first()

    if not quiz or quiz.creator_id != current_user.id:
        emit('error', {'msg': 'Vous n\'êtes pas autorisé à démarrer ce quiz'})
        return

    # Réinitialiser les scores pour tous les joueurs dans cette salle
    for username, player_data in list(players.items()):
        if player_data['room'] == room:
            players[username] = {'score': 0, 'room': room}
            print(f"Score reset for {username}")  # Log pour déboguer

    quiz.is_active = True
    db.session.commit()

    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    active_quizzes[room] = {
        'questions': questions,
        'current_question': 0
    }

    # Notifier tous les joueurs que la partie commence
    emit('game_started', {'question': {
        'question': questions[0].question_text,
        'options': [
            questions[0].option1,
            questions[0].option2,
            questions[0].option3,
            questions[0].option4
        ],
        'correct': questions[0].correct_answer
    }}, room=room)


@socketio.on('next_question')
def on_next_question(data):
    room = data['room']
    quiz_data = active_quizzes.get(room)

    if not quiz_data:
        emit('error', {'msg': 'Quiz non trouvé'})
        return

    quiz_data['current_question'] += 1
    if quiz_data['current_question'] < len(quiz_data['questions']):
        current_question = quiz_data['questions'][quiz_data[
            'current_question']]
        emit('new_question', {'question': {
            'question': current_question.question_text,
            'options': [
                current_question.option1,
                current_question.option2,
                current_question.option3,
                current_question.option4
            ],
            'correct': current_question.correct_answer
        }}, room=room)
    else:
        quiz = Quiz.query.filter_by(code=room).first()
        quiz.is_active = False
        db.session.commit()
        emit('game_over', {'scores': players}, room=room)
        del active_quizzes[room]


@socketio.on('game_over')
def on_game_over(data):
    room = data['room']
    scores = data['scores']

    # Désactiver le quiz dans la base de données
    if quiz := Quiz.query.filter_by(code=room).first():
        quiz.is_active = False
        db.session.commit()

    # Nettoyer les données de la partie
    if room in active_quizzes:
        del active_quizzes[room]

    # Émettre l'événement de fin de partie à tous les joueurs dans la salle
    emit('game_over', {'scores': scores}, room=room)


@socketio.on('host_join')
def on_host_join(data):
    room = data['room']
    join_room(room)

    # Envoyer la liste actuelle des joueurs à l'hôte
    room_players = [username for username,
                    data in players.items() if data['room'] == room]
    for player in room_players:
        emit('player_joined', {'username': player})
        emit('status', {'msg': f'{player} est dans la partie'})


@socketio.on('kick_player')
def on_kick_player(data):
    room = data['room']
    username = data['username']

    # Émettre un événement au joueur pour qu'il soit redirigé
    emit('kicked', {}, room=username)

    # Retirer le joueur de la room
    for sid in request.sid:
        if sid in room and room[sid] == username:
            leave_room(room, sid=sid)
            emit('player_left', {'username': username}, room=room)
            break
