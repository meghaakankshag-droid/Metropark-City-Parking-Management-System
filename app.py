"""
Parking Management System - Flask Backend
Metropolitan City Parking Portal — Hyderabad
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import json
import os
import csv
import io
from datetime import datetime
import math

# ─── App Initialization ────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "parking_secret_key_2024"

DATA_FILE = "parking_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return init_data()
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def init_data():
    """
    Seed the database with expanded sub-areas across all 5 zones of Hyderabad.
    Each zone now has multiple real landmark-based parking locations.
    """
    areas = {
        # ── Hitech City ──────────────────────────────────────────────────────
        "Hitech City - Cyber Towers": {
            "id": "hitech_cyber", "zone": "Hitech City",
            "lat": 17.4474, "lng": 78.3762,
            "address": "Cyber Towers, Hitech City, Hyderabad",
            "total_slots": 10,
            "slots": {f"HC{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        "Hitech City - HITEC Hub": {
            "id": "hitech_hub", "zone": "Hitech City",
            "lat": 17.4493, "lng": 78.3801,
            "address": "HITEC Hub, Madhapur, Hyderabad",
            "total_slots": 8,
            "slots": {f"HH{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        "Hitech City - Mindspace": {
            "id": "hitech_mindspace", "zone": "Hitech City",
            "lat": 17.4436, "lng": 78.3799,
            "address": "Mindspace IT Park, Hitech City, Hyderabad",
            "total_slots": 10,
            "slots": {f"HM{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        # ── Banjara Hills ─────────────────────────────────────────────────────
        "Banjara Hills - Road No. 12": {
            "id": "banjara_rd12", "zone": "Banjara Hills",
            "lat": 17.4156, "lng": 78.4347,
            "address": "Road No. 12, Banjara Hills, Hyderabad",
            "total_slots": 12,
            "slots": {f"BR{i:02d}": {"occupied": False, "booking": None} for i in range(1, 13)}
        },
        "Banjara Hills - Peddamma Temple": {
            "id": "banjara_temple", "zone": "Banjara Hills",
            "lat": 17.4263, "lng": 78.4108,
            "address": "Peddamma Temple Rd, Banjara Hills, Hyderabad",
            "total_slots": 8,
            "slots": {f"BT{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        "Banjara Hills - GVK One Mall": {
            "id": "banjara_gvk", "zone": "Banjara Hills",
            "lat": 17.4122, "lng": 78.4476,
            "address": "GVK One Mall, Banjara Hills, Hyderabad",
            "total_slots": 10,
            "slots": {f"BG{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        # ── Secunderabad ──────────────────────────────────────────────────────
        "Secunderabad - Paradise Circle": {
            "id": "secu_paradise", "zone": "Secunderabad",
            "lat": 17.4399, "lng": 78.4983,
            "address": "Paradise Circle, Secunderabad, Hyderabad",
            "total_slots": 10,
            "slots": {f"SP{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        "Secunderabad - Clock Tower": {
            "id": "secu_clock", "zone": "Secunderabad",
            "lat": 17.4368, "lng": 78.5012,
            "address": "Clock Tower, M.G. Road, Secunderabad, Hyderabad",
            "total_slots": 8,
            "slots": {f"SC{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        "Secunderabad - SD Road": {
            "id": "secu_sdroad", "zone": "Secunderabad",
            "lat": 17.4453, "lng": 78.4967,
            "address": "S.D. Road, Secunderabad, Hyderabad",
            "total_slots": 10,
            "slots": {f"SS{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        "Secunderabad - Trimulgherry": {
            "id": "secu_trimul", "zone": "Secunderabad",
            "lat": 17.4630, "lng": 78.5140,
            "address": "Trimulgherry, Secunderabad, Hyderabad",
            "total_slots": 8,
            "slots": {f"ST{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        # ── Gachibowli ────────────────────────────────────────────────────────
        "Gachibowli - DLF Cyber City": {
            "id": "gachi_dlf", "zone": "Gachibowli",
            "lat": 17.4401, "lng": 78.3489,
            "address": "DLF Cyber City, Gachibowli, Hyderabad",
            "total_slots": 10,
            "slots": {f"GD{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        "Gachibowli - University of Hyderabad": {
            "id": "gachi_uoh", "zone": "Gachibowli",
            "lat": 17.4572, "lng": 78.3305,
            "address": "University of Hyderabad Campus, Gachibowli, Hyderabad",
            "total_slots": 8,
            "slots": {f"GU{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        "Gachibowli - Aparna Sarovar": {
            "id": "gachi_aparna", "zone": "Gachibowli",
            "lat": 17.4320, "lng": 78.3620,
            "address": "Aparna Sarovar Zone, Nanakramguda, Gachibowli, Hyderabad",
            "total_slots": 8,
            "slots": {f"GA{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        # ── Madhapur ──────────────────────────────────────────────────────────
        "Madhapur - Film Nagar": {
            "id": "madhapur_film", "zone": "Madhapur",
            "lat": 17.4210, "lng": 78.4000,
            "address": "Film Nagar, Madhapur, Hyderabad",
            "total_slots": 10,
            "slots": {f"MF{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
        "Madhapur - Jubilee Hills Check Post": {
            "id": "madhapur_jubilee", "zone": "Madhapur",
            "lat": 17.4323, "lng": 78.4098,
            "address": "Jubilee Hills Check Post, Madhapur, Hyderabad",
            "total_slots": 8,
            "slots": {f"MJ{i:02d}": {"occupied": False, "booking": None} for i in range(1, 9)}
        },
        "Madhapur - Inorbit Mall": {
            "id": "madhapur_inorbit", "zone": "Madhapur",
            "lat": 17.4380, "lng": 78.3844,
            "address": "Inorbit Mall, Cyberabad, Madhapur, Hyderabad",
            "total_slots": 10,
            "slots": {f"MI{i:02d}": {"occupied": False, "booking": None} for i in range(1, 11)}
        },
    }

    # Demo bookings for realism
    demo_bookings = [
        ("Hitech City - Cyber Towers",        "HC01", "Arjun Sharma",  "TS09AB1234", "2024-01-15 09:00"),
        ("Hitech City - Cyber Towers",        "HC03", "Priya Reddy",   "TS07CD5678", "2024-01-15 10:30"),
        ("Banjara Hills - Road No. 12",       "BR02", "Rahul Kumar",   "AP11EF9012", "2024-01-15 08:15"),
        ("Gachibowli - DLF Cyber City",       "GD05", "Sneha Patel",   "TS01GH3456", "2024-01-15 11:00"),
        ("Secunderabad - Paradise Circle",    "SP01", "Kiran Rao",     "TS05KP7890", "2024-01-15 07:45"),
        ("Madhapur - Film Nagar",             "MF07", "Ananya Iyer",   "TS03MN2345", "2024-01-15 12:00"),
    ]
    for area, slot, name, vehicle, time in demo_bookings:
        areas[area]["slots"][slot]["occupied"] = True
        areas[area]["slots"][slot]["booking"] = {
            "name": name, "vehicle_number": vehicle,
            "area": area, "slot": slot, "time": time,
            "booking_id": f"BK{slot}{vehicle[-4:]}", "phone": ""
        }

    data = {
        "admin": {"username": "admin", "password": "admin123"},
        "areas": areas,
        "bookings": [],
        "history": []
    }
    save_data(data)
    return data


# ─── Known destinations lookup (fuzzy search against this map) ─────────────────
DESTINATIONS = {
    "paradise circle":          {"lat": 17.4399, "lng": 78.4983, "label": "Paradise Circle, Secunderabad"},
    "paradise":                 {"lat": 17.4399, "lng": 78.4983, "label": "Paradise Circle, Secunderabad"},
    "clock tower":              {"lat": 17.4368, "lng": 78.5012, "label": "Clock Tower, M.G. Road, Secunderabad"},
    "mg road":                  {"lat": 17.4368, "lng": 78.5012, "label": "M.G. Road, Secunderabad"},
    "sd road":                  {"lat": 17.4453, "lng": 78.4967, "label": "S.D. Road, Secunderabad"},
    "trimulgherry":             {"lat": 17.4630, "lng": 78.5140, "label": "Trimulgherry, Secunderabad"},
    "cyber towers":             {"lat": 17.4474, "lng": 78.3762, "label": "Cyber Towers, Hitech City"},
    "hitec hub":                {"lat": 17.4493, "lng": 78.3801, "label": "HITEC Hub, Madhapur"},
    "mindspace":                {"lat": 17.4436, "lng": 78.3799, "label": "Mindspace IT Park, Hitech City"},
    "road no 12":               {"lat": 17.4156, "lng": 78.4347, "label": "Road No. 12, Banjara Hills"},
    "road 12":                  {"lat": 17.4156, "lng": 78.4347, "label": "Road No. 12, Banjara Hills"},
    "peddamma temple":          {"lat": 17.4263, "lng": 78.4108, "label": "Peddamma Temple, Banjara Hills"},
    "gvk one":                  {"lat": 17.4122, "lng": 78.4476, "label": "GVK One Mall, Banjara Hills"},
    "gvk mall":                 {"lat": 17.4122, "lng": 78.4476, "label": "GVK One Mall, Banjara Hills"},
    "dlf cyber city":           {"lat": 17.4401, "lng": 78.3489, "label": "DLF Cyber City, Gachibowli"},
    "dlf":                      {"lat": 17.4401, "lng": 78.3489, "label": "DLF Cyber City, Gachibowli"},
    "university of hyderabad":  {"lat": 17.4572, "lng": 78.3305, "label": "University of Hyderabad, Gachibowli"},
    "uoh":                      {"lat": 17.4572, "lng": 78.3305, "label": "University of Hyderabad, Gachibowli"},
    "aparna sarovar":           {"lat": 17.4320, "lng": 78.3620, "label": "Aparna Sarovar, Nanakramguda"},
    "nanakramguda":             {"lat": 17.4320, "lng": 78.3620, "label": "Nanakramguda, Gachibowli"},
    "film nagar":               {"lat": 17.4210, "lng": 78.4000, "label": "Film Nagar, Madhapur"},
    "jubilee hills":            {"lat": 17.4323, "lng": 78.4098, "label": "Jubilee Hills Check Post"},
    "inorbit mall":             {"lat": 17.4380, "lng": 78.3844, "label": "Inorbit Mall, Cyberabad"},
    "inorbit":                  {"lat": 17.4380, "lng": 78.3844, "label": "Inorbit Mall, Cyberabad"},
    "hitech city":              {"lat": 17.4474, "lng": 78.3762, "label": "Hitech City"},
    "banjara hills":            {"lat": 17.4156, "lng": 78.4347, "label": "Banjara Hills"},
    "secunderabad":             {"lat": 17.4399, "lng": 78.4983, "label": "Secunderabad"},
    "gachibowli":               {"lat": 17.4401, "lng": 78.3489, "label": "Gachibowli"},
    "madhapur":                 {"lat": 17.4485, "lng": 78.3908, "label": "Madhapur"},
    "charminar":                {"lat": 17.3616, "lng": 78.4747, "label": "Charminar, Old City"},
    "hussain sagar":            {"lat": 17.4239, "lng": 78.4738, "label": "Hussain Sagar Lake"},
    "tank bund":                {"lat": 17.4239, "lng": 78.4738, "label": "Tank Bund, Hussain Sagar"},
    "nampally":                 {"lat": 17.3850, "lng": 78.4714, "label": "Nampally, Hyderabad"},
    "ameerpet":                 {"lat": 17.4374, "lng": 78.4487, "label": "Ameerpet, Hyderabad"},
    "kukatpally":               {"lat": 17.4849, "lng": 78.4138, "label": "Kukatpally, Hyderabad"},
    "dilsukhnagar":             {"lat": 17.3686, "lng": 78.5247, "label": "Dilsukhnagar, Hyderabad"},
    "lb nagar":                 {"lat": 17.3490, "lng": 78.5520, "label": "L.B. Nagar, Hyderabad"},
    "begumpet":                 {"lat": 17.4435, "lng": 78.4668, "label": "Begumpet, Hyderabad"},
    "somajiguda":               {"lat": 17.4271, "lng": 78.4601, "label": "Somajiguda, Hyderabad"},
    "panjagutta":               {"lat": 17.4253, "lng": 78.4484, "label": "Panjagutta, Hyderabad"},
}


# ─── Utility Functions ──────────────────────────────────────────────────────────

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

def get_area_stats(area_data):
    total    = area_data["total_slots"]
    occupied = sum(1 for s in area_data["slots"].values() if s["occupied"])
    return {"total": total, "occupied": occupied, "available": total - occupied}

def fuzzy_match_destination(query):
    """
    Find the best matching destination for a user's free-text query.
    Strategy: exact match → starts-with → contains → substring of key.
    Returns (key, destination_dict) or (None, None).
    """
    q = query.strip().lower()
    if q in DESTINATIONS:
        return q, DESTINATIONS[q]
    # starts-with
    for key, val in DESTINATIONS.items():
        if key.startswith(q) or q.startswith(key):
            return key, val
    # substring: query contains key
    for key, val in DESTINATIONS.items():
        if key in q:
            return key, val
    # substring: key contains query word-by-word
    q_words = set(q.split())
    best_score, best_key, best_val = 0, None, None
    for key, val in DESTINATIONS.items():
        key_words = set(key.split())
        score = len(q_words & key_words)
        if score > best_score:
            best_score, best_key, best_val = score, key, val
    if best_score > 0:
        return best_key, best_val
    return None, None


# ─── Routes: Common ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "role" in session:
        return redirect(url_for("admin_dashboard" if session["role"] == "admin" else "user_dashboard"))
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ─── Routes: Admin ──────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = load_data()
    body = request.json
    if (body.get("username") == data["admin"]["username"] and
            body.get("password") == data["admin"]["password"]):
        session["role"] = "admin"
        session["username"] = body["username"]
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    return render_template("admin.html")

@app.route("/api/admin/stats")
def admin_stats():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data  = load_data()
    stats = {}
    for area_name, area in data["areas"].items():
        stats[area_name] = get_area_stats(area)
    return jsonify(stats)

@app.route("/api/admin/all_bookings")
def admin_all_bookings():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data     = load_data()
    occupied = []
    for area_name, area in data["areas"].items():
        for slot_id, slot in area["slots"].items():
            if slot["occupied"] and slot["booking"]:
                occupied.append({"area": area_name, "slot": slot_id, **slot["booking"]})
    return jsonify(occupied)

@app.route("/api/admin/history")
def admin_history():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data = load_data()
    return jsonify(data.get("history", []))

@app.route("/api/admin/download_csv")
def download_csv():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data   = load_data()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Booking ID", "Zone", "Area", "Slot Number", "Driver Name",
                     "Vehicle Number", "Booking Time", "Vacated Time", "Status"])
    for area_name, area in data["areas"].items():
        for slot_id, slot in area["slots"].items():
            if slot["occupied"] and slot["booking"]:
                b = slot["booking"]
                writer.writerow([
                    b.get("booking_id", ""), area.get("zone", area_name), area_name,
                    slot_id, b.get("name", ""), b.get("vehicle_number", ""),
                    b.get("time", ""), "", "Active"
                ])
    for entry in data.get("history", []):
        writer.writerow([
            entry.get("booking_id", ""), "", entry.get("area", ""),
            entry.get("slot", ""), entry.get("name", ""),
            entry.get("vehicle_number", ""), entry.get("time", ""),
            entry.get("vacated_time", ""), "Released"
        ])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    )

@app.route("/api/admin/release", methods=["POST"])
def admin_release_slot():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    body = request.json
    data = load_data()
    area = data["areas"].get(body["area"])
    if not area:
        return jsonify({"success": False, "message": "Area not found"}), 404
    slot = area["slots"].get(body["slot"])
    if not slot:
        return jsonify({"success": False, "message": "Slot not found"}), 404
    if slot["booking"]:
        history_entry = {**slot["booking"], "vacated_time": datetime.now().strftime("%Y-%m-%d %H:%M")}
        data.setdefault("history", []).append(history_entry)
    slot["occupied"] = False
    slot["booking"]  = None
    save_data(data)
    return jsonify({"success": True})

@app.route("/api/admin/add_slots", methods=["POST"])
def add_slots():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    body      = request.json
    area_name = body.get("area")
    count     = int(body.get("count", 1))
    data      = load_data()
    area      = data["areas"].get(area_name)
    if not area:
        return jsonify({"success": False, "message": "Area not found"}), 404
    existing_keys = list(area["slots"].keys())
    prefix = existing_keys[0][:-2] if existing_keys else area_name[0].upper()
    nums = []
    for k in existing_keys:
        try: nums.append(int(k[len(prefix):]))
        except: pass
    next_num = max(nums) + 1 if nums else 1
    added = []
    for i in range(count):
        new_id = f"{prefix}{next_num + i:02d}"
        area["slots"][new_id] = {"occupied": False, "booking": None}
        added.append(new_id)
    area["total_slots"] = len(area["slots"])
    save_data(data)
    return jsonify({"success": True, "added": added, "total_slots": area["total_slots"]})

@app.route("/api/admin/remove_slot", methods=["POST"])
def remove_slot():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    body      = request.json
    area_name = body.get("area")
    slot_id   = body.get("slot")
    data      = load_data()
    area      = data["areas"].get(area_name)
    if not area:
        return jsonify({"success": False, "message": "Area not found"}), 404
    slot = area["slots"].get(slot_id)
    if not slot:
        return jsonify({"success": False, "message": "Slot not found"}), 404
    if slot["occupied"]:
        return jsonify({"success": False, "message": "Cannot remove an occupied slot"}), 409
    del area["slots"][slot_id]
    area["total_slots"] = len(area["slots"])
    save_data(data)
    return jsonify({"success": True, "total_slots": area["total_slots"]})


# ─── Routes: User ───────────────────────────────────────────────────────────────

@app.route("/user/dashboard")
def user_dashboard():
    return render_template("user.html")

@app.route("/api/areas")
def get_areas():
    """Return all parking areas with live slot availability counts."""
    data       = load_data()
    areas_info = []
    for name, area in data["areas"].items():
        stats = get_area_stats(area)
        areas_info.append({
            "name":      name,
            "id":        area["id"],
            "zone":      area.get("zone", name),
            "address":   area["address"],
            "lat":       area["lat"],
            "lng":       area["lng"],
            "total":     stats["total"],
            "occupied":  stats["occupied"],
            "available": stats["available"]
        })
    return jsonify(areas_info)

@app.route("/api/slots/<area_name>")
def get_slots(area_name):
    data = load_data()
    area = data["areas"].get(area_name)
    if not area:
        return jsonify({"error": "Area not found"}), 404
    slots = []
    for slot_id, slot in area["slots"].items():
        slots.append({
            "id":       slot_id,
            "occupied": slot["occupied"],
            "booked_by": slot["booking"]["name"][:3] + "***" if slot["booking"] else None
        })
    return jsonify({"area": area_name, "slots": slots})

@app.route("/api/nearest", methods=["POST"])
def nearest_parking():
    """Find parking areas sorted by distance from given GPS coordinates."""
    body     = request.json
    user_lat = float(body.get("lat", 17.385))
    user_lng = float(body.get("lng", 78.4867))
    data     = load_data()
    results  = []
    for name, area in data["areas"].items():
        stats = get_area_stats(area)
        dist  = haversine_distance(user_lat, user_lng, area["lat"], area["lng"])
        results.append({
            "name":        name,
            "id":          area["id"],
            "zone":        area.get("zone", name),
            "address":     area["address"],
            "distance_km": round(dist, 2),
            "available":   stats["available"],
            "total":       stats["total"]
        })
    results.sort(key=lambda x: x["distance_km"])
    return jsonify(results)


@app.route("/api/search_destination", methods=["POST"])
def search_destination():
    """
    Accept a free-text destination name, resolve it to GPS coordinates
    using the known-landmarks lookup (with fuzzy matching), then return
    all parking areas sorted by distance from that destination.

    Request body: { "destination": "Paradise Circle" }
    Response:     { "destination_label": "...", "results": [...] }
    """
    body        = request.json
    query       = body.get("destination", "").strip()
    if not query:
        return jsonify({"error": "Please provide a destination"}), 400

    matched_key, dest = fuzzy_match_destination(query)
    if dest is None:
        # Fall back to Hyderabad city centre
        return jsonify({
            "error":   "destination_not_found",
            "message": f"Could not recognise '{query}'. Try landmarks like 'Paradise Circle', 'DLF Cyber City', 'Film Nagar', etc.",
            "suggestions": list(DESTINATIONS.keys())[:20]
        }), 404

    dest_lat = dest["lat"]
    dest_lng = dest["lng"]
    data     = load_data()
    results  = []
    for name, area in data["areas"].items():
        stats = get_area_stats(area)
        dist  = haversine_distance(dest_lat, dest_lng, area["lat"], area["lng"])
        results.append({
            "name":        name,
            "id":          area["id"],
            "zone":        area.get("zone", name),
            "address":     area["address"],
            "distance_km": round(dist, 2),
            "available":   stats["available"],
            "total":       stats["total"],
            "lat":         area["lat"],
            "lng":         area["lng"]
        })
    results.sort(key=lambda x: x["distance_km"])
    return jsonify({
        "destination_label": dest["label"],
        "dest_lat":          dest_lat,
        "dest_lng":          dest_lng,
        "results":           results
    })


@app.route("/api/destinations/suggestions")
def destination_suggestions():
    """Return all known destination names for autocomplete."""
    return jsonify(sorted(DESTINATIONS.keys()))


@app.route("/api/book", methods=["POST"])
def book_slot():
    body     = request.json
    required = ["name", "vehicle_number", "area", "slot"]
    for field in required:
        if not body.get(field):
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400
    data = load_data()
    area = data["areas"].get(body["area"])
    if not area:
        return jsonify({"success": False, "message": "Area not found"}), 404
    slot = area["slots"].get(body["slot"])
    if not slot:
        return jsonify({"success": False, "message": "Slot not found"}), 404
    if slot["occupied"]:
        return jsonify({"success": False, "message": "Slot already occupied"}), 409
    booking_id = f"BK{body['slot']}{body['vehicle_number'][-4:].upper()}"
    booking = {
        "booking_id":     booking_id,
        "name":           body["name"],
        "vehicle_number": body["vehicle_number"].upper(),
        "area":           body["area"],
        "slot":           body["slot"],
        "time":           datetime.now().strftime("%Y-%m-%d %H:%M"),
        "phone":          body.get("phone", "")
    }
    slot["occupied"] = True
    slot["booking"]  = booking
    data["bookings"].append(booking)
    save_data(data)
    return jsonify({"success": True, "booking": booking})

@app.route("/api/release", methods=["POST"])
def release_by_user():
    body = request.json
    data = load_data()
    area = data["areas"].get(body.get("area"))
    if not area:
        return jsonify({"success": False, "message": "Area not found"}), 404
    slot = area["slots"].get(body.get("slot"))
    if not slot or not slot["occupied"]:
        return jsonify({"success": False, "message": "Slot not found or already free"}), 404
    if slot["booking"]["vehicle_number"].upper() != body.get("vehicle_number", "").upper():
        return jsonify({"success": False, "message": "Vehicle number mismatch"}), 403
    history_entry = {**slot["booking"], "vacated_time": datetime.now().strftime("%Y-%m-%d %H:%M")}
    data.setdefault("history", []).append(history_entry)
    slot["occupied"] = False
    slot["booking"]  = None
    save_data(data)
    return jsonify({"success": True})


# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        init_data()
        print("✅ Database initialised with expanded sub-area demo data")
    print("🚗 MetroPark running at http://localhost:5000")
    app.run(debug=True, port=5000)
