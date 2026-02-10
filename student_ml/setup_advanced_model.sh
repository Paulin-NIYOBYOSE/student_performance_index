#!/bin/bash

# Advanced Student Performance Prediction System Setup Script

echo "=========================================="
echo "Advanced Student Performance System Setup"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Run: source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "🗄️  Setting up database..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Failed to run migrations"
    exit 1
fi
echo "✓ Database ready"
echo ""

# Generate dataset
echo "📊 Generating enhanced dataset (200+ samples)..."
python manage.py generate_data --samples 200
if [ $? -ne 0 ]; then
    echo "❌ Failed to generate dataset"
    exit 1
fi
echo "✓ Dataset generated"
echo ""

# Load data
echo "📥 Loading data into database..."
python manage.py load_data
if [ $? -ne 0 ]; then
    echo "❌ Failed to load data"
    exit 1
fi
echo "✓ Data loaded"
echo ""

# Train model
echo "🤖 Training advanced ML model..."
echo "   (This may take 30-60 seconds)"
python manage.py train_model
if [ $? -ne 0 ]; then
    echo "❌ Failed to train model"
    exit 1
fi
echo "✓ Model trained"
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the server: python manage.py runserver"
echo "2. Test the API: python performance/test_predictions.py"
echo "3. Read ADVANCED_FEATURES.md for technical details"
echo ""
echo "API endpoint: http://127.0.0.1:8000/api/predict/"
echo ""
