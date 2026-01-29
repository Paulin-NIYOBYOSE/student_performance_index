import joblib
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

MODEL_PATH = "performance/model.pkl"


def classify_student(data: dict) -> dict:
    """Classify student based on their study habits and lifestyle."""
    hours_studied = data.get("hours_studied", 0)
    sleep_hours = data.get("sleep_hours", 0)
    previous_scores = data.get("previous_scores", 0)
    sample_papers = data.get("sample_papers", 0)
    extracurricular = data.get("extracurricular", False)
    
    classification = ""
    description = ""
    
    # Stressed Student: High study hours (>10) with low sleep (<5)
    if hours_studied > 10 and sleep_hours < 5:
        classification = "Stressed Student"
        description = "High study load with insufficient sleep. Risk of burnout."
    
    # Sleep Deprived: Very low sleep (<4)
    elif sleep_hours < 4:
        classification = "Sleep Deprived"
        description = "Severe lack of sleep affecting cognitive function."
    
    # Overachiever: High study, high practice, good sleep
    elif hours_studied >= 8 and sample_papers >= 5 and sleep_hours >= 6:
        classification = "Overachiever"
        description = "Dedicated student with balanced preparation."
    
    # Underperformer: Low study, low practice, low previous scores
    elif hours_studied < 3 and sample_papers < 2 and previous_scores < 50:
        classification = "At Risk"
        description = "Needs more study time and practice to improve."
    
    # Balanced Student: Moderate study, good sleep, has activities
    elif 4 <= hours_studied <= 8 and 6 <= sleep_hours <= 9 and extracurricular:
        classification = "Balanced Student"
        description = "Good balance between academics and life."
    
    # Bookworm: High study but no extracurricular
    elif hours_studied > 8 and not extracurricular:
        classification = "Bookworm"
        description = "Focused on academics, could benefit from activities."
    
    # Casual Learner: Low study hours but decent sleep
    elif hours_studied < 4 and sleep_hours >= 7:
        classification = "Casual Learner"
        description = "Relaxed approach to studies."
    
    # Normal Student: Default
    else:
        classification = "Normal Student"
        description = "Average study habits."
    
    return {
        "classification": classification,
        "description": description
    }


def validate_input(data: dict) -> dict:
    errors = {}
    
    if "hours_studied" not in data:
        errors["hours_studied"] = "Required"
    elif not isinstance(data["hours_studied"], int) or not (0 <= data["hours_studied"] <= 24):
        errors["hours_studied"] = "Must be 0-24"
    
    if "previous_scores" not in data:
        errors["previous_scores"] = "Required"
    elif not isinstance(data["previous_scores"], int) or not (0 <= data["previous_scores"] <= 100):
        errors["previous_scores"] = "Must be 0-100"
    
    if "extracurricular" not in data:
        errors["extracurricular"] = "Required"
    elif not isinstance(data["extracurricular"], bool):
        errors["extracurricular"] = "Must be true or false"
    
    if "sleep_hours" not in data:
        errors["sleep_hours"] = "Required"
    elif not isinstance(data["sleep_hours"], int) or not (0 <= data["sleep_hours"] <= 24):
        errors["sleep_hours"] = "Must be 0-24"
    
    if "sample_papers" not in data:
        errors["sample_papers"] = "Required"
    elif not isinstance(data["sample_papers"], int) or not (0 <= data["sample_papers"] <= 20):
        errors["sample_papers"] = "Must be 0-20"
    
    return errors


@csrf_exempt
@api_view(["POST"])
def predict_performance(request):
    errors = validate_input(request.data)
    if errors:
        return Response({"errors": errors}, status=400)
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return Response({"error": "Model not found. Train the model first."}, status=500)
    data = request.data
    features = np.array(
        [
            [
                data["hours_studied"],
                data["previous_scores"],
                1 if data["extracurricular"] else 0,
                data["sleep_hours"],
                data["sample_papers"],
            ]
        ]
    )
    try:
        prediction = model.predict(features)[0]
    except Exception as exc:
        return Response({"error": f"Prediction failed: {exc}"}, status=500)
    
    student_class = classify_student(data)
    
    return Response({
        "predicted_performance_index": round(float(prediction), 2),
        "student_type": student_class["classification"],
        "student_description": student_class["description"]
    })
