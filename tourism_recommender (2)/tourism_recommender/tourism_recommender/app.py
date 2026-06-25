from flask import Flask, render_template, request, jsonify
import pickle, os, numpy as np

app = Flask(__name__)

BASE = os.path.join(os.path.dirname(__file__), "model")
with open(os.path.join(BASE,"model.pkl"),"rb") as f:      model        = pickle.load(f)
with open(os.path.join(BASE,"encoders.pkl"),"rb") as f:   encoders     = pickle.load(f)
with open(os.path.join(BASE,"package_info.pkl"),"rb") as f: package_info = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    d = request.get_json()
    try:
        budget_enc   = encoders["budget"].transform([d["budget"]])[0]
        climate_enc  = encoders["climate_preference"].transform([d["climate_preference"]])[0]
        activity_enc = encoders["activity_preference"].transform([d["activity_preference"]])[0]
        travel_enc   = encoders["travel_with"].transform([d["travel_with"]])[0]
        duration     = int(d["duration_days"])
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

    X = np.array([[budget_enc, duration, climate_enc, activity_enc, travel_enc]])
    proba = model.predict_proba(X)[0]
    top3  = np.argsort(proba)[::-1][:3]
    names = encoders["package"].inverse_transform(top3)

    results = []
    for name, idx in zip(names, top3):
        info = package_info.get(name, {})
        results.append({
            "name":       name,
            "confidence": round(float(proba[idx]) * 100, 1),
            "emoji":      info.get("emoji","✈️"),
            "desc":       info.get("desc",""),
            "highlights": info.get("highlights",[]),
            "days":       info.get("days",""),
            "best":       info.get("best",""),
        })
    return jsonify({"recommendations": results})


if __name__ == "__main__":
    app.run(debug=True)
