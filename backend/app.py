from flask import Flask,render_template,request
import os
from ai.predictor import predict_claim_priority

app = Flask(__name__)

UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload",methods=["POST"])
def upload():

    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER,file.filename)

    file.save(filepath)

    df = predict_claim_priority(filepath)

    results = df.head(50).to_dict(orient="records")

    return render_template("results.html",results=results)


if __name__ == "__main__":
    app.run(debug=True)
