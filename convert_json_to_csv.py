import json
import csv

# Read the results.json file
with open('results.json', 'r') as f:
    results = json.load(f)

# Prepare data for CSV
csv_data = []

for puzzle_id, result in results.items():
    # Skip puzzles with errors
    if 'error' in result:
        continue
    
    # Create grid_solution as a JSON string
    grid_solution = {
        "header": result.get('headers', []),
        "rows": result.get('grid', [])
    }
    
    # Convert to JSON string (with double quotes escaped)
    grid_solution_str = json.dumps(grid_solution)
    
    # Get steps (default to 1000 if not present)
    steps = result.get('steps', 1000)
    
    csv_data.append({
        'id': puzzle_id,
        'grid_solution': grid_solution_str,
        'steps': steps
    })

# Sort by puzzle id for consistent ordering
csv_data.sort(key=lambda x: x['id'])

# Write to CSV file
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'grid_solution', 'steps'])
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Successfully converted {len(csv_data)} puzzles to results.csv")
print(f"Skipped {len(results) - len(csv_data)} puzzles with errors")
