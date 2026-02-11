# Student Performance Predictor

ML-powered web app that predicts student academic performance based on study habits and sleep patterns.

**Repository**: [github.com/Paulin-NIYOBYOSE/student_performance_index](https://github.com/Paulin-NIYOBYOSE/student_performance_index)

## Quick Start

```bash
# Clone
git clone https://github.com/Paulin-NIYOBYOSE/student_performance_index.git
cd student_performance_index

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

## Usage

Enter student data:
- **Hours Studied** (0-24)
- **Previous Scores** (0-100)
- **Sleep Hours** (0-24)
- **Sample Papers** (0-20)
- **Extracurricular** (yes/no)

Click **Predict Performance** to get results with classification and recommendations.

## API

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 6, "previous_scores": 75, "sleep_hours": 7, "sample_papers": 5, "extracurricular": true}'
```

## Tech Stack

- Django + Django REST Framework
- scikit-learn (Random Forest)
- HTML/CSS/JavaScript

## License

MIT
