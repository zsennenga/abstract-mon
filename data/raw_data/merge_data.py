import csv
import json
import os
import re


def read_csv_to_dict_list(filepath):
    """Read CSV file and return list of dictionaries."""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_dict_list_to_json(data, filepath):
    """Write list of dictionaries to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_effect_text(text, effect_chance=None):
    """Clean up effect text by removing markup, replacing placeholders, and removing newlines."""
    if not text:
        return text

    # Remove markup like [regular damage]{mechanic:regular-damage}
    text = re.sub(r"\[([^\]]+)\]\{[^}]+\}", r"\1", text)

    # Remove empty markup references like []{move:something}
    text = re.sub(r"\[\]\{[^}]+\}", "", text)

    # Replace $effect_chance% with actual percentage if available
    if effect_chance and "$effect_chance%" in text:
        text = text.replace("$effect_chance%", f"{effect_chance}%")

    # Remove newlines and replace with spaces
    text = re.sub(r"\n+", " ", text)

    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def main():
    data_dir = "."  # Current directory since we're already in raw_data

    # Read and process abilities
    print("Processing abilities...")
    abilities = read_csv_to_dict_list(os.path.join(data_dir, "abilities.csv"))
    ability_prose = read_csv_to_dict_list(os.path.join(data_dir, "ability_prose.csv"))

    # Filter for English only (local_language_id == 9)
    ability_prose_en = [row for row in ability_prose if row["local_language_id"] == "9"]

    # Create lookup dict for ability prose
    ability_prose_lookup = {row["ability_id"]: row for row in ability_prose_en}

    # Merge abilities with their English prose
    abilities_final = []
    for ability in abilities:
        prose = ability_prose_lookup.get(ability["id"])
        if prose:
            abilities_final.append(
                {
                    "id": ability["id"],
                    "name": ability["identifier"],
                    "effect": clean_effect_text(prose["effect"]),
                }
            )

    print("Processing items...")
    items = read_csv_to_dict_list(os.path.join(data_dir, "items.csv"))
    item_prose = read_csv_to_dict_list(os.path.join(data_dir, "item_prose.csv"))

    # Filter for English only (local_language_id == 9)
    item_prose_en = [row for row in item_prose if row["local_language_id"] == "9"]

    # Create lookup dict for item prose
    item_prose_lookup = {row["item_id"]: row for row in item_prose_en}

    # Merge items with their English prose, keeping fling data
    items_final = []
    for item in items:
        prose = item_prose_lookup.get(item["id"])
        if prose:
            items_final.append(
                {
                    "id": item["id"],
                    "name": item["identifier"],
                    "fling_power": item["fling_power"],
                    "fling_effect_id": item["fling_effect_id"],
                    "effect": clean_effect_text(prose["effect"]),
                }
            )

    print("Processing moves...")
    moves = read_csv_to_dict_list(os.path.join(data_dir, "moves.csv"))
    move_names = read_csv_to_dict_list(os.path.join(data_dir, "move_names.csv"))
    move_effect_prose = read_csv_to_dict_list(
        os.path.join(data_dir, "move_effect_prose.csv")
    )
    move_damage_classes = read_csv_to_dict_list(
        os.path.join(data_dir, "move_damage_classes.csv")
    )
    type_names = read_csv_to_dict_list(os.path.join(data_dir, "type_names.csv"))

    # Filter for English only (local_language_id == 9)
    move_names_en = [row for row in move_names if row["local_language_id"] == "9"]
    move_effect_prose_en = [
        row for row in move_effect_prose if row["local_language_id"] == "9"
    ]
    type_names_en = [row for row in type_names if row["local_language_id"] == "9"]

    # Create lookup dicts
    move_names_lookup = {row["move_id"]: row for row in move_names_en}
    move_effect_lookup = {row["move_effect_id"]: row for row in move_effect_prose_en}
    damage_class_lookup = {row["id"]: row for row in move_damage_classes}
    type_names_lookup = {row["type_id"]: row for row in type_names_en}

    # Process moves and merge with names and effects
    moves_final = []
    for move in moves:
        move_id = move["id"]
        name_data = move_names_lookup.get(move_id)
        effect_data = move_effect_lookup.get(move["effect_id"])
        damage_class_data = damage_class_lookup.get(move["damage_class_id"])
        type_data = type_names_lookup.get(move["type_id"])

        if name_data:  # Only include moves that have English names
            move_data = {
                "id": move_id,
                "name": name_data["name"],
                "power": move["power"] if move["power"] else None,
                "accuracy": move["accuracy"] if move["accuracy"] else None,
                "effect_chance": (
                    move["effect_chance"] if move["effect_chance"] else None
                ),
            }

            # Add type name if available
            if type_data:
                move_data["type"] = type_data["name"]

            # Add damage class if available
            if damage_class_data:
                move_data["damage_class"] = damage_class_data["identifier"]

            # Add effect if available
            if effect_data:
                move_data["effect"] = clean_effect_text(
                    effect_data["effect"], move["effect_chance"]
                )

            moves_final.append(move_data)

    # Save processed data to JSON files in the parent data folder
    print("Saving processed data...")
    write_dict_list_to_json(abilities_final, "../abilities.json")
    write_dict_list_to_json(items_final, "../items.json")
    write_dict_list_to_json(moves_final, "../moves.json")

    print(f"Processed {len(abilities_final)} abilities")
    print(f"Processed {len(items_final)} items")
    print(f"Processed {len(moves_final)} moves")

    # Display sample data
    print("\nSample abilities data:")
    for i, ability in enumerate(abilities_final[:3]):
        print(f"  {ability}")

    print("\nSample items data:")
    for i, item in enumerate(items_final[:3]):
        print(f"  {item}")

    print("\nSample moves data:")
    for i, move in enumerate(moves_final[:3]):
        print(f"  {move}")


if __name__ == "__main__":
    main()
