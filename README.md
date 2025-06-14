#  Resume2Portfolio

Turn your resume into a structured portfolio using OCR and Django.

**🔗 Live Demo:** [https://resume2portfolio.duckdns.org/](https://resume2portfolio.duckdns.org/)

---

## 🚀 Project Overview

Resume2Portfolio is a Django-based web application that allows users to upload a resume (image or PDF), extract structured data using OCR (Optical Character Recognition), and generate a clean JSON output.

### ✨ Use Cases

* Automatically build portfolios from resumes
* Parse resumes for job portals
* Structure applicant data for storage or analysis

---

## ⚙️ Tech Stack Used

### 🔹 Backend

* **Python 3.12** – Core programming language.
* **Django 5.x** – Backend web framework (models, views, URLs).
* **SQLite3** – Lightweight built-in database for storing parsed data.
* **Tesseract OCR** – Converts resume images into text.
* **PyMuPDF (fitz)** – Extracts text from PDF resumes.
* **EasyOCR** *(optional)* – For better accuracy with image-based resumes.

### 🔹 Frontend

* **HTML5, CSS3** – Basic structure and styling.
* **Bootstrap 5** – Responsive and user-friendly UI.
* **JavaScript** – For UI interactions like loading indicators.

### 🔹 DevOps & Deployment

* **Gunicorn** – WSGI server for running Django in production.
* **Supervisor** – Keeps the Django app always running.
* **Nginx** – Acts as a reverse proxy server.
* **DuckDNS** – Free dynamic domain name service.
* **AWS EC2 (Ubuntu)** – Cloud server hosting.

---

## 📂 Project Structure

```
resume2portfolio/
├── ocrapp/                 # Main Django app
│   ├── templates/          # HTML templates (upload, output)
│   ├── views.py            # Logic for file upload & OCR parsing
│   ├── models.py           # Django model to store parsed resume data
│   └── urls.py             # App-level URL routing
├── static/                 # Static assets like CSS and JS
├── db.sqlite3              # SQLite database file
├── manage.py               # Django project runner
├── requirements.txt        # All Python dependencies
└── config.yaml             # Optional: custom config (e.g., Tesseract path)
```

---

## 🛠️ Installation Guide (Local Setup)

Follow these steps to run the project locally:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Aman-859/resume2portfolio.git
cd resume2portfolio
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Tesseract OCR

This is required for OCR to work.

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

#### macOS (Homebrew):

```bash
brew install tesseract
```

#### Windows:

* Download: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
* Add install path (e.g., `C:\Program Files\Tesseract-OCR`) to system `PATH`

### 5️⃣ Apply database migrations

```bash
python manage.py migrate
```

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🔎 Sample Resume Output

Check out this resume parsed and built using Resume2Portfolio:
👉 [View Resume Output](http://resume2portfolio.duckdns.org/resume/8a2a7af9-85b4-44eb-aaaf-2ea7dc572f14/)

---

## 📬 Contact

**Aman S Mishra**
📧 [amanmishra150306@gmail.com](mailto:amanmishra150306@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/Aman-SM/) | [GitHub](https://github.com/Aman-859)

---

️ If you like this project, give it a star or fork it to support!
