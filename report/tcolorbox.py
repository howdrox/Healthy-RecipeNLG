import re

def convert_to_tcolorbox(recipe_text):
    # Split out the four main sections by their headings
    sections = re.split(r"^## Recipe Title:|^Inputs \(base ingredients\):|^Ingredients:|^Instructions:",
                        recipe_text, flags=re.MULTILINE)
    # After splitting, sections will look like:
    # ["", " Title text\n\n", "\n   - item\n ...", "\n   - item\n ...", "\n\n 1. Step...\n2. Step..."]
    if len(sections) < 5:
        raise ValueError("Could not find all four sections. Check your headings!")
    
    # Pull them out (strip leading/trailing whitespace)
    title      = sections[1].strip()
    base_block = sections[2].strip()
    ingr_block = sections[3].strip()
    instr_block= sections[4].strip()
    
    # Helper to pull lines that start with a dash
    def parse_list(block):
        return [ line.lstrip().lstrip('–-').strip() 
                 for line in block.splitlines() 
                 if line.lstrip().startswith(('-', '–')) ]
    
    base_ingredients = parse_list(base_block)
    ingredients      = parse_list(ingr_block)
    
    # For instructions: grab every line that begins with a number + dot
    instructions = []
    for line in instr_block.splitlines():
        m = re.match(r"^\s*\d+\.\s*(.+)$", line)
        if m:
            instructions.append(m.group(1).strip())
    
    if not instructions:
        raise ValueError("No instruction steps found — check their formatting!")
    
    # Build the LaTeX tcolorbox
    out = []
    out.append(f"\\begin{{tcolorbox}}[recipebox={{{title}}}]")
    out.append(f"\t\\textbf{{Base Ingredients:}} {', '.join(base_ingredients)}\n")
    out.append("\t\\vspace{0.5em}")
    out.append("\t\\textbf{Ingredients:}")
    out.append("\t\\begin{itemize}")
    for item in ingredients:
        out.append(f"\t\t\\item {item}")
    out.append("\t\\end{itemize}\n")
    out.append("\t\\vspace{0.5em}")
    out.append("\t\\textbf{Instructions:}")
    out.append("\t\\begin{enumerate}")
    for step in instructions:
        out.append(f"\t\t\\item {step}")
    out.append("\t\\end{enumerate}")
    out.append("\\end{tcolorbox}")
    
    return "\n".join(out)



# Example usage
input_recipe = """## Recipe Title: Dried Beef And Pear Salad

Inputs (base ingredients):
   - chocolate
   - pickles
   - beef
   - pear

Ingredients:
   - 1 (4 oz.) pkg. chocolate or butterscotch pudding mix
   - 1/2 c. chopped pickles
   - 2 oz. jar dried beef, chopped
   - peel of 1/4 medium pear

Instructions:
   1. Mix pudding and pickle in a bowl.
   2. Add beef and pear. Chill.
"""

print(convert_to_tcolorbox(input_recipe))
