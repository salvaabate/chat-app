from chatapp import create_app, socketio

app = create_app(test_config=None)

app.app_context().push()

if __name__ == '__main__':
    socketio.run(app)
