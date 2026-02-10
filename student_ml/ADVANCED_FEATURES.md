# Advanced Student Performance Prediction System

## Overview

This enhanced system uses advanced machine learning techniques with realistic constraints to predict student performance accurately and without bias. The model considers complex interactions between study habits, sleep patterns, and lifestyle factors.

## Key Enhancements

### 1. Advanced Feature Engineering

The system creates 14 features from 5 input variables:

**Base Features:**

- Hours Studied (0-24)
- Previous Scores (0-100)
- Extracurricular Activities (Yes/No)
- Sleep Hours (0-24)
- Sample Papers Practiced (0-20)

**Engineered Features:**

- **Study Efficiency**: Previous scores per study hour
- **Sleep Quality Score**: Optimal at 7-9 hours, penalized outside this range
- **Balance Score**: Weighted combination of study, sleep, and activities
- **Practice Intensity**: Papers practiced per study hour
- **Burnout Risk**: Binary flag for high study + low sleep
- **Underprepared Risk**: Binary flag for low study + low practice
- **Cognitive Capacity**: Sleep-based learning capacity (3-9 hours scale)
- **Total Preparation**: Weighted sum of all preparation factors
- **Study-Sleep Interaction**: Multiplicative effect of study and sleep quality

### 2. Realistic Constraints

The model applies evidence-based constraints:

**Sleep Constraints:**

- < 3 hours: 70% performance penalty (critical impairment)
- < 4 hours: 50% performance penalty (severe impairment)
- < 5 hours: 30% performance penalty (moderate impairment)
- > 12 hours: 40% performance penalty (excessive sleep issues)
- > 10 hours: 15% performance penalty (oversleeping)

**Study Constraints:**

- 0 hours: Maximum 50% of previous score
- > 12 hours with < 5 sleep: 50% burnout penalty
- Diminishing returns after 8 hours of study

**Practice Constraints:**

- 0 sample papers: 20% performance reduction
- Low effort (< 3 hours study, < 2 papers, < 40 previous): Capped at 35

**Improvement Constraints:**

- Maximum improvement: Previous score + 30 points
- Performance bounded: 0-100 range

### 3. Advanced ML Model

**Algorithm:** Gradient Boosting Regressor

- 300 estimators for robust predictions
- Learning rate: 0.05 (prevents overfitting)
- Max depth: 5 (captures complex interactions)
- Early stopping with validation
- Feature scaling with StandardScaler

**Why Gradient Boosting over Random Forest?**

- Better handles feature interactions
- More accurate for regression tasks
- Built-in regularization
- Sequential error correction

### 4. Comprehensive Student Classification

The system classifies students into 10 categories:

1. **High Performer**: Excellent balance (7+ hours study, 5+ papers, 6-9 hours sleep)
2. **Balanced Student**: Healthy lifestyle (4-8 hours study, 7-9 hours sleep, activities)
3. **Burnout Risk**: Overworking (>10 hours study, <5 hours sleep)
4. **Sleep Deprived**: Critical lack of sleep (<4 hours)
5. **At Risk**: Insufficient preparation (<2 hours study, <2 papers, <50 previous)
6. **Dedicated Learner**: Strong focus (>9 hours study, good sleep, no activities)
7. **Underprepared**: Good rest but low study (<3 hours study, 8+ hours sleep)
8. **Oversleeping**: Excessive sleep (>10 hours)
9. **Average Student**: Standard patterns
10. **Critical Risk**: Multiple severe issues

### 5. Intelligent Analysis System

Each prediction includes:

**Risk Assessment:**

- Risk Level: Critical / High / Medium / Low
- Specific warnings for dangerous patterns
- Health and performance alerts

**Personalized Recommendations:**

- Sleep optimization advice
- Study habit improvements
- Balance suggestions
- Health warnings

**Performance Gap Analysis:**

- Predicted vs. previous score comparison
- Improvement trajectory assessment
- Trend identification

### 6. Enhanced Dataset

Generated 200+ realistic samples covering:

- High performers with balanced habits
- Struggling students with multiple issues
- Burnout cases (high study, low sleep)
- Underachievers (good potential, low effort)
- Sleep-deprived students
- Oversleepers
- Efficient learners
- Edge cases and extreme scenarios

## API Response Format

```json
{
  "predicted_performance_index": 72.5,
  "student_classification": "Balanced Student",
  "description": "Healthy balance between academics, activities, and rest.",
  "risk_level": "Low",
  "performance_gap": 5.5,
  "analysis": {
    "warnings": [],
    "recommendations": [
      "Great improvement trajectory! Maintain current habits."
    ]
  },
  "input_warnings": []
}
```

## Example Scenarios

### Scenario 1: Burnout Risk

**Input:**

```json
{
  "hours_studied": 14,
  "previous_scores": 75,
  "extracurricular": false,
  "sleep_hours": 4,
  "sample_papers": 10
}
```

**Expected Output:**

- Classification: "Burnout Risk"
- Risk Level: "High"
- Warnings: "Burnout risk: Excessive study with insufficient rest"
- Recommendations: "Reduce study hours and prioritize quality over quantity"
- Performance: Significantly penalized despite high effort

### Scenario 2: Efficient Learner

**Input:**

```json
{
  "hours_studied": 6,
  "previous_scores": 85,
  "extracurricular": true,
  "sleep_hours": 8,
  "sample_papers": 6
}
```

**Expected Output:**

- Classification: "High Performer"
- Risk Level: "Low"
- Performance: High score with positive trajectory
- Recommendations: "Maintain current habits"

### Scenario 3: Sleep Deprived

**Input:**

```json
{
  "hours_studied": 8,
  "previous_scores": 70,
  "extracurricular": false,
  "sleep_hours": 3,
  "sample_papers": 5
}
```

**Expected Output:**

- Classification: "Sleep Deprived"
- Risk Level: "Critical"
- Warnings: "CRITICAL: Severe sleep deprivation detected"
- Recommendations: "Prioritize sleep immediately - aim for 7-8 hours"
- Performance: Heavily penalized (50% reduction)

## Bias Mitigation

The system ensures fairness through:

1. **No demographic features**: Only behavior-based inputs
2. **Evidence-based constraints**: Based on sleep science and learning research
3. **Balanced training data**: Equal representation of all student types
4. **Transparent logic**: All penalties and bonuses are documented
5. **Cross-validation**: Model tested across diverse scenarios

## Model Performance Metrics

After training, the system reports:

- R² Score (goodness of fit)
- RMSE (prediction error)
- MAE (average absolute error)
- Feature importance rankings

## Setup and Usage

### 1. Generate Enhanced Dataset

```bash
python performance/generate_dataset.py
```

### 2. Load Data to Database

```bash
python manage.py shell
>>> from performance.load_data import run
>>> run()
>>> exit()
```

### 3. Train Advanced Model

```bash
python manage.py shell
>>> from performance.train_model import train
>>> train()
>>> exit()
```

### 4. Run Tests

```bash
# Start server in one terminal
python manage.py runserver

# Run tests in another terminal
python performance/test_predictions.py
```

## Technical Details

**Model File Structure:**

```python
{
    'model': GradientBoostingRegressor,
    'scaler': StandardScaler,
    'feature_columns': [list of 14 features]
}
```

**Prediction Pipeline:**

1. Validate input
2. Engineer 14 features
3. Scale features
4. Model prediction
5. Apply realistic constraints
6. Classify student
7. Generate recommendations

## Research-Based Design

The constraints are based on:

- Sleep research: 7-9 hours optimal for cognitive function
- Learning science: Diminishing returns after 8 hours of study
- Burnout research: High workload + low sleep = performance decline
- Practice effects: Spaced practice improves retention

## Future Enhancements

Potential improvements:

- Time-series analysis for trend prediction
- Personalized study schedules
- Stress level integration
- Diet and exercise factors
- Social support metrics
- Mental health indicators

## Conclusion

This advanced system provides accurate, unbiased predictions by:

- Using sophisticated feature engineering
- Applying evidence-based constraints
- Considering realistic human limitations
- Providing actionable insights
- Ensuring fairness across all student types

The model recognizes that a student who doesn't sleep will not perform well, regardless of study hours, and that excessive study without rest leads to burnout rather than success.
