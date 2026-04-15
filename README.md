# 🚗 MetroPark — Metropolitan City Parking Management System

A full-stack parking management system built with **Python Flask** + **Vanilla JS**.

---

## 📁 Project Structure

```
parking_system/
├── app.py               ← Flask backend (all API routes)
├── parking_data.json    ← Auto-generated flat-file database
├── requirements.txt     ← Python dependencies
└── templates/
    ├── index.html       ← Landing page (admin/user entry points)
    ├── admin.html       ← Admin dashboard
    └── user.html        ← User parking portal
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## 🔐 Admin Login
- **Username:** `admin`
- **Password:** `admin123`

---

## 🌟 Features

### Admin Portal
- View live occupancy stats for all 5 areas
- See all active bookings in a table
- Force-release any occupied slot
- **Download CSV report** of all bookings

### User Portal
- Browse all parking areas with availability
- Search nearest parking (via GPS or manual coordinates)
- Interactive slot grid (green = free, red = occupied)
- Book a slot with name + vehicle number
- Release your slot using vehicle number verification

---

## 🏙️ Parking Areas (Hyderabad)
| Area | Slots |
|------|-------|
| Hitech City | 10 |
| Banjara Hills | 10 |
| Secunderabad | 10 |
| Gachibowli | 10 |
| Madhapur | 10 |

---

## 🔧 Tech Stack
- **Backend:** Python + Flask
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Database:** JSON flat-file (no DB setup needed)
- **Distance:** Haversine formula for nearest parking
