# 🎯 Quick Test Scenarios

## Copy & Paste These Values Into the Web Form

### ✅ Scenario 1: Perfect Balance

```
Hours Studied: 7
Previous Scores: 85
Extracurricular: Yes
Sleep Hours: 8
Sample Papers: 6
```

**Expected:** ~76 points, "High Performer"

---

### 🌟 Scenario 2: Top Student

```
Hours Studied: 8
Previous Scores: 95
Extracurricular: Yes
Sleep Hours: 8
Sample Papers: 10
```

**Expected:** ~88 points, "High Performer"

---

### ⚠️ Scenario 3: Struggling Student

```
Hours Studied: 0
Previous Scores: 40
Extracurricular: No
Sleep Hours: 10
Sample Papers: 0
```

**Expected:** ~10 points, "At Risk", Critical warnings

---

### 🔥 Scenario 4: Burnout Alert

```
Hours Studied: 15
Previous Scores: 80
Extracurricular: No
Sleep Hours: 3
Sample Papers: 12
```

**Expected:** ~10 points, "Burnout Risk", CRITICAL warnings

---

### 😴 Scenario 5: Sleep Deprived

```
Hours Studied: 12
Previous Scores: 70
Extracurricular: No
Sleep Hours: 4
Sample Papers: 8
```

**Expected:** Low score, warnings about sleep

---

### 🎮 Scenario 6: Underachiever

```
Hours Studied: 2
Previous Scores: 75
Extracurricular: Yes
Sleep Hours: 9
Sample Papers: 1
```

**Expected:** Below potential, needs more effort

---

## 🧪 Test Validation Errors

### Test 1: Negative Hours

```
Hours Studied: -5
(fill other fields normally)
```

**Expected:** Error: "Must be 0-24"

### Test 2: Invalid Score

```
Previous Scores: 150
(fill other fields normally)
```

**Expected:** Error: "Must be 0-100"

### Test 3: Too Much Sleep

```
Sleep Hours: 30
(fill other fields normally)
```

**Expected:** Error: "Must be 0-24"

---

## 🎨 What to Look For

- **Prediction Number** - The performance score
- **Classification Badge** - Student category
- **Risk Level** - Color-coded indicator
- **Warnings** - Red/orange alerts
- **Recommendations** - Personalized advice
- **Performance Gap** - Change from previous scores

---

## 💡 Pro Tips

1. **Try extreme combinations** to see how the model handles edge cases
2. **Compare similar inputs** with one variable changed
3. **Look for patterns** in the recommendations
4. **Notice the warnings** for unhealthy patterns
5. **Test the validation** with invalid inputs

---

## 🌐 Access the App

Open your browser and go to:
**http://127.0.0.1:8000/**

The server is running and ready for testing! 🚀
