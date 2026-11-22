"""абораторна робота 2. 'ять завдань з  у Python."""

import argparse
import sys

import task1_vehicles
import task2_sensor
import task3_vector
import task4_orders
from task5_queue import FirstInFirstOut, PrinterQueue, PrintJob, ShortestFirst
from task5_urgent import UrgentFirst


def demo_print_queue() -> None:
    jobs = [
        PrintJob("віт", 12, 0),
        PrintJob("Тези", 2, 1),
        PrintJob("аява", 5, 2, urgent=True),
        PrintJob("одаток", 3, 3),
    ]
    queue = PrinterQueue(FirstInFirstOut())
    print("окументи в черзі")
    for job in jobs:
        queue.add(job)
        label = " (терміново)" if job.urgent else ""
        print(f"  {job.title}: {job.pages} стор., хвилина {job.arrival_minute}{label}")

    print("\nорядок друку")
    for label, strategy in [
        ("FIFO", FirstInFirstOut()),
        ("Спочатку короткі", ShortestFirst()),
        ("Спочатку термінові (нова стратегія)", UrgentFirst()),
    ]:
        queue.set_strategy(strategy)
        names = " → ".join(job.title for job in queue.print_order())
        print(f"  {label}: {names}")


def main() -> None:
    tasks = {
        "1": ("аслідування та поліморфізм", task1_vehicles.demo),
        "2": ("Інкапсуляція та властивості", task2_sensor.demo),
        "3": ("агічні методи Vector2D", task3_vector.demo),
        "4": ("бстрактні класи та композиція", task4_orders.demo),
        "5": ("атерн Strategy для черги друку", demo_print_queue),
    }
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=["all", *tasks], default="all",
                        help="омер завдання. Типово запускаються всі завдання.")
    selected = parser.parse_args().task
    for number, (title, demo) in tasks.items():
        if selected in ("all", number):
            print(f"\nЯ {number}. {title}")
            print("-" * 58)
            demo()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
