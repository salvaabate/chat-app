from flask import session, Blueprint, render_template
from . import socketio
# from . import login_required
# from app.db import get_db

bp = Blueprint('chat', __name__)


@bp.route('/')
# @login_required
def index():
    return render_template('index.html')


@socketio.on('message_sent')
def message_sent(message):
    print('message received')
    socketio.emit('message', message, broadcast=True)

