import random
import string

specials = "!$&?%"
digits = string.digits
letters = string.ascii_lowercase

special_chars = random.sample(specials, 3)
digit_chars = random.sample(digits, 3)
letter_chars = random.choices(letters, k=12 - 6)
all_chars = special_chars + digit_chars + letter_chars
random.shuffle(all_chars)

password = random.choice(string.ascii_uppercase) + ''.join(all_chars)
print(password)