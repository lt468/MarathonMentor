#!/bin/zsh

# Check if autopep8 is installed
if ! command -v autopep8 &> /dev/null; then
    echo "autopep8 not found. Please install it using 'pip install autopep8'."
    exit 1
fi

# Find all Python files in the current directory and its subdirectories
python_files=($(find . -name "*.py" -not -path "./venv/*" -not -path "./training_plan/migrations/*"))

# Check if there are any Python files
if [ ${#python_files[@]} -eq 0 ]; then
    echo "No Python files found in the current directory and its subdirectories."
    exit 0
fi

# Run autopep8 on each Python file
for file in "${python_files[@]}"; do
    autopep8 --in-place "$file"
    echo "Formatted: $file"
done

echo "Autopep8 formatting complete."
