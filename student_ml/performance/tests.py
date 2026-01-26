from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse


class PredictPerformanceTests(TestCase):
    @patch("performance.views.joblib.load")
    def test_predict_performance(self, mock_load):
        mock_model = MagicMock()
        mock_model.predict.return_value = [72.45]
        mock_load.return_value = mock_model

        response = self.client.post(
            reverse("predict-performance"),
            data={
                "hours_studied": 6,
                "previous_scores": 78,
                "extracurricular": True,
                "sleep_hours": 7,
                "sample_papers": 3,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predicted_performance_index": 72.45})
