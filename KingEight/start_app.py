from flask import Flask,request,jsonify,render_template
from serv import content
from serv import get_anything
from serv import user_option
from serv import devices
from serv import friend
from serv import chat
app = Flask(__name__)

app.register_blueprint(content.content_bp)
app.register_blueprint(get_anything.get_any)
app.register_blueprint(user_option.user_pb)
app.register_blueprint(devices.dev)
app.register_blueprint(friend.fri)
app.register_blueprint(chat.ch)






@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run("0.0.0.0",9527,debug=True)