# MiniF2F Formalization Website

This is a simple website to display MiniF2F dataset of mathematical problems and their proofs in natural language.

## Local Run Guide

Please follow the steps below to run this website locally:

### 1. Clone the Repository

First, you need to clone this project to your local machine:

```bash
git clone https://github.com/shihaoyang0423/MiniF2F-Exhibition.git
cd MiniF2F-Exhibition
```

### 2. Create and Activate a Python Virtual Environment (Recommended)

To avoid dependency conflicts, it is recommended to create an isolated Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# Or .\venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

After activating the virtual environment, install the required Python dependencies for the project:

```bash
pip install -r requirements.txt
```


### 4. Run the Website

After installing the dependencies, you can start the Flask application:

```bash
python3 app.py
```

If everything runs successfully, you will see a message like `Running on http://127.0.0.1:5000` in your terminal. Open this address in your browser to access the website.

### 5. Stop the Website

Press `Ctrl+C` in the terminal to stop the website.
