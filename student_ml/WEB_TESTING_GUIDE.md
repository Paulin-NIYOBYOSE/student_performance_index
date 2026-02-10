# 🌐 Web Testing Guide

## Step 1: Access the Application

The server is now running! Open your web browser and go to:

```
http://127.0.0.1:8000/
```

or

```
http://localhost:8000/
```

You should see a beautiful, modern interface with the title **"Student Performance Predictor"**.

---

## Step 2: Understanding the Form

You'll see a form with 5 input fields:

1. **Hours Studied** (0-24) - How many hours the student studied
2. **Previous Scores** (0-100) - Student's previous exam scores
3. **Extracurricular Activities** (Yes/No) - Whether student participates in activities
4. **Sleep Hours** (0-24) - How many hours of sleep
5. **Sample Papers Practiced** (0-100) - Number of practice papers completed

---

## Step 3: Test Cases to Try

### 🌟 Test Case 1: High Performer (Balanced Student)

**Try these values:**

- Hours Studied: `7`
- Previous Scores: `85`
- Extracurricular Activities: `Yes`
- Sleep Hours: `8`
- Sample Papers: `6`

**Expected Result:**

- Prediction: ~76
- Classification: "High Performer"
- Risk Level: Medium
- Recommendations about maintaining balance

---

### 🎯 Test Case 2: Excellent Student (Top Performance)

**Try these values:**

- Hours Studied: `8`
- Previous Scores: `95`
- Extracurricular Activities: `Yes`
- Sleep Hours: `8`
- Sample Papers: `10`

**Expected Result:**

- Prediction: ~88
- Classification: "High Performer"
- Excellent balance message

---

### ⚠️ Test Case 3: At Risk Student (Needs Help)

**Try these values:**

- Hours Studied: `0`
- Previous Scores: `40`
- Extracurricular Activities: `No`
- Sleep Hours: `10`
- Sample Papers: `0`

**Expected Result:**

- Prediction: ~10
- Classification: "At Risk"
- Risk Level: High
- Warning: "No study time recorded"
- Recommendations to start studying

---

### 🔥 Test Case 4: Burnout Risk (Critical)

**Try these values:**

- Hours Studied: `15`
- Previous Scores: `80`
- Extracurricular Activities: `No`
- Sleep Hours: `3`
- Sample Papers: `12`

**Expected Result:**

- Prediction: Very low (~10)
- Classification: "Burnout Risk"
- Risk Level: High
- CRITICAL warnings about sleep deprivation
- Recommendations to reduce study hours and increase sleep

---

### 😴 Test Case 5: Sleep Deprived

**Try these values:**

- Hours Studied: `12`
- Previous Scores: `70`
- Extracurricular Activities: `No`
- Sleep Hours: `4`
- Sample Papers: `8`

**Expected Result:**

- Lower performance due to lack of sleep
- Warnings about cognitive impairment
- Recommendations to increase sleep

---

### 📚 Test Case 6: Underachiever (Good Potential, Low Effort)

**Try these values:**

- Hours Studied: `2`
- Previous Scores: `75`
- Extracurricular Activities: `Yes`
- Sleep Hours: `9`
- Sample Papers: `1`

**Expected Result:**

- Performance below potential
- Recommendations to increase study time

---

## Step 4: Test Input Validation

### Try Invalid Inputs:

**Negative Hours:**

- Hours Studied: `-5`
- Click Predict
- **Expected:** Error message "Must be 0-24"

**Score Over 100:**

- Previous Scores: `150`
- Click Predict
- **Expected:** Error message "Must be 0-100"

**Too Many Sleep Hours:**

- Sleep Hours: `30`
- Click Predict
- **Expected:** Error message "Must be 0-24"

**Leave Fields Empty:**

- Leave any field blank
- Click Predict
- **Expected:** Error message "Required"

---

## Step 5: Observe the Results

After clicking "Predict Performance", you'll see:

### 📊 Prediction Card Shows:

1. **Predicted Performance Index** - The score (0-100)
2. **Student Classification** - Category (High Performer, At Risk, etc.)
3. **Description** - What this classification means
4. **Risk Level** - Low, Medium, or High
5. **Performance Gap** - Difference from previous scores

### ⚠️ Warnings Section (if any):

- Critical alerts (red)
- Important warnings (orange)
- Examples: "CRITICAL: Severe sleep deprivation detected"

### 💡 Recommendations Section:

- Personalized advice based on the input
- Actionable suggestions to improve performance
- Examples: "Increase sleep to 7-8 hours", "Practice more sample papers"

---

## Step 6: Experiment!

Try different combinations to see how the model responds:

- **What happens with 0 hours of study?**
- **Does more sleep always help?**
- **What's the impact of extracurricular activities?**
- **Can you find the optimal balance?**
- **What happens with extreme values?**

---

## 🎨 What to Notice

### Visual Feedback:

- **Green indicators** - Good performance
- **Yellow/Orange indicators** - Medium risk
- **Red indicators** - High risk or critical warnings
- **Smooth animations** when results appear
- **Color-coded risk levels**

### Smart Analysis:

- The system considers interactions between factors
- It detects burnout patterns (high study + low sleep)
- It identifies underpreparation (low study + low practice)
- It provides context-aware recommendations

---

## 🛑 When You're Done Testing

To stop the server:

1. Go back to your terminal
2. Press `CTRL + C`

Or I can stop it for you when you're ready!

---

## 📝 Notes

- The model uses **Gradient Boosting** with advanced feature engineering
- It applies **realistic constraints** (e.g., you can't improve by 50 points overnight)
- It considers **sleep quality** (7-9 hours is optimal)
- It detects **burnout risk** (excessive study with insufficient rest)
- All predictions are bounded between 0-100

---

## 🚀 Have Fun Testing!

The system is designed to be realistic and educational. Try to find patterns and understand how different factors affect student performance!
