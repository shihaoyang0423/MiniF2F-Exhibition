import json

input_file = 'minif2f_lean4.jsonl'
output_file = 'processed_minif2f.jsonl'

def process_file(input_path, output_path):
    processed_data = []
    with open(input_path, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile):
            try:
                data = json.loads(line.strip())
                processed_item = {
                    "id": data.get("id"),
                    "split": data.get("split"),
                    "informal_stmt": data.get("informal_stmt"),
                    "informal_proof": data.get("informal_proof"),
                    "name": data.get("name"),
                    "index": i + 1
                }
                processed_data.append(processed_item)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {i+1}: {e}")
                print(f"Problematic line: {line.strip()}")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for item in processed_data:
            outfile.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"Processed {len(processed_data)} items and saved to {output_path}")

if __name__ == "__main__":
    process_file(input_file, output_file)
