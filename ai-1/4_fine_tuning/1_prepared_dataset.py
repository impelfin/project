import pandas as pd
import json

# 데이터 세트 준비
df = pd.read_csv(
    'tsukuyomi.csv',
    usecols=[1, 2],
    names=['prompt', 'completion'],
    skiprows=2)
df.to_json(
    "tsukuyomi.jsonl", 
    orient='records', 
    lines=True,
    force_ascii=False
)

def convert_to_new_format(old_data):
    new_data = []
    
    for entry in old_data:
        new_entry = {
            "messages": [
                {"role": "user", "content": entry["prompt"]},
                {"role": "assistant", "content": entry["completion"]}
            ]
        }
        new_data.append(new_entry)
        
    return new_data

# Load the old data
old_data = []
with open('tsukuyomi.jsonl', 'r') as file:
    for line in file:
        old_data.append(json.loads(line))

# Convert the old data to the new format
converted_data = convert_to_new_format(old_data)

# Save the converted data to a new file
with open('tsukuyomi_new.jsonl', 'w') as file:
    for entry in converted_data:
        file.write(json.dumps(entry, ensure_ascii=False) + '\n')

