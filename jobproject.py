import random
from collections import Counter
import psycopg2

# 1. Weekly colours data
weekly_colours = [
    "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
]

# 2. Flatten & count frequencies
all_colours = []
for day in weekly_colours:
    all_colours.extend([c.strip() for c in day.split(",")])

colour_counts = Counter(all_colours)

# 3. Mean, Median, Mode
mean_colour = colour_counts.most_common(1)[0][0]

sorted_list = sorted(all_colours)
n = len(sorted_list)
if n % 2 == 0:
    median_colour = (sorted_list[n // 2 - 1], sorted_list[n // 2])
else:
    median_colour = sorted_list[n // 2]

mode_colour = colour_counts.most_common(1)[0]  # (colour, count)

# 4. Variance
avg_freq = sum(colour_counts.values()) / len(colour_counts)
variance = sum((freq - avg_freq) ** 2 for freq in colour_counts.values()) / len(colour_counts)

# 5. Probability of RED
prob_red = colour_counts.get("RED", 0) / sum(colour_counts.values())

# 6. Save to PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "database": "bincomproject",  
    "user": "postgres",         
    "password": "#lionsdon'teatgrass"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS colour_frequency (
            colour TEXT PRIMARY KEY,
            frequency INT NOT NULL
        )
    """)

    # Insert or update colours
    for colour, freq in colour_counts.items():
        cur.execute("""
            INSERT INTO colour_frequency (colour, frequency)
            VALUES (%s, %s)
            ON CONFLICT (colour) DO UPDATE SET frequency = EXCLUDED.frequency
        """, (colour, freq))

    conn.commit()
    print("✅ Colours saved successfully to PostgreSQL.")
except Exception as e:
    print("⚠ Database error:", e)
finally:
    if 'conn' in locals():
        cur.close()
        conn.close()

# 7. Recursive Search
def recursive_search(data_list, target, index=0):
    if index >= len(data_list):
        return False
    if data_list[index] == target:
        return True
    return recursive_search(data_list, target, index + 1)

# 8. Random binary → decimal
binary_str = "".join(random.choice("01") for _ in range(4))
binary_decimal = int(binary_str, 2)

# 9. Fibonacci sum
def fib_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_total = fib_sum(50)

# 10. Special "1 appears 3 times" logic
input_seq = "0101101011101011011101101000111"
output_seq = ""

for i in range(len(input_seq)):
    if input_seq[i] == "1":
        window = input_seq[i:i+3]
        if window.count("1") == 3:
            output_seq += "1"
        else:
            output_seq += "0"
    else:
        output_seq += "0"

# 11. Print Results
print("Mean colour:", mean_colour)
print("Median colour:", median_colour)
print("Mode colour:", mode_colour)
print("Variance:", variance)
print(f"Probability of RED: {prob_red:.2%}")
print("Random binary:", binary_str, "-> Decimal:", binary_decimal)
print("Sum of first 50 Fibonacci numbers:", fib_total)
print("Special output sequence:", output_seq)
