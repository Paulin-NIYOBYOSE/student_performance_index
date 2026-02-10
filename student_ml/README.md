# Django ML Prediction API – Advanced Student Performance System

A Django REST API that predicts student performance using an advanced machine learning model with realistic constraints and bias mitigation. The system uses Gradient Boosting with 14 engineered features to provide accurate, fair predictions.

## Key Features

- **Advanced ML Model**: Gradient Boosting with feature engineering and realistic constraints
- **Bias-Free Predictions**: Evidence-based constraints ensure fair outcomes
- **Comprehensive Analysis**: Risk assessment, warnings, and personalized recommendations
- **Realistic Constraints**: Penalizes extreme behaviors (no sleep, burnout, etc.)
- **10 Student Classifications**: From "High Performer" to "Burnout Risk"
- **Enhanced Dataset**: 200+ realistic samples covering diverse student profiles
- **RESTful API**: Clean endpoint with detailed validation
- **Django Admin**: Data management interface
- **Management Commands**: Easy setup and training workflow

## What Makes This Advanced?

### 1. Realistic Behavior Modeling

- Students who don't sleep (<3 hours) get 70% performance penalty
- Excessive study (>12 hours) with low sleep (<5 hours) triggers burnout penalty
- No study time = maximum 50% of previous score
- Optimal sleep (7-9 hours) maximizes cognitive capacity

### 2. Feature Engineering

Creates 14 features from 5 inputs:

- Study efficiency, sleep quality, balance score
- Practice intensity, burnout risk, cognitive capacity
- Study-sleep interactions, total preparation score

### 3. Evidence-Based Constraints

Based on sleep science and learning research:

- Optimal sleep: 7-9 hours
- Diminishing returns after 8 hours of study
- Burnout from high workload + low sleep
- Practice effects on retention

See [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) for complete technical details.

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

5. **Generate enhanced dataset and train model**

   ```bash
   # Generate 200+ realistic samples
   python manage.py generate_data

   # Load data into database
   python manage.py load_data

   # Train advanced model
   python manage.py train_model
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
  "predicted_performance_index": 74.16,
  "student_classification": "Balanced Student",
  "description": "Healthy balance between academics, activities, and rest.",
  "risk_level": "Low",
  "performance_gap": 5.16,
  "analysis": {
    "warnings": [],
    "recommendations": [
      "Great improvement trajectory! Maintain current habits."
    ]
  }
}
```

### Example: Burnout Risk Detection

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "hours_studied": 14,
    "previous_scores": 75,
    "extracurricular": false,
    "sleep_hours": 4,
    "sample_papers": 10
  }'
```

Response:

```json
{
  "predicted_performance_index": 52.3,
  "student_classification": "Burnout Risk",
  "description": "Overworking with insufficient recovery. Performance will decline.",
  "risk_level": "High",
  "performance_gap": -22.7,
  "analysis": {
    "warnings": [
      "Burnout risk: Excessive study with insufficient rest",
      "High risk of cognitive impairment due to low sleep"
    ],
    "recommendations": [
      "Reduce study hours and prioritize quality over quantity",
      "Increase sleep to at least 6-7 hours",
      "Performance declining. Review study methods and lifestyle."
    ]
  },
  "input_warnings": ["Studying >16 hours/day is unrealistic and unhealthy"]
}
```

### Input Validation

- `hours_studied`: integer, 0-24 (warning if >16)
- `previous_scores`: integer, 0-100
- `extracurricular`: boolean
- `sleep_hours`: integer, 0-24 (warning if <3 or >12)
- `sample_papers`: integer, 0-20

Invalid requests return detailed error messages with 400 status code.

Cross-field validation ensures study + sleep hours don't exceed 24 hours.

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to:

- View and manage student performance data
- Inspect training data
- Add new records

## Testing

### Run automated tests

```bash
# Start server in one terminal
python manage.py runserver

# Run comprehensive tests in another terminal
python performance/test_predictions.py
```

This tests 12 scenarios including:

- Balanced high performers
- Sleep-deprived students
- Burnout cases
- Oversleepers
- Zero effort students
- Perfect balance
- Edge cases

### Manual testing examples

**Balanced Student:**

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 6, "previous_scores": 85, "extracurricular": true, "sleep_hours": 8, "sample_papers": 6}'
```

**Sleep Deprived (Critical Warning):**

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 8, "previous_scores": 70, "extracurricular": false, "sleep_hours": 3, "sample_papers": 5}'
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

- **Algorithm**: Gradient Boosting Regressor (300 estimators)
- **Feature Engineering**: 14 features from 5 inputs
- **Preprocessing**: StandardScaler for feature normalization
- **Target**: Performance Index (0-100, regression)
- **Constraints**: Evidence-based realistic limits
- **Training**: Cross-validation with early stopping
- **Dataset**: 200+ realistic samples covering diverse student profiles

### Why Gradient Boosting?

- Better handles feature interactions than Random Forest
- More accurate for regression tasks
- Built-in regularization prevents overfitting
- Sequential error correction improves predictions

### Feature Importance

Top features (determined during training):

1. Previous Scores
2. Total Preparation Score
3. Study-Sleep Interaction
4. Hours Studied
5. Sleep Quality Score
6. Cognitive Capacity
7. Sample Papers Practiced
8. Balance Score
9. Study Efficiency
10. Practice Intensity

See [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) for complete technical documentation.

## Student Classifications

The system classifies students into 10 categories:

1. **High Performer**: Excellent balance of study, practice, and rest
2. **Balanced Student**: Healthy lifestyle with good habits
3. **Burnout Risk**: Overworking with insufficient sleep
4. **Sleep Deprived**: Critical lack of sleep affecting cognition
5. **At Risk**: Insufficient preparation across all areas
6. **Dedicated Learner**: Strong academic focus, could add activities
7. **Underprepared**: Good rest but insufficient study time
8. **Oversleeping**: Excessive sleep indicating potential issues
9. **Average Student**: Standard patterns with room for improvement
10. **Critical Risk**: Multiple severe issues requiring intervention

Each classification includes:

- Risk level (Critical/High/Medium/Low)
- Specific warnings
- Personalized recommendations
- Performance gap analysis

## Deployment Notes

- Ensure `model.pkl` is in `/performance/` directory
- Switch from SQLite to PostgreSQL for production
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`
- Use environment variables for sensitive settings
- Consider caching for frequently requested predictions
- Monitor model performance and retrain periodically

## Management Commands

```bash
# Generate enhanced dataset
python manage.py generate_data --samples 200

# Load data into database
python manage.py load_data

# Train the advanced model
python manage.py train_model

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## Project Structure

```
student_ml/
├── manage.py
├── requirements.txt
├── dataset.csv                    # Generated training data
├── README.md                      # This file
├── ADVANCED_FEATURES.md          # Technical documentation
├── student_ml/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── performance/
    ├── models.py                 # Django models
    ├── views.py                  # API endpoint with advanced logic
    ├── serializers.py
    ├── urls.py
    ├── admin.py
    ├── train_model.py           # Advanced ML training
    ├── generate_dataset.py      # Realistic data generation
    ├── load_data.py             # Database loading
    ├── test_predictions.py      # Comprehensive tests
    ├── model.pkl                # Trained model (generated)
    └── management/
        └── commands/            # Django management commands
            ├── generate_data.py
            ├── load_data.py
            └── train_model.py
```

## Advanced Features

### Realistic Constraints Applied

**Sleep Penalties:**

- < 3 hours: 70% reduction (critical)
- < 4 hours: 50% reduction (severe)
- < 5 hours: 30% reduction (moderate)
- > 12 hours: 40% reduction (excessive)

**Study Constraints:**

- 0 hours: Max 50% of previous score
- > 12 hours + < 5 sleep: 50% burnout penalty
- Diminishing returns after 8 hours

**Other Factors:**

- No practice papers: 20% reduction
- Low overall effort: Capped at 35
- Maximum improvement: +30 from previous score

### Bias Mitigation

- No demographic features (age, gender, race, etc.)
- Only behavior-based inputs
- Evidence-based constraints from research
- Balanced training data across all student types
- Transparent, explainable logic
- Cross-validated performance

## Research Foundation

Constraints based on:

- **Sleep Science**: 7-9 hours optimal for cognitive function
- **Learning Research**: Spaced practice and diminishing returns
- **Burnout Studies**: High workload + low sleep = decline
- **Educational Psychology**: Balance and well-being matter

## Example Scenarios

### Scenario 1: Perfect Balance

```json
Input: {"hours_studied": 7, "previous_scores": 85, "extracurricular": true, "sleep_hours": 8, "sample_papers": 6}
Output: High performance, "High Performer" classification, positive recommendations
```

### Scenario 2: Burnout

```json
Input: {"hours_studied": 14, "previous_scores": 75, "extracurricular": false, "sleep_hours": 4, "sample_papers": 10}
Output: Reduced performance, "Burnout Risk" classification, critical warnings
```

### Scenario 3: No Effort

```json
Input: {"hours_studied": 0, "previous_scores": 60, "extracurricular": false, "sleep_hours": 10, "sample_papers": 0}
Output: Low performance (max 30), "At Risk" classification, intervention needed
```

## API Response Fields

- `predicted_performance_index`: Predicted score (0-100)
- `student_classification`: One of 10 categories
- `description`: Explanation of classification
- `risk_level`: Critical/High/Medium/Low
- `performance_gap`: Predicted - previous score
- `analysis.warnings`: List of critical issues
- `analysis.recommendations`: Personalized advice
- `input_warnings`: Validation warnings (optional)

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
