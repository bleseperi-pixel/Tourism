# 🌍 Wanderwise — Tourism Package Recommendation System

AI-powered tourism package recommender using Random Forest ML, Flask backend, and HTML/CSS/JS frontend.

---

## 📁 Project Structure

```
tourism_recommender/
├── app.py                   ← Flask backend (main entry point)
├── requirements.txt         ← Python dependencies
├── model/
│   ├── train_model.py       ← ML training script
│   ├── model.pkl            ← Trained Random Forest model
│   ├── encoders.pkl         ← Label encoders
│   └── package_info.pkl     ← Destination metadata
├── templates/
│   └── index.html           ← Frontend HTML
└── static/
    ├── css/style.css        ← Styling
    └── js/main.js           ← Frontend logic
```

---

## ⚙️ Setup & Run

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — (Optional) Retrain the model

```bash
python model/train_model.py
```
> The pre-trained model is already included. Skip this step unless you want to retrain.

### Step 3 — Run Flask server

```bash
python app.py
```

### Step 4 — Open in browser

```
http://localhost:5000
```

---

## 🤖 ML Details

| Item | Value |
|------|-------|
| Algorithm | Random Forest Classifier |
| Library | scikit-learn |
| Input Features | Budget, Duration (days), Climate, Activity, Travel type |
| Output | Top 3 ranked tourism packages |
| Training Samples | 41 samples |
| Destinations | 24 global packages |

---

## 🗺️ Destinations Included

Goa Beach Escape · Manali Snow Trip · Jaipur Heritage Tour · Kerala Backwaters ·
Darjeeling Hills · Varanasi Cultural Tour · Andaman Islands · Shimla Retreat ·
Bali Adventure · Switzerland Alps · Thailand Cultural Tour · Maldives Resort ·
New Zealand Adventure · Paris Getaway · Vietnam Nature Trek · Santorini Retreat ·
Dubai Luxury Escape · Iceland Aurora · Machu Picchu Explorer · Japan Winter Tour ·
Safari Kenya · Bora Bora Luxury · Italy Heritage Tour · Amazon Rainforest Trek

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **ML**: scikit-learn (RandomForestClassifier), pandas, numpy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Fonts**: Google Fonts (Playfair Display + Inter)
