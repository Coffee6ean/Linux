### ✅ `setup.md` — EC2 Environment Setup for CFA Processor

````markdown
# EC2 Setup Instructions for CFA Processor

This guide walks through the necessary steps to prepare an EC2 Ubuntu instance to run the CFA file processing API.

---

## 📦 Step 1: Install System Dependencies

Update packages and install Python, pip, venv, and Nginx:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx -y
````

---

## 🏗️ Step 2: Set Up Project Environment

Navigate to your project folder and create a virtual environment:

```bash
cd project_directory  # Replace with your actual project folder
python3 -m venv venv
source venv/bin/activate
```

---

## 📚 Step 3: Install Required Python Libraries

Install all required packages inside the virtual environment:

```bash
pip install Flask
pip install pandas
pip install openpyxl
pip install plotly
pip install --upgrade kaleido
```

---

## 📁 Step 4: Prepare Output Directory

Create a folder to store remote CFA results:

```bash
cd ~/
mkdir CFA_Results_Remote
```

---

## ✅ Done!

Your EC2 instance is now ready to run the Flask-based CFA processing service.
Make sure to:

* Configure your Flask app to run on `0.0.0.0`
* Open port `5000` in your EC2 security group
* Use `gunicorn` or `flask run` for quick testing
