import flask


app = flask.Flask(__name__)


@app.route("/home",methods = ['GET'])
def home():
    return {"author":"Ajinkya patil" , "Env": "devlopment", "version":"1.0.0"}

if __name__ == "__main__":
    app.run(debug = True)