import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle, os

data = {
    "budget": [
        "Low","Low","Low","Low","Low","Low","Low","Low",
        "Medium","Medium","Medium","Medium","Medium","Medium","Medium","Medium",
        "High","High","High","High","High","High","High","High",
        "Low","Medium","High","Low","Medium","High","Low","Medium","High",
        "Low","Medium","High","Low","Medium","High","Low","Medium","High",
    ],
    "duration_days": [
        2,3,1,4,2,3,1,5,
        5,7,4,6,5,7,3,6,
        10,14,7,12,10,14,7,12,
        3,6,9,4,8,11,2,5,13,
        1,7,10,3,6,14,4,8,12,
    ],
    "climate_preference": [
        "Tropical","Cold","Tropical","Any","Cold","Any","Tropical","Cold",
        "Tropical","Cold","Any","Tropical","Cold","Any","Tropical","Cold",
        "Any","Cold","Tropical","Cold","Any","Tropical","Cold","Any",
        "Tropical","Cold","Any","Cold","Tropical","Any","Tropical","Cold","Any",
        "Any","Tropical","Cold","Tropical","Any","Cold","Cold","Any","Tropical",
    ],
    "activity_preference": [
        "Adventure","Relaxation","Culture","Adventure","Relaxation","Culture","Nature","Relaxation",
        "Adventure","Relaxation","Culture","Nature","Adventure","Culture","Nature","Relaxation",
        "Adventure","Relaxation","Culture","Nature","Adventure","Relaxation","Culture","Nature",
        "Culture","Adventure","Relaxation","Nature","Culture","Adventure","Relaxation","Nature","Culture",
        "Adventure","Relaxation","Nature","Culture","Adventure","Relaxation","Nature","Culture","Adventure",
    ],
    "travel_with": [
        "Solo","Couple","Family","Solo","Couple","Family","Solo","Couple",
        "Couple","Family","Solo","Couple","Family","Solo","Couple","Family",
        "Family","Couple","Solo","Family","Solo","Couple","Family","Solo",
        "Solo","Family","Couple","Solo","Couple","Family","Couple","Solo","Family",
        "Family","Solo","Couple","Family","Solo","Couple","Solo","Family","Couple",
    ],
    "package": [
        "Goa Beach Escape","Manali Snow Trip","Jaipur Heritage Tour","Kerala Backwaters",
        "Darjeeling Hills","Varanasi Cultural Tour","Andaman Islands","Shimla Retreat",
        "Bali Adventure","Switzerland Alps","Thailand Cultural Tour","Maldives Resort",
        "New Zealand Adventure","Paris Getaway","Vietnam Nature Trek","Santorini Retreat",
        "Dubai Luxury Escape","Iceland Aurora","Machu Picchu Explorer","Japan Winter Tour",
        "Safari Kenya","Bora Bora Luxury","Italy Heritage Tour","Amazon Rainforest Trek",
        "Jaipur Heritage Tour","Manali Snow Trip","Santorini Retreat","Vietnam Nature Trek",
        "Thailand Cultural Tour","Dubai Luxury Escape","Goa Beach Escape","Shimla Retreat","Italy Heritage Tour",
        "Andaman Islands","Kerala Backwaters","Iceland Aurora","Varanasi Cultural Tour","Bali Adventure",
        "Maldives Resort","Amazon Rainforest Trek","Paris Getaway","Machu Picchu Explorer",
    ],
}

df = pd.DataFrame(data)

encoders = {}
for col in ["budget","climate_preference","activity_preference","travel_with"]:
    le = LabelEncoder()
    df[col+"_enc"] = le.fit_transform(df[col])
    encoders[col] = le

target_le = LabelEncoder()
df["package_enc"] = target_le.fit_transform(df["package"])
encoders["package"] = target_le

features = ["budget_enc","duration_days","climate_preference_enc","activity_preference_enc","travel_with_enc"]
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(df[features], df["package_enc"])

out = os.path.dirname(__file__)
with open(os.path.join(out,"model.pkl"),"wb") as f: pickle.dump(model, f)
with open(os.path.join(out,"encoders.pkl"),"wb") as f: pickle.dump(encoders, f)

package_info = {
    "Goa Beach Escape":       {"emoji":"🏖️","desc":"Sun, sand & seafood on India's vibrant coast.","highlights":["Beach parties","Water sports","Fish thali"],"days":"3-5","best":"Oct–Mar"},
    "Manali Snow Trip":       {"emoji":"❄️","desc":"Snow-capped Himalayas with thrilling adventures.","highlights":["Skiing","Rohtang Pass","Solang Valley"],"days":"4-6","best":"Dec–Feb"},
    "Jaipur Heritage Tour":   {"emoji":"🏰","desc":"The Pink City's royal forts and vibrant bazaars.","highlights":["Amber Fort","Hawa Mahal","Local crafts"],"days":"3-4","best":"Oct–Mar"},
    "Kerala Backwaters":      {"emoji":"🛶","desc":"Serene houseboat cruise through lush green canals.","highlights":["Houseboat stay","Ayurveda spa","Spice gardens"],"days":"4-6","best":"Sep–Mar"},
    "Darjeeling Hills":       {"emoji":"🍵","desc":"Tea estates, toy train & breathtaking Himalayan views.","highlights":["Tea tasting","Tiger Hill sunrise","Toy train ride"],"days":"3-5","best":"Mar–May"},
    "Varanasi Cultural Tour": {"emoji":"🪔","desc":"Spiritual ghats and ancient temple city on the Ganges.","highlights":["Ganga Aarti","Boat ride at dawn","Silk shopping"],"days":"2-3","best":"Oct–Mar"},
    "Andaman Islands":        {"emoji":"🌊","desc":"Crystal waters and untouched coral reefs.","highlights":["Scuba diving","Cellular Jail","Beach camping"],"days":"5-7","best":"Oct–May"},
    "Shimla Retreat":         {"emoji":"🏔️","desc":"Colonial charm meets Himalayan cool breezes.","highlights":["Mall Road","Jakhu Temple","Pine forests"],"days":"3-5","best":"Mar–Jun"},
    "Bali Adventure":         {"emoji":"🌴","desc":"Island of gods — temples, rice terraces & surf.","highlights":["Ubud temples","Surfing","Rice terrace trek"],"days":"6-8","best":"Apr–Oct"},
    "Switzerland Alps":       {"emoji":"🗻","desc":"Alpine luxury with world-class skiing and scenery.","highlights":["Jungfrau peak","Swiss chocolate","Mountain railways"],"days":"7-10","best":"Dec–Mar"},
    "Thailand Cultural Tour": {"emoji":"🐘","desc":"Temples, street food & elephant sanctuaries.","highlights":["Chiang Mai temples","Street food tour","Thai massage"],"days":"5-7","best":"Nov–Apr"},
    "Maldives Resort":        {"emoji":"🤿","desc":"Overwater bungalows in turquoise paradise.","highlights":["Overwater villa","Snorkelling","Sunset cruise"],"days":"5-7","best":"Nov–Apr"},
    "New Zealand Adventure":  {"emoji":"🎿","desc":"Bungee, skydive & Lord of the Rings landscapes.","highlights":["Bungee jumping","Skydiving","Milford Sound"],"days":"10-14","best":"Dec–Feb"},
    "Paris Getaway":          {"emoji":"🗼","desc":"Love, art and croissants in the City of Light.","highlights":["Eiffel Tower","Louvre Museum","Seine cruise"],"days":"5-7","best":"Apr–Jun"},
    "Vietnam Nature Trek":    {"emoji":"🌿","desc":"Karst mountains, rice paddies & floating villages.","highlights":["Ha Long Bay cruise","Sapa trek","Hoi An lanterns"],"days":"7-10","best":"Feb–Apr"},
    "Santorini Retreat":      {"emoji":"🌅","desc":"White-washed cliffs and legendary Mediterranean sunsets.","highlights":["Caldera view","Wine tasting","Oia village walk"],"days":"5-7","best":"Apr–Oct"},
    "Dubai Luxury Escape":    {"emoji":"🏙️","desc":"Ultra-modern skyline meets golden desert adventures.","highlights":["Burj Khalifa","Desert safari","Dubai Mall"],"days":"4-6","best":"Nov–Mar"},
    "Iceland Aurora":         {"emoji":"🌌","desc":"Northern lights, geysers and volcanic landscapes.","highlights":["Aurora borealis","Blue Lagoon","Geyser tour"],"days":"7-10","best":"Sep–Mar"},
    "Machu Picchu Explorer":  {"emoji":"🏛️","desc":"Lost Incan citadel high in the Peruvian Andes.","highlights":["Inca Trail hike","Huayna Picchu","Sacred Valley"],"days":"8-12","best":"May–Oct"},
    "Japan Winter Tour":      {"emoji":"⛩️","desc":"Snow monkeys, ski resorts and ancient Zen shrines.","highlights":["Snow monkey park","Shinkansen ride","Kyoto temples"],"days":"10-14","best":"Dec–Feb"},
    "Safari Kenya":           {"emoji":"🦁","desc":"Big Five in their natural savannah habitat.","highlights":["Masai Mara game drive","Hot air balloon","Maasai village"],"days":"7-10","best":"Jul–Oct"},
    "Bora Bora Luxury":       {"emoji":"💎","desc":"Pearl of the Pacific — ultimate island luxury.","highlights":["Private lagoon villa","Pearl farm visit","Coral reef snorkelling"],"days":"7-10","best":"May–Oct"},
    "Italy Heritage Tour":    {"emoji":"🍝","desc":"Roman ruins, Renaissance art and pasta perfection.","highlights":["Colosseum tour","Vatican Museums","Amalfi Coast drive"],"days":"10-14","best":"Apr–Jun"},
    "Amazon Rainforest Trek": {"emoji":"🐍","desc":"Deepest jungle adventure on Earth.","highlights":["Wildlife night walk","Canopy walkway","Amazon river cruise"],"days":"7-10","best":"Jun–Nov"},
}

with open(os.path.join(out,"package_info.pkl"),"wb") as f: pickle.dump(package_info, f)
print("✅ Model, encoders & package_info saved.")
