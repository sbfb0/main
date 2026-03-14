import re

# --- 1. THE LEXER (From Before) ---
token_patterns = [
    ('START',     r'start:sbfb'),       
    ('END',       r'<end>'),            
    ('KEYWORD',   r'idk|type|insert python'),
    ('STRING',    r'"[^"]*"'),                
    ('LPAREN',    r'\('),               
    ('RPAREN',    r'\)'),               
    ('WORD',      r'[a-zA-Z_.]+'),            
    ('SKIP',      r'[ \t\n]+'),               
    ('MISMATCH',  r'.'),                      
]

def tokenize(code):
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
    tokens = []
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP': continue
        elif kind == 'MISMATCH': raise RuntimeError(f"Syntax Error! sbfb doesn't understand: {value}")
        tokens.append((kind, value))
    return tokens

# --- 2. THE PARSER / INTERPRETER (New!) ---
def run_sbfb(tokens):
    print("--- Running sbfb Program ---")
    
    # We use an 'index' (i) to keep track of which token we are currently looking at
    i = 0
    while i < len(tokens):
        kind, value = tokens[i]
        
        if kind == 'START':
            # Just starting the program, move to the next token
            i += 1
            
        elif kind == 'END':
            # We hit <end>, so we stop running!
            print("--- Program Finished ---")
            break
            
        elif kind == 'KEYWORD' and value == 'idk':
            # We found 'idk'. The environment name (like 'frontend') is 2 steps ahead.
            # idk -> ( -> frontend
            env_name = tokens[i+2][1]
            print(f"[System Note: Setting up {env_name} environment...]")
            
            # Skip past 'idk', '(', 'frontend', and ')' to get to the next line
            i += 4 
            
        elif kind == 'KEYWORD' and value == 'type':
            # We found 'type'! The string we want to print is 2 steps ahead.
            # type -> ( -> "hello world"
            string_token = tokens[i+2][1]
            
            # Remove the quotation marks from the string
            clean_string = string_token.strip('"')
            
            # Actually print it to the screen!
            print(clean_string)
            
            # Skip past 'type', '(', '"hello world"', and ')'
            i += 4 
            
        else:
            # If it's something else, just move forward one step
            i += 1

# --- 3. TEST YOUR LANGUAGE ---
sbfb_code = """
start:sbfb
idk(frontend)

type ("hello world")
type ("sbfb is officially working!")

<end>
"""

# Run the lexer to get tokens
my_tokens = tokenize(sbfb_code)

# Run the parser to execute the code!
run_sbfb(my_tokens)
