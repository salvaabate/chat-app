import datetime
import re
import threading

from flask import session, Blueprint, render_template
from . import socketio
from chatapp.auth import login_required
from chatapp.db import get_db
from chatapp.bot_handler import handle_bot_message

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    db_messages = db.execute('SELECT * from messages ORDER by id').fetchmany(50)
    return render_template('index.html', messages=db_messages)


@socketio.on('text')
def message_sent(message_received):
    message = message_received['msg']
    regex = '^/stock='
    if re.search(regex, message) is not None:
        handle_bot_messages(message)
        return

    db = get_db()
    db.execute('INSERT INTO messages (sent_by,message) values (?,?)', (session['username'], message))
    db.commit()
    dt = datetime.datetime.now().strftime('%m-%d-%Y %H:%M')
    socketio.emit('message', {'sent': dt, 'username': session.get('username'), 'msg': message}, broadcast=True)


def handle_bot_messages(message):
    stock_code = message.split('=')[1]
    bot_thread = threading.Thread(target=handle_bot_message, args=(stock_code,))
    bot_thread.start()
