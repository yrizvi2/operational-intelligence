from datetime import datetime, timedelta
import random
import csv
import argparse #python built in library for parsing command-link arguments
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

START_TIME = datetime(2026, 2, 25, 16, 50, 0)
INTERVAL_MINUTES = 1
DEFAULT_MINUTES = 60  #parameterization

def generate_cpu_usage(index: int):
    # Inject a short CPU spike between minute 20 and minute 25
    if 20 <= index <= 25:
        return round(random.uniform(85, 95), 2)

    # Simulate normal load between 20% and 60%
    return round(random.uniform(20, 60), 2)

def generate_memory_usage():
    # Simulate normal memory usage between 40% and 80%
    return round(random.uniform(40, 80), 2)

def generate_latency_ms(index: int):
    # Inject a short latency spike during the same anomaly window
    if 20 <= index <= 25:
        return round(random.uniform(300, 500), 2)
        # Simulate normal latency between 80ms and 150ms
    return round(random.uniform(80, 150), 2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=DEFAULT_MINUTES)
    args = parser.parse_args()

    total_points = args.minutes 

    current_time = START_TIME

    with open("data/telemetry.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["timestamp", "cpu_usage", "memory_usage", "latency_ms"])

        for i in range(total_points):
            writer.writerow([
                current_time.isoformat(),
                generate_cpu_usage(i),
                generate_memory_usage(),
                generate_latency_ms(i)
            ])
            current_time += timedelta(minutes=INTERVAL_MINUTES)
            

if __name__ == "__main__":
    main()
