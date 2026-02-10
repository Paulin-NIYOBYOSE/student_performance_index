"""
Test the advanced prediction model with various student scenarios.
"""
import requests
import json

API_URL = "http://127.0.0.1:8000/api/predict/"


def test_prediction(name, data):
    """Test a single prediction scenario."""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    print(f"Input: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def run_tests():
    """Run comprehensive test scenarios."""
    
    test_cases = [
        # Realistic scenarios
        ("Balanced High Performer", {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": True,
            "sleep_hours": 8,
            "sample_papers": 6
        }),
        
        ("Sleep Deprived Student", {
            "hours_studied": 8,
            "previous_scores": 70,
            "extracurricular": False,
            "sleep_hours": 3,
            "sample_papers": 5
        }),
        
        ("Burnout Risk", {
            "hours_studied": 14,
            "previous_scores": 75,
            "extracurricular": False,
            "sleep_hours": 4,
            "sample_papers": 10
        }),
        
        ("No Study at All", {
            "hours_studied": 0,
            "previous_scores": 60,
            "extracurricular": True,
            "sleep_hours": 10,
            "sample_papers": 0
        }),
        
        ("Oversleeper", {
            "hours_studied": 3,
            "previous_scores": 55,
            "extracurricular": False,
            "sleep_hours": 14,
            "sample_papers": 1
        }),
        
        ("Efficient Learner", {
            "hours_studied": 5,
            "previous_scores": 80,
            "extracurricular": True,
            "sleep_hours": 8,
            "sample_papers": 5
        }),
        
        ("Struggling Student", {
            "hours_studied": 2,
            "previous_scores": 35,
            "extracurricular": False,
            "sleep_hours": 6,
            "sample_papers": 1
        }),
        
        ("Perfect Balance", {
            "hours_studied": 6,
            "previous_scores": 90,
            "extracurricular": True,
            "sleep_hours": 8,
            "sample_papers": 7
        }),
        
        ("Underachiever", {
            "hours_studied": 1,
            "previous_scores": 75,
            "extracurricular": True,
            "sleep_hours": 10,
            "sample_papers": 0
        }),
        
        ("Extreme Burnout", {
            "hours_studied": 16,
            "previous_scores": 80,
            "extracurricular": False,
            "sleep_hours": 3,
            "sample_papers": 12
        }),
        
        # Edge cases
        ("Zero Everything", {
            "hours_studied": 0,
            "previous_scores": 40,
            "extracurricular": False,
            "sleep_hours": 2,
            "sample_papers": 0
        }),
        
        ("Maximum Effort", {
            "hours_studied": 10,
            "previous_scores": 95,
            "extracurricular": True,
            "sleep_hours": 8,
            "sample_papers": 10
        }),
    ]
    
    print("\n" + "="*60)
    print("ADVANCED STUDENT PERFORMANCE PREDICTION TESTS")
    print("="*60)
    
    for name, data in test_cases:
        test_prediction(name, data)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("Run: python manage.py runserver")
    input("\nPress Enter to start tests...")
    run_tests()
