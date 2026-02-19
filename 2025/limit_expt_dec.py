import requests
import csv
import concurrent.futures
import time

CHALLENGE_URL = "https://limittheory.aictf.sg:5000"


def query(coconut_milk, eggs, sugar, pandan_leaves):
    time.sleep(1)  # Delay before making the request
    response = requests.post(
        f"{CHALLENGE_URL}/experiment",
        json={
            "coconut_milk": coconut_milk,
            "eggs": eggs,
            "sugar": sugar,
            "pandan_leaves": pandan_leaves
        },
    )
    return response.json()  # Assuming you want the JSON response


def process_row(row):
    print(f"Processing row: {row}")  # Print the current row being processed
    coconut_milk = float(row['coconut_milk'])
    eggs = float(row['eggs'])
    sugar = float(row['sugar'])
    pandan_leaves = float(row['pandan_leaves'])

    last_passed_value = None  # Variable to store the last PASSED value

    # Increase pandan leaves until we get a "FAILED" response
    while True:
        response = query(coconut_milk, eggs, sugar, pandan_leaves)

        if response.get('message') == "PASSED":
            last_passed_value = pandan_leaves  # Update the last passed value
        elif response.get('message') == "FAILED":
            break  # Stop when we hit a FAILED response

        # Increase pandan leaves by 0.1
        pandan_leaves += 1000.0

    # Return the last PASSED value if available
    if last_passed_value is not None:
        return {
            'coconut_milk': coconut_milk,
            'eggs': eggs,
            'sugar': sugar,
            'pandan_leaves': last_passed_value,
            'message': "PASSED"  # Indicate that the last value was PASSED
        }

    return None  # Return None if no passing value found


# Read the CSV file
input_file = 'input_data.csv'  # Change this to your input file name
output_file = 'output_data.csv'  # File to store results

with open(input_file, mode='r', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    rows = list(reader)  # Load all rows into a list for processing

# Open the output CSV file to store results
with open(output_file, mode='w', newline='') as csv_file:
    fieldnames = ['coconut_milk', 'eggs', 'sugar', 'pandan_leaves', 'message']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Use ThreadPoolExecutor to process rows in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(process_row, row): row for row in rows}

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                writer.writerow(result)

print("Processing complete. Results stored in output_data.csv.")