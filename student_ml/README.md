# Django ML Prediction API – Student Performance

A Django REST API that predicts student performance using a machine learning model trained on study habits and academic data.

## Features

- RESTful API endpoint for performance prediction
- Django admin interface for data management
- Input validation and error handling
- Unit tests
- ML model persistence with joblib

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd student_ml
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load dataset and train model**

   ```bash
   python manage.py shell
   >>> from performance.load_data import run
   >>> run()
   >>> from performance.train_model import train
   >>> train()
   >>> exit()
   ```

6. **Create superuser (optional, for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/predict/`

## API Usage

### Request Format

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "hours_studied": 6,
    "previous_scores": 78,
    "extracurricular": true,
    "sleep_hours": 7,
    "sample_papers": 3
  }'
```

### Response Format

```json
{
  "predicted_performance_index": 74.16
}
```

### Input Validation

- `hours_studied`: integer, 0-24
- `previous_scores`: integer, 0-100
- `extracurricular`: boolean
- `sleep_hours`: integer, 0-24
- `sample_papers`: integer, 0-20

Invalid requests return detailed error messages with 400 status code.

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to:

- View and manage student performance data
- Inspect training data
- Add new records

## Testing

### Run unit tests

```bash
python manage.py test
```

### Manual testing examples

**Valid request:**

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 10, "previous_scores": 95, "extracurricular": true, "sleep_hours": 8, "sample_papers": 5}'
```

**Invalid request (validation error):**

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 25, "previous_scores": 78, "extracurricular": true, "sleep_hours": 7, "sample_papers": 3}'
```

## Project Structure

```
student_ml/
├── manage.py
├── requirements.txt
├── dataset.csv
├── student_ml/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── performance/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    ├── load_data.py
    └── train_model.py
```

## Model Details

- **Algorithm**: Random Forest Regressor (200 estimators)
- **Target**: Performance Index (regression)
- **Features**: Hours studied, previous scores, extracurricular activities, sleep hours, sample papers practiced
- **Training**: Uses `dataset.csv` with 20 sample records

## Deployment Notes

- Store `model.pkl` outside repository or in `/performance/`
- Switch from SQLite to PostgreSQL for production
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`
- Use environment variables for sensitive settings

## Joblib Questions

**a. What is the purpose of joblib?**
Joblib is used for efficient serialization/deserialization of Python objects, especially large NumPy arrays or scikit-learn models, allowing trained models to be saved to disk and loaded later without retraining.

**b. Other libraries that can achieve the same as joblib**

- `pickle` (standard Python)
- `cloudpickle`
- `dill`
- `skops` (scikit-learn ecosystem)

## License

This project is for educational purposes.
