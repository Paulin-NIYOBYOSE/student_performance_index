import joblib
import numpy as np
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

MODEL_PATH = "performance/model.pkl"


def validate_input(data: dict) -> None:
    required_fields = {
        "hours_studied": (int, (0, 24)),
        "previous_scores": (int, (0, 100)),
        "extracurricular": (bool, None),
        "sleep_hours": (int, (0, 24)),
        "sample_papers": (int, (0, 20)),
    }
    errors = {}
    for field, (field_type, value_range) in required_fields.items():
        if field not in data:
            errors[field] = "This field is required."
            continue
        value = data[field]
        if not isinstance(value, field_type):
            errors[field] = f"Must be of type {field_type.__name__}."
            continue
        if value_range and not (value_range[0] <= value <= value_range[1]):
            errors[field] = f"Must be between {value_range[0]} and {value_range[1]}."
    if errors:
        raise ValidationError(errors)


@api_view(["POST"])
def predict_performance(request: Request) -> Response:
    try:
        validate_input(request.data)
    except ValidationError as exc:
        return Response({"errors": exc.message_dict}, status=400)
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
    return Response({"predicted_performance_index": round(float(prediction), 2)})
