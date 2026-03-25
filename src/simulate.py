from datetime import datetime, timedelta
import random
import csv
import argparse
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

START_TIME = datetime(2026, 2, 25, 16, 50, 0)
INTERVAL_MINUTES = 1
DEFAULT_MINUTES = 60  #parameterization

def generate_cpu_usage():
    # Simulate normal load between 20% and 60%
    return round(random.uniform(20, 60), 2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=DEFAULT_MINUTES)
    args = parser.parse_args()

    total_points = args.minutes 

    current_time = START_TIME

    with open("data/telemetry.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cpu_usage"])

        for _ in range(total_points):
            writer.writerow([current_time.isoformat(), generate_cpu_usage()])
            current_time += timedelta(minutes=INTERVAL_MINUTES)

if __name__ == "__main__":
    main()
