import re

def show_recipe(raw_text: str):
    # Helper to extract between two tags
    def extract_section(txt, start_tag, end_tag):
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        match = re.search(pattern, txt, flags=re.DOTALL)
        return match.group(1).strip() if match else ""

    # 1) Extract each chunk
    inputs_chunk       = extract_section(raw_text, "<INPUT_START>", "<INPUT_END>")
    ingredients_chunk  = extract_section(raw_text, "<INGR_START>", "<INGR_END>")
    instructions_chunk = extract_section(raw_text, "<INSTR_START>", "<INSTR_END>")
    title_chunk        = extract_section(raw_text, "<TITLE_START>", "<TITLE_END>")

    # 2) Split on their respective NEXT markers, if non-empty
    input_list = (
        [s.strip() for s in inputs_chunk.split("<NEXT_INPUT>")]
        if inputs_chunk
        else []
    )
    ing_list = (
        [s.strip() for s in ingredients_chunk.split("<NEXT_INGR>")]
        if ingredients_chunk
        else []
    )
    instr_list = (
        [s.strip() for s in instructions_chunk.split("<NEXT_INSTR>")]
        if instructions_chunk
        else []
    )

    # 3) Print in a clean format
    # print("\n" + "=" * 40)
    # print("\n")
    if title_chunk:
        print(f"## Recipe Title: {title_chunk}\n")

    if input_list:
        print("Inputs (base ingredients):")
        for inp in input_list:
            print(f"   - {inp}")
        print()  # blank line

    if ing_list:
        print("Ingredients:")
        for ing in ing_list:
            print(f"   - {ing}")
        print()

    if instr_list:
        print("Instructions:")
        for i, step in enumerate(instr_list, start=1):
            print(f"   {i}. {step}")
    # print("=" * 40 + "\n")