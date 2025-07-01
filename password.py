import random
import string
import os

# Clear console function for different operating systems
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Apply color formatting to password characters
def colorize(password, digits, symbols):
    result = ''
    for ch in password:
        if ch in digits:
            # Purple color for digits
            result += f'\033[38;2;148;111;242m{ch}\033[0m'
        elif ch in symbols:
            # Yellow color for symbols
            result += f'\033[38;2;242;217;102m{ch}\033[0m'
        else:
            result += ch
    return result

# Helper function for user input with prompt
def ask(prompt):
    return input(prompt + ' ').strip()

# Validate integer input within range
def ask_int(prompt, min_val, max_val):
    while True:
        val = ask(prompt)
        if val.isdigit():
            val = int(val)
            if min_val <= val <= max_val:
                return val
            print(f"Please enter a number between {min_val} and {max_val}.")
        else:
            print("Invalid input. Please enter a number.")

# Yes/No question handler
def ask_yn(prompt):
    while True:
        val = ask(prompt + " (y/n)").lower()
        if val in ['y', 'n']:
            return val == 'y'
        print("Please respond with 'y' or 'n'.")

# Multiple choice question handler
def ask_choice(prompt, options):
    while True:
        val = ask(f"{prompt} ({'/'.join(options)})")
        if val in options:
            return val
        print("Choose a valid option.")

# Main password generation logic
def generate_password(length, use_digits, use_symbols, start_type, digit_count, symbol_count):
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!$&?*"

    password_chars = []

    # Handle starting character based on user choice
    if start_type == '1':
        start_char = random.choice(string.ascii_uppercase)
    elif start_type == '2':
        start_char = random.choice(string.ascii_lowercase)
    elif start_type == '3':
        start_char = random.choice(digits)
    elif start_type == '4':
        start_char = random.choice(symbols)
    else:
        start_char = random.choice(string.ascii_letters)

    password_chars.append(start_char)

    # Adjust counts if starting character matches requirements
    if digit_count and start_char in digits:
        digit_count -= 1
    if symbol_count and start_char in symbols:
        symbol_count -= 1

    # Add required digits if specified
    if digit_count and digit_count > 0:
        available_digits = digits.replace(start_char, '') if start_char in digits else digits
        password_chars += random.sample(available_digits, k=min(digit_count, len(available_digits)))

    # Add required symbols if specified
    if symbol_count and symbol_count > 0:
        available_symbols = symbols.replace(start_char, '') if start_char in symbols else symbols
        password_chars += random.sample(available_symbols, k=min(symbol_count, len(available_symbols)))

    # Add random digits if enabled but no count specified
    if not digit_count and use_digits:
        max_digits = max(1, length // 5)
        password_chars += random.choices(digits, k=random.randint(1, max_digits))

    # Add random symbols if enabled but no count specified
    if not symbol_count and use_symbols:
        max_symbols = max(1, length // 6)
        password_chars += random.choices(symbols, k=random.randint(1, max_symbols))

    # Fill remaining characters
    remaining = length - len(password_chars)
    if remaining < 0:
        password_chars = password_chars[:length]
    elif remaining > 0:
        char_pool = list(letters)
        if use_digits and not digit_count:
            char_pool += list(digits)
        if use_symbols and not symbol_count:
            char_pool += list(symbols)
        
        char_pool = [c for c in char_pool if c != start_char]
        if char_pool:
            password_chars += random.choices(char_pool, k=remaining)

    # Shuffle all characters except first
    if len(password_chars) > 1:
        other_chars = password_chars[1:]
        random.shuffle(other_chars)
        password_chars = [password_chars[0]] + other_chars

    return ''.join(password_chars)

# Main program flow
def main():
    base_questions = 4
    extra_questions = 0
    current_question = 1

    # Get password length
    print(f"({current_question}/{base_questions}) What should be the password length?")
    length = ask_int("Enter a number between 8 and 32:", 8, 32)
    current_question += 1

    # Get digits preference
    print(f"({current_question}/{base_questions}) Do you want to include numbers?")
    use_digits = ask_yn("Include digits (0–9)?")
    current_question += 1

    # Get symbols preference
    print(f"({current_question}/{base_questions}) Do you want to include symbols?")
    use_symbols = ask_yn("Include symbols (! $ & ? *)?")
    current_question += 1

    # Check for advanced configuration
    print(f"({current_question}/{base_questions}) Do you want to apply additional rules?")
    advanced = ask_yn("Enable advanced configuration?")
    current_question += 1

    start_type = None
    digit_count = 0
    symbol_count = 0

    # Handle advanced configuration
    if advanced:
        extra_questions += 1
        if use_digits:
            extra_questions += 1
        if use_symbols:
            extra_questions += 1
        total_questions = base_questions + extra_questions

        # Get starting character type
        print(f"({current_question}/{total_questions}) Set password starting character.")
        start_type = ask_choice(
            "Choose starting type: 1 - Uppercase, 2 - Lowercase, 3 - Digit, 4 - Symbol",
            ['1', '2', '3', '4']
        )
        current_question += 1

        # Get exact digit count if enabled
        if use_digits:
            print(f"({current_question}/{total_questions}) Specify exact number of digits.")
            val = ask("Enter digit count or type 'n' to skip:")
            if val.isdigit():
                digit_count = min(int(val), length - 1)
            current_question += 1

        # Get exact symbol count if enabled
        if use_symbols:
            print(f"({current_question}/{total_questions}) Specify exact number of symbols.")
            val = ask("Enter symbol count or type 'n' to skip:")
            if val.isdigit():
                symbol_count = min(int(val), length - (digit_count if digit_count else 0) - 1)
            current_question += 1
    else:
        total_questions = base_questions

    # Password generation loop
    while True:
        password = generate_password(length, use_digits, use_symbols, start_type, digit_count, symbol_count)
        print("\nGenerated password:")
        print(colorize(password, string.digits, "!$&?*"))
        if ask_yn("\nDo you want to use this password?"):
            clear_console()
            print(password)
            break

if __name__ == "__main__":
    main()