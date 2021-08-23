from flask import session, Blueprint, render_template
from . import socketio
from app.auth import login_required
from app.db import get_db

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    db_messages = db.execute('SELECT * from messages ORDER by id').fetchmany(50)
    return render_template('index.html', messages=db_messages)


@socketio.on('text')
def message_sent(message):
    db = get_db()
    db.execute('INSERT INTO messages (sent_by,message) values (?,?)', (session['username'], message['msg']))
    db.commit()
    socketio.emit('message', {'username': session.get('username'), 'msg': message['msg']}, broadcast=True)
