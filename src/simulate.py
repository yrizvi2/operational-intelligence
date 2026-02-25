from datetime import datetime, timedelta
import random
import csv
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

START_TIME = datetime(2026, 2, 25, 16, 50, 0)
INTERVAL_MINUTES = 1
TOTAL_POINTS = 60  # 1 hour for now

def generate_cpu_usage():
    # Simulate normal load between 20% and 60%
    return round(random.uniform(20, 60), 2)

def main():
    current_time = START_TIME

    with open("data/telemetry.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cpu_usage"])

        for _ in range(TOTAL_POINTS):
            writer.writerow([current_time.isoformat(), generate_cpu_usage()])
            current_time += timedelta(minutes=INTERVAL_MINUTES)

if __name__ == "__main__":
    main()
