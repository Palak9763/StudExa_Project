#!/bin/bash
# StudExa Setup Script — run this once after extracting the ZIP

echo "======================================"
echo "  StudExa — Student Progress Monitor"
echo "  Setup Script"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install django pillow

# Run migrations
echo ""
echo "🗄️  Setting up database..."
python3 manage.py makemigrations
python3 manage.py migrate

# Seed data
echo ""
echo "🌱 Seeding initial data..."
python3 manage.py seed_data

# Create media dirs
mkdir -p media/proofs media/profiles

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Run the server:  python3 manage.py runserver"
echo "Then open:       http://127.0.0.1:8000"
echo ""
echo "Login credentials:"
echo "  Admin:   admin@spms.com   / admin123"
echo "  Faculty: faculty@spms.com / faculty123"
echo "  Student: student@spms.com / student123"
echo "======================================"
