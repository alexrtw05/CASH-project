import nbformat as nbf
import random
import os

# ============================================================================
# CHALLENGE METADATA - Required for automatic challenge registration
# ============================================================================

challenge_metadata = {
    "title": "hello",
    "description": "A simple example challenge to demonstrate the challenge system. Extract hidden words from puzzles.",
    "imageURL": "/resources/python.jpg",
    "difficulty": "easy",
    "is_active": True,
}

# ============================================================================
# CONFIGURATION: One-word title for file naming (change when copying to hs25, fs26, etc.)
# ============================================================================
one_word_title = "example"

challenge_hints = {
    1: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl1_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": False,
    },
    2: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl2_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": False,
    },
    3: {
        "hintURL": f"/notebooks/{one_word_title}/{one_word_title}_lvl3_HASH.ipynb",
        "hintComment": "Download this jupyter notebook and open it in a Google Colab.",
        "hintImageURL": "/resources/python.jpg",
        "is_final": True,
    },
}




# ============================================================================
# TODO SECTION: Edit the word list below
# ============================================================================
# You can customize this word list to create your own challenge theme.
# The list should contain roughly 20 different code-related words (more is allowed).
# Each word will be randomly selected based on the challenge code/seed.
# Students will need to extract these words from the puzzle text.
#
# Example themes:
# - Programming concepts: "variable", "function", "loop", "class"
# - Animals: "elephant", "penguin", "dolphin", "tiger"
# - Languages: "python", "javascript", "rust", "golang"
#
# ADAPT:
# - words: Change the list items to your desired words
# ============================================================================

words = [
    "python", "coding", "challenge", "notebook", "jupyter",
    "function", "variable", "loop", "list", "string",
    "algorithm", "debug", "compile", "syntax", "module",
    "library", "import", "class", "object", "method"
]

# ============================================================================
# DO NOT MODIFY: The functions below are required for the challenge system
# ============================================================================

def get_solution(code, lvl):
    """Generate solution for each level based on code seed"""
    random.seed(code+lvl)
    return random.choice(words)

def get_hash(number):
    """Hash function for code validation"""
    return number % 20

# ============================================================================
# if you want, you can implement a custom solution checker function here, rather than just having the exact word match, might want to discuss this with the CASH team first though
#def check_solution(expected_code, submitted_code, level, user_hash):
#    """
#    Custom validation for TSP challenge.
#     Level 1: Float with 5% tolerance
#     Level 2: Float with 0.1% tolerance
#     """
#     try:
#         code_parsed = float(submitted_code)
#         expected = float(expected_code)
# 
#         if level == 1:
#             # 5% tolerance
#             return abs(code_parsed - expected) < 0.05 * expected
#         elif level == 2:
#             # 0.1% tolerance
#             return abs(code_parsed - expected) < 0.001 * expected
#         else:
#             return expected_code == submitted_code
#     except:
#         return False

#def get_solution(final_challenge_code, lvl):
#   if you decide to implemennt a custom checker then this function has to give the solution to a given level (based on the final_challenge_code keyword that is passed in generate_notebook_lvl), 
#   SO YOU NEED TO REPLACE THE GET_SOLUTION FUNCTION FROM ABOVE
#   the output of this get_soluiton() call will then be passed on to check_solution() as the expected_code variable,
#   so to summarize the variable in check_solution expected_code=get_solution(final_challenge_code, lvl) 
#   in the following as an example lvl1, will always be bazinga, lvl2 will be a character depending on the final_challenge_code, and lvl 3 will be some function depending on final_challenge_code
#    if lvl == 1:
#        return 'bazinga'
#    if lvl == 2:
#        return "abcdefghijklmnopqrstuvwxyz"[final_challenge_code%26]
#    if lvl == 3:
#        return final_challenge_code*239472+2
# as a fallback the solution will be the codeword (same as if you do not have a custom checker)
#    random.seed(code+lvl)
#    return random.choice(words)





def generate_notebook_lvl(final_challenge_code=1, solution=False, nb=None, level=1):
    # ---------------------------------------------------------
    # do not modify this section for generating the notebook file
    filename = f"{one_word_title}_lvl{level}_{final_challenge_code}.ipynb"
    if solution:
        filename = f"{one_word_title}_lvl{level}_solution.ipynb"

    print(f"Generating notebook {filename}...")
    os.makedirs(f"notebooks/{one_word_title}", exist_ok=True)
    filename = f"notebooks/{one_word_title}/" + filename

    with open(filename, "w") as f:
        nbf.write(nb, f)
    print(f"Notebook '{filename}' generated successfully!")


# ============================================================================
# END: DO NOT MODIFY
# ============================================================================


# ============================================================================
# TODO SECTION: Notebook Level Challenges
# ============================================================================
# Edit the challenge text to create the levels for your own challenge
# 
# Each level has to output a valid jupyter notebook, it can have multiple text sections,
# include text, load images, make requests import libraries have multiple subtasks etc, 
# you are free to create the challenge however you like. The template contains a very simple example with text and code cells
# - intro_text: The text shown to students (change the joke, instructions, hints)
# - code_message: The puzzle text containing the <word> or transformed word
#
# IMPORTANT: the correct code word is determined by calling "get_solution(code)"
#
# ADAPT the following functions:
# - generate_notebook_lvl1(): Customize level 1
# - generate_notebook_lvl2(): Customize level 2 
# - generate_notebook_lvl3(): Customize level 3 
# ============================================================================


def generate_notebook_lvl1(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text, jokes, and instructions for level 1
    # You can modify:
    # But keep the <word> placeholder so students extract the word from the word list
    # do not modify the solution extraction logic below -- of course we encourage you to modify the content of your challenge dynamically 
    # according to the chosen final code word

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 1)
    # --------------------------------

    """Level 1: Find the secret word"""
    nb = nbf.v4.new_notebook()

    # Header
    title_cell = nbf.v4.new_markdown_cell("## CASH Notebook")
    nb.cells.append(title_cell)

    # Challenge title
    challenge_cell = nbf.v4.new_markdown_cell("## Example Challenge LVL 1")

    # Get the solution word
    word = final_solution_word[::-1]

    # Intro text with joke and hint
    intro_text = f"""Welcome to the example template challenge this is level 1.

Why did the programmer quit his job? Because he didn't get arrays!

The secret token to find is: <{word}>
"""

    # Code cell with the challenge
    code_message = f"""text = '''Welcome to the example template challenge this is level 1.

Why did the programmer quit his job? Because he didn't get arrays!

The secret token to find is: <{word}>'''
"""

    # Template for student solution
    complete_code = """
# TODO: Extract the word between the < and > symbols
answer = ""
print(answer)
"""

    # Solution code
    solution_code = """
# Extract text between < and >
start = text.find('<') + 1
end = text.find('>')
answer = text[start:end][::-1]
print(answer)
"""
    # TODO: 
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell (will be for the master solution)
    nb.cells.append(challenge_cell)
    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))
    nb.cells.append(nbf.v4.new_code_cell(code_message))
    nb.cells.append(nbf.v4.new_code_cell(complete_code))

    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below



    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file

    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=1)

    # -----------------------------------------------------------------


def generate_notebook_lvl2(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text, jokes, and instructions for level 2
    # You can modify:
    # But keep the <word> placeholder so students extract the word from the word list
    # do not modify the solution extraction logic below -- of course we encourage you to modify the content of your challenge dynamically
    # according to the chosen final code word

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 2)
    # --------------------------------

    """Level 2: String reversal"""
    nb = nbf.v4.new_notebook()

    # Header
    title_cell = nbf.v4.new_markdown_cell("## CASH Notebook")
    nb.cells.append(title_cell)

    # Challenge title
    challenge_cell = nbf.v4.new_markdown_cell("## Example Challenge LVL 2")

    # Get the solution word
    word = final_solution_word[::-1]

    # Intro text with joke and hint
    intro_text = f"""Welcome to the example template challenge this is level 2.

Why do Java developers always wear glasses? Because they don't C#!

The secret token to find is: <{word}>
"""

    # Code cell with the challenge
    code_message = f"""text = '''Welcome to the example template challenge this is level 2.

Why do Java developers always wear glasses? Because they don't C#!

The secret token to find is: <{word}>'''
"""

    # Template for student solution
    complete_code = """
# TODO: Extract the word between the < and > symbols
answer = ""
print(answer)
"""

    # Solution code
    solution_code = """
# Extract text between < and >
start = text.find('<') + 1
end = text.find('>')
answer = text[start:end]
print(answer)
"""
    # TODO:
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell (will be for the master solution)
    nb.cells.append(challenge_cell)
    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))
    nb.cells.append(nbf.v4.new_code_cell(code_message))
    nb.cells.append(nbf.v4.new_code_cell(complete_code))

    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below



    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file

    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=2)

    # -----------------------------------------------------------------


def generate_notebook_lvl3(final_challenge_code=1, final_solution_flag=False):
    # TODO: Customize the challenge text, jokes, and instructions for level 3
    # You can modify:
    # But keep the <word> placeholder so students extract the word from the word list
    # do not modify the solution extraction logic below -- of course we encourage you to modify the content of your challenge dynamically
    # according to the chosen final code word

    # --------------------------------
    # Do not modify the solution token extraction logic
    final_solution_word = get_solution(final_challenge_code, 3)
    # --------------------------------

    """Level 3: Extract from uppercase"""
    nb = nbf.v4.new_notebook()

    # Header
    title_cell = nbf.v4.new_markdown_cell("## CASH Notebook")
    nb.cells.append(title_cell)

    # Challenge title
    challenge_cell = nbf.v4.new_markdown_cell("## Example Challenge LVL 3")

    # Get the solution word
    word = final_solution_word.upper()

    # Intro text with joke and hint
    intro_text = f"""Welcome to the example template challenge this is level 3.

How many programmers does it take to change a light bulb? None, that's a hardware problem!

The secret token to find is: <{word}>
"""

    # Code cell with the challenge
    code_message = f"""text = '''Welcome to the example template challenge this is level 3.

How many programmers does it take to change a light bulb? None, that's a hardware problem!

The secret token to find is: <{word}>'''
"""

    # Template for student solution
    complete_code = """
# TODO: Extract the word between the < and > symbols
answer = ""
print(answer)
"""

    # Solution code
    solution_code = """
# Extract text between < and >
start = text.find('<') + 1
end = text.find('>')
answer = text[start:end]
print(answer)
"""
    # TODO:
    # Make sure to build up the notebook cells, and if the final_solution_flag tag is set, include the solution code cell (will be for the master solution)
    nb.cells.append(challenge_cell)
    nb.cells.append(nbf.v4.new_markdown_cell(intro_text))
    nb.cells.append(nbf.v4.new_code_cell(code_message))
    nb.cells.append(nbf.v4.new_code_cell(complete_code))

    if final_solution_flag:
        nb.cells.append(nbf.v4.new_code_cell(solution_code))

    # note: the notebook must be stored in the variable nb for the function call below



    # -----------------------------------------------------------------
    # do not modify the following line for generating the notebook file

    generate_notebook_lvl(final_challenge_code, final_solution_flag, nb, level=3)

    # -----------------------------------------------------------------


# ============================================================================
# DO NOT MODIFY: Notebook generation and main execution
# ============================================================================

def gen_notebook(code=1, solution=False):
    """Generate all levels for a given code"""
    generate_notebook_lvl1(code, solution)
    generate_notebook_lvl2(code, solution)
    generate_notebook_lvl3(code, solution)


# Execute when run as a script
if __name__ == '__main__':
    # Generate solution notebooks
    gen_notebook(code=1, solution=True)

    # Generate challenge notebooks for different codes
    for i in range(20):
        gen_notebook(code=i, solution=False)

    print("All notebooks generated successfully!")
    print(f"You can find them in the notebooks/{one_word_title}/ directory.")

# ============================================================================
# END: DO NOT MODIFY
# ============================================================================
