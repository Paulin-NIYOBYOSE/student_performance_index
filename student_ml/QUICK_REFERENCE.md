# Quick Reference Guide

## Setup (One Command)

```bash
./setup_advanced_model.sh
```

Or manually:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py generate_data
python manage.py load_data
python manage.py train_model
```

## Start Server

```bash
python manage.py runserver
```

## Test API

```bash
# In another terminal
python performance/test_predictions.py
```

## API Endpoint

```
POST http://127.0.0.1:8000/api/predict/
Content-Type: application/json
```

## Request Format

```json
{
  "hours_studied": 6,
  "previous_scores": 78,
  "extracurricular": true,
  "sleep_hours": 7,
  "sample_papers": 3
}
```

## Response Format

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

## Input Constraints

| Field           | Type | Range      | Notes                |
| --------------- | ---- | ---------- | -------------------- |
| hours_studied   | int  | 0-24       | Warning if >16       |
| previous_scores | int  | 0-100      | -                    |
| extracurricular | bool | true/false | -                    |
| sleep_hours     | int  | 0-24       | Warning if <3 or >12 |
| sample_papers   | int  | 0-20       | -                    |

**Cross-validation**: hours_studied + sleep_hours ≤ 24

## Realistic Constraints Applied

### Sleep Penalties

- < 3 hours: **70% reduction** (critical)
- < 4 hours: **50% reduction** (severe)
- < 5 hours: **30% reduction** (moderate)
- > 12 hours: **40% reduction** (excessive)

### Study Constraints

- 0 hours: Max **50% of previous score**
- > 12 hours + < 5 sleep: **50% burnout penalty**
- Diminishing returns after 8 hours

### Other Factors

- No practice papers: **20% reduction**
- Low overall effort: **Capped at 35**
- Max improvement: **Previous + 30**

## Student Classifications

1. **High Performer** - Excellent balance
2. **Balanced Student** - Healthy lifestyle
3. **Burnout Risk** - Overworking + low sleep
4. **Sleep Deprived** - Critical lack of sleep
5. **At Risk** - Insufficient preparation
6. **Dedicated Learner** - Strong focus
7. **Underprepared** - Good rest, low study
8. **Oversleeping** - Excessive sleep
9. **Average Student** - Standard patterns
10. **Critical Risk** - Multiple severe issues

## Risk Levels

- **Critical**: Immediate intervention needed
- **High**: Significant concerns
- **Medium**: Some issues to address
- **Low**: Healthy patterns

## Example Scenarios

### Perfect Balance

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 7, "previous_scores": 85, "extracurricular": true, "sleep_hours": 8, "sample_papers": 6}'
```

→ High performance, positive recommendations

### Burnout Risk

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 14, "previous_scores": 75, "extracurricular": false, "sleep_hours": 4, "sample_papers": 10}'
```

→ Reduced performance, critical warnings

### Sleep Deprived

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 8, "previous_scores": 70, "extracurricular": false, "sleep_hours": 3, "sample_papers": 5}'
```

→ Severe penalty (50%), health warnings

### No Effort

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 0, "previous_scores": 60, "extracurricular": false, "sleep_hours": 10, "sample_papers": 0}'
```

→ Low performance (max 30), intervention needed

## Management Commands

```bash
# Generate dataset
python manage.py generate_data --samples 200

# Load data to database
python manage.py load_data

# Train model
python manage.py train_model

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## File Structure

```
student_ml/
├── README.md                      # Main documentation
├── ADVANCED_FEATURES.md          # Technical details
├── IMPROVEMENTS.md               # Before/after comparison
├── QUICK_REFERENCE.md           # This file
├── setup_advanced_model.sh      # One-command setup
├── dataset.csv                   # Training data
├── requirements.txt              # Dependencies
├── performance/
│   ├── views.py                 # API endpoint
│   ├── train_model.py          # ML training
│   ├── generate_dataset.py     # Data generation
│   ├── test_predictions.py     # Test suite
│   └── model.pkl               # Trained model
└── student_ml/
    └── settings.py              # Django config
```

## Model Details

- **Algorithm**: Gradient Boosting Regressor
- **Features**: 14 (from 5 inputs)
- **Estimators**: 300
- **Dataset**: 200+ samples
- **Preprocessing**: StandardScaler
- **Validation**: Cross-validation

## Feature Engineering

From 5 inputs → 14 features:

1. Hours Studied
2. Previous Scores
3. Extracurricular Activities
4. Sleep Hours
5. Sample Papers Practiced
6. Study Efficiency
7. Sleep Quality Score
8. Balance Score
9. Practice Intensity
10. Burnout Risk
11. Underprepared Risk
12. Cognitive Capacity
13. Total Preparation
14. Study-Sleep Interaction

## Troubleshooting

### Model not found

```bash
python manage.py train_model
```

### Database errors

```bash
python manage.py migrate
python manage.py load_data
```

### Import errors

```bash
pip install -r requirements.txt
```

### Server won't start

```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

## Admin Interface

```
URL: http://127.0.0.1:8000/admin/
```

Create admin user:

```bash
python manage.py createsuperuser
```

## Testing

### Automated Tests

```bash
python performance/test_predictions.py
```

### Manual Test

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"hours_studied": 6, "previous_scores": 78, "extracurricular": true, "sleep_hours": 7, "sample_papers": 3}'
```

## Key Principles

1. **No sleep = Poor performance** (70% penalty for <3 hours)
2. **Burnout is real** (50% penalty for overwork + low sleep)
3. **Balance matters** (Optimal: 7-9 hours sleep, 4-8 hours study)
4. **Practice helps** (Sample papers improve scores)
5. **Diminishing returns** (More study ≠ always better)
6. **Realistic limits** (Can't improve >30 points from previous)

## Support

- Read: `README.md` for overview
- Read: `ADVANCED_FEATURES.md` for technical details
- Read: `IMPROVEMENTS.md` for before/after comparison
- Check: Code comments for implementation details
- Test: `test_predictions.py` for examples

## License

Educational purposes
