import joblib
import numpy as np
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

MODEL_PATH = "performance/model.pkl"


def engineer_features_for_prediction(data: dict) -> pd.DataFrame:
    """Engineer features for a single prediction matching training features."""
    
    # Base features
    hours_studied = data["hours_studied"]
    previous_scores = data["previous_scores"]
    extracurricular = 1 if data["extracurricular"] else 0
    sleep_hours = data["sleep_hours"]
    sample_papers = data["sample_papers"]
    
    # Engineered features (same as training)
    study_efficiency = previous_scores / (hours_studied + 1)
    
    # Sleep quality score
    if 7 <= sleep_hours <= 9:
        sleep_quality = 1.0
    elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
        sleep_quality = 0.8
    elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
        sleep_quality = 0.5
    elif 4 <= sleep_hours < 5 or 11 < sleep_hours <= 12:
        sleep_quality = 0.2
    else:
        sleep_quality = 0.0
    
    balance_score = (hours_studied / 10) * 0.4 + sleep_quality * 0.3 + extracurricular * 0.3
    practice_intensity = sample_papers / (hours_studied + 1)
    burnout_risk = 1 if (hours_studied > 10 and sleep_hours < 6) else 0
    underprepared_risk = 1 if (hours_studied < 3 and sample_papers < 2) else 0
    cognitive_capacity = min(1.0, max(0.0, (sleep_hours - 3) / 6))
    total_preparation = hours_studied * 0.3 + sample_papers * 2 + previous_scores * 0.2
    study_sleep_interaction = hours_studied * sleep_quality
    
    # Create DataFrame with all features
    features_df = pd.DataFrame([{
        "Hours Studied": hours_studied,
        "Previous Scores": previous_scores,
        "Extracurricular Activities": extracurricular,
        "Sleep Hours": sleep_hours,
        "Sample Question Papers Practiced": sample_papers,
        "study_efficiency": study_efficiency,
        "sleep_quality": sleep_quality,
        "balance_score": balance_score,
        "practice_intensity": practice_intensity,
        "burnout_risk": burnout_risk,
        "underprepared_risk": underprepared_risk,
        "cognitive_capacity": cognitive_capacity,
        "total_preparation": total_preparation,
        "study_sleep_interaction": study_sleep_interaction
    }])
    
    return features_df


def apply_realistic_constraints_single(prediction: float, data: dict) -> float:
    """Apply realistic constraints to a single prediction with high-level logic."""
    
    hours_studied = data["hours_studied"]
    sleep_hours = data["sleep_hours"]
    previous_scores = data["previous_scores"]
    sample_papers = data["sample_papers"]
    
    pred = prediction
    
    # ============ CRITICAL: IMPOSSIBLE SCENARIOS ============
    
    # Zero sleep = cognitive failure, cannot perform on exam
    if sleep_hours == 0:
        pred = 0  # Cannot function without any sleep
    elif sleep_hours == 1:
        pred = min(pred * 0.05, 5)  # Severe impairment, max 5%
    elif sleep_hours == 2:
        pred = min(pred * 0.1, 10)  # Extreme impairment, max 10%
    elif sleep_hours < 4:
        pred *= 0.2  # Severe cognitive decline
    elif sleep_hours < 5:
        pred *= 0.4  # Significant impairment
    elif sleep_hours < 6:
        pred *= 0.6  # Moderate impairment
    
    # Zero study = cannot pass without studying (unless previous knowledge)
    if hours_studied == 0:
        # Can only rely on previous knowledge, heavily degraded
        pred = min(pred, previous_scores * 0.3)  # Max 30% of previous scores
        if sample_papers == 0:
            pred = min(pred, 5)  # Essentially failing without any preparation
    elif hours_studied == 1:
        pred = min(pred, previous_scores * 0.5)  # Very limited preparation
    elif hours_studied < 3:
        pred = min(pred, previous_scores * 0.7)  # Insufficient preparation
    
    # ============ EXCESSIVE/UNREALISTIC SCENARIOS ============
    
    # Excessive sleep (>12 hours) indicates health issues, reduced performance
    if sleep_hours > 14:
        pred *= 0.3  # Severe lethargy, possible health crisis
    elif sleep_hours > 12:
        pred *= 0.5  # Oversleeping significantly impacts alertness
    elif sleep_hours > 10:
        pred *= 0.75  # Mild oversleeping
    
    # ============ BURNOUT SCENARIOS ============
    
    # Extreme study with no sleep = burnout and failure
    if hours_studied > 12 and sleep_hours < 5:
        pred *= 0.3  # Burnout severely impacts performance
    elif hours_studied > 10 and sleep_hours < 6:
        pred *= 0.5  # High burnout risk
    elif hours_studied > 8 and sleep_hours < 5:
        pred *= 0.6  # Moderate burnout
    
    # ============ PREPARATION QUALITY ============
    
    # No practice papers = unprepared for exam format
    if sample_papers == 0:
        pred *= 0.7  # Unfamiliar with exam format
    elif sample_papers < 3:
        pred *= 0.85  # Limited practice
    
    # ============ LOW EFFORT OVERALL ============
    
    # Very low previous scores + no effort = failing
    if previous_scores < 30 and hours_studied < 2 and sample_papers < 2:
        pred = min(pred, 15)  # Almost certainly failing
    elif previous_scores < 40 and hours_studied < 3 and sample_papers < 2:
        pred = min(pred, 25)  # Likely failing
    elif previous_scores < 50 and hours_studied < 4 and sample_papers < 3:
        pred = min(pred, 35)  # At risk of failing
    
    # ============ FINAL BOUNDS AND CAPS ============
    
    # Absolute bounds
    pred = max(0, min(100, pred))
    
    # Realistic improvement cap - can't improve more than 25 points without exceptional effort
    base_max = previous_scores + 25
    if hours_studied >= 8 and sample_papers >= 7 and 7 <= sleep_hours <= 9:
        base_max = previous_scores + 35  # Exceptional preparation allows more improvement
    elif hours_studied >= 6 and sample_papers >= 5 and 6 <= sleep_hours <= 10:
        base_max = previous_scores + 30  # Good preparation
    
    if pred > base_max:
        pred = base_max
    
    # Cannot exceed 100
    pred = min(100, pred)
    
    return pred


def classify_student(data: dict, predicted_score: float) -> dict:
    """Advanced student classification with detailed insights and high-level logic."""
    hours_studied = data.get("hours_studied", 0)
    sleep_hours = data.get("sleep_hours", 0)
    previous_scores = data.get("previous_scores", 0)
    sample_papers = data.get("sample_papers", 0)
    extracurricular = data.get("extracurricular", False)
    
    warnings = []
    recommendations = []
    risk_level = "Low"
    
    # ============ CRITICAL/IMPOSSIBLE SCENARIOS ============
    
    # Zero sleep - medical emergency
    if sleep_hours == 0:
        warnings.append("Zero sleep = cannot function")
        recommendations.append("Get sleep immediately")
        risk_level = "Critical"
        classification = "Medical Emergency"
        description = "Cannot perform without sleep."
        return {
            "classification": classification,
            "description": description,
            "risk_level": risk_level,
            "warnings": warnings,
            "recommendations": recommendations,
            "performance_gap": round(predicted_score - previous_scores, 2)
        }
    
    # Zero study with zero practice - complete failure
    if hours_studied == 0 and sample_papers == 0:
        warnings.append("No preparation")
        recommendations.append("Start studying now")
        risk_level = "Critical"
        classification = "Unprepared - Failing"
        description = "Will fail without preparation."
        return {
            "classification": classification,
            "description": description,
            "risk_level": risk_level,
            "warnings": warnings,
            "recommendations": recommendations,
            "performance_gap": round(predicted_score - previous_scores, 2)
        }
    
    # Excessive sleep (>14 hours) - health crisis
    if sleep_hours > 14:
        warnings.append("Excessive sleep (>14h)")
        recommendations.append("Consult a doctor")
        risk_level = "Critical"
        classification = "Health Crisis"
        description = "May indicate health issues."
        return {
            "classification": classification,
            "description": description,
            "risk_level": risk_level,
            "warnings": warnings,
            "recommendations": recommendations,
            "performance_gap": round(predicted_score - previous_scores, 2)
        }
    
    # ============ SEVERE SCENARIOS ============
    
    if sleep_hours < 3:
        warnings.append("Severe sleep deprivation")
        recommendations.append("Get 7-8 hours sleep")
        risk_level = "Critical"
    elif sleep_hours < 4:
        warnings.append("Dangerous sleep levels")
        recommendations.append("Increase sleep to 6-7h")
        risk_level = "Critical"
    elif sleep_hours < 5:
        warnings.append("Low sleep affects cognition")
        recommendations.append("Increase sleep")
        risk_level = "High"
    
    if hours_studied > 12 and sleep_hours < 6:
        warnings.append("Burnout risk")
        recommendations.append("Reduce study, rest more")
        risk_level = "High" if risk_level != "Critical" else risk_level
    
    if sleep_hours > 12:
        warnings.append("Oversleeping")
        recommendations.append("Check health")
        risk_level = "Medium" if risk_level == "Low" else risk_level
    
    if hours_studied == 0:
        warnings.append("No study time")
        recommendations.append("Study 4-5h daily")
        risk_level = "High" if risk_level not in ["Critical"] else risk_level
    elif hours_studied < 2:
        warnings.append("Insufficient study")
        recommendations.append("Study 3-4h daily")
        risk_level = "High" if risk_level == "Low" else risk_level
    
    if sample_papers == 0:
        recommendations.append("Practice sample papers")
    
    # ============ CLASSIFICATION LOGIC ============
    
    # Priority order: most severe first
    if sleep_hours < 3:
        classification = "Sleep Deprived - Critical"
        description = "Dangerously low sleep."
    elif hours_studied > 10 and sleep_hours < 5:
        classification = "Burnout - Critical"
        description = "Overworking without rest."
    elif sleep_hours < 5:
        classification = "Sleep Deprived"
        description = "Low sleep affects performance."
    elif hours_studied == 0:
        classification = "No Preparation"
        description = "No study time recorded."
    elif hours_studied < 2 and sample_papers < 2 and previous_scores < 50:
        classification = "At Risk - Failing"
        description = "Likely to fail."
    elif hours_studied < 2 and sample_papers < 2:
        classification = "At Risk"
        description = "Needs more preparation."
    elif sleep_hours > 12:
        classification = "Oversleeping"
        description = "May indicate health issues."
    elif hours_studied >= 7 and sample_papers >= 5 and 6 <= sleep_hours <= 9:
        classification = "High Performer"
        description = "Excellent balance."
    elif 4 <= hours_studied <= 8 and 7 <= sleep_hours <= 9 and extracurricular:
        classification = "Balanced Student"
        description = "Good work-life balance."
    elif hours_studied > 9 and not extracurricular and sleep_hours >= 6:
        classification = "Dedicated Learner"
        description = "Strong focus on academics."
    elif hours_studied < 3 and sleep_hours >= 8:
        classification = "Underprepared"
        description = "Needs more study time."
    elif hours_studied >= 4 and sample_papers >= 3 and sleep_hours >= 6:
        classification = "Adequate Preparation"
        description = "Room for improvement."
    else:
        classification = "Average Student"
        description = "Standard preparation."
    
    # Performance gap analysis
    performance_gap = predicted_score - previous_scores
    if performance_gap > 10:
        recommendations.append("Keep it up!")
    elif performance_gap < -10:
        recommendations.append("Review study methods")
        risk_level = "High" if risk_level == "Low" else risk_level
    elif performance_gap < -5:
        recommendations.append("Performance declining")
        risk_level = "Medium" if risk_level == "Low" else risk_level
    
    return {
        "classification": classification,
        "description": description,
        "risk_level": risk_level,
        "warnings": warnings,
        "recommendations": recommendations,
        "performance_gap": round(performance_gap, 2)
    }


def validate_input(data: dict) -> dict:
    """Enhanced validation with realistic constraint checking."""
    errors = {}
    warnings = []
    
    if "hours_studied" not in data:
        errors["hours_studied"] = "Required"
    elif not isinstance(data["hours_studied"], int) or not (0 <= data["hours_studied"] <= 24):
        errors["hours_studied"] = "Must be 0-24"
    elif data["hours_studied"] > 16:
        warnings.append("16h+ study is unhealthy")
    
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
    elif data["sleep_hours"] < 3:
        warnings.append("<3h sleep is dangerous")
    elif data["sleep_hours"] > 12:
        warnings.append(">12h sleep may indicate issues")
    
    if "sample_papers" not in data:
        errors["sample_papers"] = "Required"
    elif not isinstance(data["sample_papers"], int) or not (0 <= data["sample_papers"] <= 20):
        errors["sample_papers"] = "Must be 0-20"
    
    # Cross-field validation - provide warnings for extreme scenarios instead of blocking
    if not errors:
        hours_studied = data.get("hours_studied", 0)
        sleep_hours = data.get("sleep_hours", 0)
        sample_papers = data.get("sample_papers", 0)
        total_hours = hours_studied + sleep_hours
        
        # Allow but warn about impossible time combinations
        if total_hours > 24:
            warnings.append(f"Impossible: {total_hours}h total exceeds 24h/day")
        
        # Minimum realistic time for other activities
        if total_hours > 22 and total_hours <= 24:
            warnings.append(f"Only {24 - total_hours}h left for other activities")
        
        # Zero sleep warning
        if sleep_hours == 0:
            warnings.append("Zero sleep = cannot function")
        elif sleep_hours == 1:
            warnings.append("1h sleep = severe impairment")
        elif sleep_hours == 2:
            warnings.append("2h sleep = extreme fatigue")
        
        # Excessive study warning
        if hours_studied >= 20:
            warnings.append("20h+ study = physically impossible")
        elif hours_studied >= 16:
            warnings.append("16h+ study = extreme burnout")
        elif hours_studied >= 14:
            warnings.append("14h+ study = unsustainable")
        
        # Burnout combinations
        if hours_studied > 12 and sleep_hours < 4:
            warnings.append("Burnout crisis: too much study, no rest")
        elif hours_studied > 10 and sleep_hours < 5:
            warnings.append("Severe burnout risk")
        elif hours_studied > 8 and sleep_hours < 6:
            warnings.append("Study-sleep imbalance")
        
        # Excessive sleep
        if sleep_hours >= 20:
            warnings.append("20h+ sleep = health emergency")
        elif sleep_hours >= 16:
            warnings.append("16h+ sleep = possible illness")
        elif sleep_hours > 12:
            warnings.append("Excessive sleep (>12h)")
        
        # No preparation
        if hours_studied == 0 and sample_papers == 0:
            warnings.append("No preparation = will fail")
        elif hours_studied == 0:
            warnings.append("No study time")
        elif hours_studied < 2 and sample_papers < 2:
            warnings.append("Severely underprepared")
    
    return {"errors": errors, "warnings": warnings}


@csrf_exempt
@api_view(["POST"])
def predict_performance(request):
    """Advanced prediction endpoint with feature engineering and constraints."""
    
    validation_result = validate_input(request.data)
    if validation_result["errors"]:
        return Response({"errors": validation_result["errors"]}, status=400)
    
    try:
        model_data = joblib.load(MODEL_PATH)
        model = model_data['model']
        scaler = model_data['scaler']
        feature_columns = model_data['feature_columns']
    except FileNotFoundError:
        return Response({"error": "Model not found. Train the model first."}, status=500)
    except Exception as e:
        return Response({"error": f"Failed to load model: {str(e)}"}, status=500)
    
    data = request.data
    
    try:
        # Engineer features for prediction
        features_df = engineer_features_for_prediction(data)
        
        # Ensure correct feature order
        features_array = features_df[feature_columns].values
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        raw_prediction = model.predict(features_scaled)[0]
        
        # Apply realistic constraints
        adjusted_prediction = apply_realistic_constraints_single(raw_prediction, data)
        
        # Classify student
        student_analysis = classify_student(data, adjusted_prediction)
        
        # Build response
        response_data = {
            "predicted_performance_index": round(float(adjusted_prediction), 2),
            "student_classification": student_analysis["classification"],
            "description": student_analysis["description"],
            "risk_level": student_analysis["risk_level"],
            "performance_gap": student_analysis["performance_gap"],
            "analysis": {
                "warnings": student_analysis["warnings"],
                "recommendations": student_analysis["recommendations"]
            }
        }
        
        # Add validation warnings if any
        if validation_result["warnings"]:
            response_data["input_warnings"] = validation_result["warnings"]
        
        return Response(response_data)
        
    except Exception as exc:
        return Response({"error": f"Prediction failed: {str(exc)}"}, status=500)
