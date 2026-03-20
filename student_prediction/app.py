from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# ---------------- DATA ----------------
data = {
    "Hours": [1,2,3,4,5,6,7,8],
    "Sleep": [6,7,6,8,7,6,7,8],
    "Previous": [40,50,55,60,65,70,75,80],
    "Score": [35,45,50,65,70,75,85,90]
}

df = pd.DataFrame(data)

X = df[["Hours","Sleep","Previous"]]
y = df["Score"]

model = LinearRegression()
model.fit(X, y)

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    hours = ""
    sleep = ""
    prev = ""

    if request.method == "POST":

        # Predict button
        if "predict" in request.form:
            hours = request.form["hours"]
            sleep = request.form["sleep"]
            prev = request.form["prev"]

            prediction = model.predict([[float(hours), float(sleep), float(prev)]])
            result = round(max(0, min(100, prediction[0])), 2)

        # Clear button
        elif "clear" in request.form:
            return render_template("index.html", result=None, hours="", sleep="", prev="")

    return render_template("index.html", result=result, hours=hours, sleep=sleep, prev=prev)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)