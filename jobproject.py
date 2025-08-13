import random
from collections import Counter

# Colours from the table (each day as a string)
weekly_colours = [
    "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
]

# Flatten all colours into a single list
all_colours = []
for day in weekly_colours:
    parts = [c.strip() for c in day.split(",")]
    all_colours.extend(parts)

# Count frequency of each colour
colour_counts = Counter(all_colours)

# Mean colour → most frequent one
mean_colour = colour_counts.most_common(1)[0][0]

# Median colour → middle of sorted list
sorted_list = sorted(all_colours)
n = len(sorted_list)
if n % 2 == 0:
    median_colour = (sorted_list[n // 2 - 1], sorted_list[n // 2])
else:
    median_colour = sorted_list[n // 2]

# Mode colour (colour with highest frequency)
mode_colour = colour_counts.most_common(1)[0]  # (colour, count)

# Variance of colours
avg_freq = sum(colour_counts.values()) / len(colour_counts)
variance = sum((freq - avg_freq) ** 2 for freq in colour_counts.values()) / len(colour_counts)

# Probability of picking red at random
prob_red = colour_counts.get("RED", 0) / sum(colour_counts.values())

# Save to PostgreSQL (basic example)
import psycopg2
try:
    conn = psycopg2.connect(
        host="localhost",
        database="bincom_test",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS colour_frequency (colour TEXT, frequency INT)")
    cur.execute("DELETE FROM colour_frequency")
    for colour, freq in colour_counts.items():
        cur.execute("INSERT INTO colour_frequency (colour, frequency) VALUES (%s, %s)", (colour, freq))
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print("Database connection skipped:", e)

# Recursive search
def recursive_search(data_list, target, index=0):
    if index >= len(data_list):
        return False
    if data_list[index] == target:
        return True
    return recursive_search(data_list, target, index + 1)

# Random 4-digit binary → decimal
binary_str = "".join(random.choice("01") for _ in range(4))
binary_decimal = int(binary_str, 2)

# Fibonacci sum (first 50 terms)
def fib_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_total = fib_sum(50)

# Extra bit: detect if '1' appears exactly 3 times → output 1 else 0
input_seq = "0101101011101011011101101000111"
output_seq = ""
for i in range(len(input_seq)):
    if input_seq[i] == "1":
        # Count 1s in the current 3-char window (if possible)
        window = input_seq[i:i+3]
        if window.count("1") == 3:
            output_seq += "1"
        else:
            output_seq += "0"
    else:
        output_seq += "0"

# Results
print("Mean colour:", mean_colour)
print("Median colour:", median_colour)
print("Mode colour:", mode_colour)
print("Variance:", variance)
print(f"Probability of RED: {prob_red:.2%}")
print("Random binary:", binary_str, "-> Decimal:", binary_decimal)
print("Sum of first 50 Fibonacci numbers:", fib_total)
print("Special 1s detection output:", output_seq)
