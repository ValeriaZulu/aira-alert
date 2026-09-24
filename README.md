# 🍃 AiraAlert

**AiraAlert** is a web application for estimating air quality based on **PM2.5 (particulate matter)** data from the **SIATA** monitoring network.

The application obtains the user's geographic coordinates through the browser, sends them to a Python/Flask backend hosted on **AWS EC2**, and estimates the PM2.5 concentration at that location using **spatial interpolation**. The resulting PM2.5 value is then converted into an **Air Quality Index (AQI)** and classified according to predefined air-quality categories.

---

## 📌 Project Overview

AiraAlert was developed as an academic project focused on the integration of:

* 🌐 React and TypeScript for the frontend
* 🐍 Python and Flask for the backend
* ☁️ AWS EC2 for backend deployment
* 📊 SIATA PM2.5 historical data
* 📍 Browser geolocation
* 📐 Spatial interpolation with `scipy`
* 🌱 Air Quality Index calculation

The project demonstrates how environmental data can be processed and transformed into an accessible air-quality measurement for a user's location.

---

## 🏗️ Architecture

```text
┌──────────────────────────────┐
│          React App           │
│      TypeScript + Vite       │
└──────────────┬───────────────┘
               │
               │ Browser Geolocation
               ▼
       Latitude / Longitude
               │
               │ HTTP POST
               ▼
┌──────────────────────────────┐
│          AWS EC2             │
│        Flask + Python        │
│                              │
│  ┌────────────────────────┐  │
│  │ SIATA PM2.5 dataset    │  │
│  └────────────┬───────────┘  │
│               │              │
│       Historical data        │
│               │              │
│       Spatial interpolation │
│               │              │
│          AQI calculation     │
└──────────────┬───────────────┘
               │
               │ JSON response
               ▼
┌──────────────────────────────┐
│          React App           │
│                              │
│   PM2.5 + AQI + Category     │
│   + Historical Date           │
└──────────────────────────────┘
```

---

## ✨ Main Features

### 📍 Geolocation

The application uses the browser's Geolocation API to obtain the user's current:

* Latitude
* Longitude

These coordinates are sent to the backend to calculate the air-quality estimate.

### 📊 PM2.5 Estimation

The backend processes PM2.5 measurements from **21 SIATA monitoring stations**.

For the requested date and hour, the application uses the available station measurements and applies **linear spatial interpolation** to estimate the PM2.5 concentration at the user's coordinates.

### 🌎 Historical Data

The available dataset contains historical SIATA measurements.

The backend matches the current:

* Month
* Day
* Hour

with the historical dataset and uses the most recent available year for that date and time.

### 🟢 Air Quality Index

The estimated PM2.5 concentration is converted into an AQI value using PM2.5 concentration breakpoints.

The application displays:

* PM2.5 concentration
* AQI
* Air-quality category
* Historical date used for the measurement

### 🎨 Dynamic Interface

The interface changes according to the calculated air-quality category.

| AQI Category                    | Color     |
| ------------------------------- | --------- |
| Bueno                           | 🟢 Green  |
| Moderado                        | 🟡 Yellow |
| Insalubre para grupos sensibles | 🟠 Orange |
| Insalubre                       | 🔴 Red    |
| Muy insalubre                   | 🟣 Purple |
| Peligroso                       | 🟣 Purple |

---

## 🧮 AQI Classification

The application uses PM2.5 concentration breakpoints to calculate the AQI through linear interpolation.

| PM2.5 (µg/m³) |       AQI | Category                        |
| ------------: | --------: | ------------------------------- |
|    0.0 – 12.0 |    0 – 50 | Bueno                           |
|   12.1 – 35.4 |  51 – 100 | Moderado                        |
|   35.5 – 55.4 | 101 – 150 | Insalubre para grupos sensibles |
|  55.5 – 150.4 | 151 – 200 | Insalubre                       |
| 150.5 – 250.4 | 201 – 300 | Muy insalubre                   |
| 250.5 – 350.4 | 301 – 400 | Peligroso                       |
| 350.5 – 500.4 | 401 – 500 | Peligroso                       |

The AQI is calculated using the following interpolation formula:

```text
AQI = ((IHi - ILo) / (BPHi - BPLo)) × (Cp - BPLo) + ILo
```

Where:

* `Cp` = PM2.5 concentration
* `BPHi` = upper concentration breakpoint
* `BPLo` = lower concentration breakpoint
* `IHi` = upper AQI breakpoint
* `ILo` = lower AQI breakpoint

---

## 🗂️ Project Structure

```text
airalert-react/
│
├── frontend/
|    ├── src/
|    │   ├── components/
|    │   │   ├── AirQualityCard.tsx
|    │   │   ├── LocationInfo.tsx
|    │   │   └── MeasureButton.tsx
|    │   │
|    │   ├── services/
|    │   │   └── airQualityService.ts
|    │   │
|    │   ├── types/
|    │   │   └── airQuality.ts
|    │   │
|    │   ├── App.tsx
|    │   ├── index.css
|    │   └── main.tsx
|    │
|    ├── public/
|    ├── package.json
|    ├── tsconfig.json
|    ├── vite.config.ts
|
├── backend/
|    ├── app.py
|
├── data-processing/
|    ├── clean_siata_data.py
|
└── README.md
```

---

## 🛠️ Technologies

### Frontend

* **React**
* **TypeScript**
* **Vite**
* **CSS**
* **Browser Geolocation API**

### Backend

* **Python**
* **Flask**
* **Pandas**
* **NumPy**
* **SciPy**

### Infrastructure

* **Amazon Web Services (AWS)**
* **Amazon EC2**

### Data

* **SIATA**
* PM2.5 historical measurements

---

## 🔄 Application Flow

1. The user opens AiraAlert.
2. The user selects **"Medir contaminación"**.
3. The browser requests permission to access the user's location.
4. The application obtains the latitude and longitude.
5. React sends the coordinates to the Flask API through an HTTP `POST` request.
6. The backend identifies the corresponding historical date and hour.
7. PM2.5 measurements from the available SIATA stations are selected.
8. `scipy.interpolate.griddata` performs linear spatial interpolation.
9. The interpolated PM2.5 value is converted into an AQI.
10. The backend returns a JSON response.
11. React displays the PM2.5 value, AQI, category and historical date.

---

## 📡 API

### `POST /medir`

Receives the user's geographic coordinates.

#### Request

```json
{
  "latitud": 6.24213,
  "longitud": -75.57987
}
```

#### Response

```json
{
  "pm25": 12.34,
  "aqi": 52,
  "categoria": "Moderado",
  "color": "amarillo",
  "fecha": "septiembre 18 - 15:00"
}
```

---

## 📍 Data Processing

The original SIATA dataset contains hourly PM2.5 measurements from multiple monitoring stations.

During preprocessing, invalid values were handled before performing the spatial interpolation:

* `-9999` values were treated as missing data.
* Negative PM2.5 values were treated as invalid.
* Extremely high anomalous values were treated as missing.
* Missing values were interpolated over time for each monitoring station.

The resulting dataset was then used by the Flask backend.

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd airalert-react
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The application will be available at:

```text
http://localhost:5173
```

### 4. Backend

The frontend communicates with the Flask API deployed on AWS EC2.

The backend must be running and accessible for the air-quality measurement functionality to work.

---

## ⚠️ Important Considerations

* Browser geolocation requires user permission.
* The application depends on the availability of the Flask backend.
* The EC2 public IP address may change if the instance is stopped and restarted.
* The spatial interpolation requires the requested location to be within the area covered by the available monitoring stations.
* The historical dataset determines the temporal availability of the measurements.

---

## 🎓 Academic Context

This project was developed as an academic exercise to integrate concepts related to:

* Web development
* REST APIs
* Data processing
* Environmental data
* Geographic coordinates
* Spatial interpolation
* Cloud computing
* Data visualization and interpretation

The project also represents the migration of an initial prototype developed with **MIT App Inventor** into a code-based web application using **React, TypeScript, Python and Flask**.

---

## 👩‍💻 Author

**Valeria Zuluaga Alzate**

Systems Engineering student
Universidad Pontificia Bolivariana

---

## 📄 License

This project was developed for academic purposes.
