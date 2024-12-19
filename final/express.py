import numpy as np
from scipy.stats import invgauss, burr, cauchy, norm, genpareto, logistic, genextreme, geom

class ShuttleBusSimulation:
    def __init__(self, num_stops=9, selected_stops=None, express_stops=None, arrival_distributions=None, 
                 depart_distributions=None, stop_time_distributions=None, travel_time_distributions=None, bus_capacity=40):
        self.num_stops = num_stops
        self.selected_stops = selected_stops if selected_stops else list(range(1, num_stops + 1))
        self.express_stops = express_stops if express_stops else []
        self.original_arrival_probs = [0.1477, 0.1947, 0.1583, 0.0969, 0.3929, 0.1930, 0.8800, 0.9167, 0.6111]
        self.original_depart_probs = [1.0000, 0.3333, 0.4490, 0.2178, 0.1176, 0.1692, 0.6286, 0.2444, 0.1947]
        self.arrival_distributions = arrival_distributions or [
            (lambda p: lambda: geom.rvs(p=p))(p) for p in self.original_arrival_probs
        ]
        self.depart_distributions = depart_distributions or [
            (lambda p: lambda: geom.rvs(p=p))(p) for p in self.original_depart_probs
        ]

        self.stop_time_distributions = stop_time_distributions or [lambda: 0 for _ in range(num_stops)]
        self.travel_time_distributions = travel_time_distributions or [
            lambda: invgauss.rvs(mu=25.47, scale=np.sqrt(178.75)/25.47, loc=33.711),
            lambda: invgauss.rvs(mu=105.42, scale=np.sqrt(4993.3)/105.42),
            lambda: burr.rvs(c=11.081, d=0.57773, loc=0, scale=123.18),
            lambda: cauchy.rvs(loc=177.26, scale=12.508),
            lambda: norm.rvs(loc=96.401, scale=16.862),
            lambda: genpareto.rvs(c=-0.49566, loc=196.64, scale=39.068),
            lambda: logistic.rvs(loc=48.301, scale=5.2597),
            lambda: genextreme.rvs(c=-0.33525, loc=22.453, scale=5.7636),
            lambda: genextreme.rvs(c=0.3512, loc=78.031, scale=5.9755)
        ]
        self.back_to_start_distribution = lambda: genextreme.rvs(c=0.3512, loc=78.031, scale=5.9755)
        self.bus_capacity = bus_capacity

        self.results = []  # List to store results for each bus trip
        self.passengers = 0

    def adjust_probabilities(self, original_probs, old_interval, new_interval):
        """
        Adjust probabilities for geometric distributions based on new interval.
        
        Args:
            original_probs (list): List of original probabilities (p values).
            old_interval (float): Original time interval (e.g., 10 minutes).
            new_interval (float): New time interval (e.g., 7 minutes).
        
        Returns:
            list: Adjusted probabilities for the new interval.
        """
        return [1 - (1 - (p)) ** (old_interval / new_interval) for p in original_probs]

    def update_intervals_for_express_stops(self, old_interval, new_interval):
        """
        Update arrival and departure distributions for express stops based on new interval.
        
        Args:
            old_interval (float): Original time interval (e.g., 10 minutes).
            new_interval (float): New time interval (e.g., 5 minutes).
        """
        adjusted_arrival_probs = self.adjust_probabilities(
            [self.original_arrival_probs[i - 1] for i in self.express_stops], old_interval, new_interval)
        adjusted_depart_probs = self.adjust_probabilities(
            [self.original_depart_probs[i - 1] for i in self.express_stops], old_interval, new_interval)

        for idx, stop in enumerate(self.express_stops):
            self.arrival_distributions[stop - 1] = (lambda p: lambda: geom.rvs(p=p))(adjusted_arrival_probs[idx])
            self.depart_distributions[stop - 1] = (lambda p: lambda: geom.rvs(p=p))(adjusted_depart_probs[idx])

    def simulate_stop(self, stop_number):
        if stop_number not in self.selected_stops:
            return {"boarded": 0, "alighted": 0, "stop_time": 0, "overflow": 0}

        arrival_distribution = self.arrival_distributions[stop_number - 1]
        passengers_boarding = arrival_distribution()

        total_passengers = self.passengers + passengers_boarding
        overflow = max(0, total_passengers - self.bus_capacity)
        passengers_boarding -= overflow
        self.passengers += passengers_boarding

        depart_distribution = self.depart_distributions[stop_number - 1]
        passengers_alighting = min(self.passengers, depart_distribution())
        self.passengers -= passengers_alighting

        stop_time = 2.877 * (passengers_boarding + passengers_alighting)

        # For stop 1, force alighting passengers to 0
        if stop_number == 1:
            passengers_alighting = 0

        return {
            "boarded": passengers_boarding,
            "alighted": passengers_alighting,
            "stop_time": stop_time,
            "overflow": overflow
        }

    def simulate_travel(self, start_stop, end_stop):
        travel_time = 0
        for stop in range(start_stop, end_stop):
            travel_time_distribution = self.travel_time_distributions[stop - 1]
            travel_time += travel_time_distribution()
        return travel_time

    def run_trip(self, start_time, express=False):
        trip_results = []
        current_time = start_time
        stops = self.express_stops if express else self.selected_stops

        for i in range(len(stops)):
            stop = stops[i]
            stop_result = self.simulate_stop(stop)

            # Calculate travel time to the next stop if applicable
            if i < len(stops) - 1:
                travel_time = self.simulate_travel(stop, stops[i + 1])
            else:
                travel_time = 0

            trip_results.append({
                "stop": stop,
                "time": current_time,
                **stop_result,
                "travel_time": travel_time
            })

            # Update current time
            current_time += stop_result["stop_time"] + travel_time

        # Add travel time back to the first stop
        travel_time_back = self.simulate_travel(stops[-1], self.num_stops + 1)
        trip_results.append({
            "stop": "Back to Start",
            "time": current_time,
            "boarded": 0,
            "alighted": 0,
            "stop_time": 0,
            "travel_time": travel_time_back,
            "overflow": 0
        })

        self.results.append(trip_results)

    def run(self, start_time, end_time, headway_minutes, num_simulations=1, express=False):
        for _ in range(num_simulations):
            headway_seconds = headway_minutes * 60
            current_time = start_time

            while current_time <= end_time:
                self.passengers = 0  # Reset passengers for each trip
                self.run_trip(current_time, express=express)
                current_time += headway_seconds

    def summarize_results_by_departure_time(self):
        results_by_departure = {}

        for trip in self.results:
            departure_time = trip[0]["time"]
            hours, minutes = divmod(departure_time // 60, 60)
            time_label = f"{hours:02}:{minutes:02}"

            if time_label not in results_by_departure:
                results_by_departure[time_label] = {stop: {"boarded": 0, "alighted": 0, "stop_time": 0, "travel_time": 0, "overflow": 0, "count": 0}
                                                    for stop in range(1, self.num_stops + 1)}
                results_by_departure[time_label]["Back to Start"] = {"boarded": 0, "alighted": 0, "stop_time": 0, "travel_time": 0, "overflow": 0, "count": 0}

            for result in trip:
                stop = result["stop"]
                results_by_departure[time_label][stop]["boarded"] += result["boarded"]
                results_by_departure[time_label][stop]["alighted"] += result["alighted"]
                results_by_departure[time_label][stop]["stop_time"] += result["stop_time"]
                results_by_departure[time_label][stop]["travel_time"] += result["travel_time"]
                results_by_departure[time_label][stop]["overflow"] += result["overflow"]
                results_by_departure[time_label][stop]["count"] += 1

        formatted_results = {}
        for time_label, stops_data in results_by_departure.items():
            formatted_results[time_label] = []
            for stop, data in stops_data.items():
                count = data["count"] if data["count"] > 0 else 1
                formatted_results[time_label].append({
                    "stop": stop,
                    "avg_boarded": data["boarded"] / count,
                    "avg_alighted": data["alighted"] / count,
                    "avg_stop_time": data["stop_time"] / count,
                    "avg_travel_time": data["travel_time"] / count if stop != "Back to Start" else data["travel_time"] / count,
                    "avg_overflow": data["overflow"] / count
                })

        return formatted_results

# Example usage of the updated simulation
simulation = ShuttleBusSimulation(num_stops=9, selected_stops=[1, 2, 3, 4, 5, 6, 7, 8, 9], express_stops=[1, 3, 5, 7, 9], bus_capacity=40)

# Adjust probabilities for 5-minute intervals only for express stops
simulation.update_intervals_for_express_stops(old_interval=10, new_interval=5)

# Define the schedule in seconds (11:30 -> 11:50 and 12:40 -> 13:40)
def time_to_seconds(hour, minute):
    return hour * 3600 + minute * 60

# Run the regular simulation
start_time_1 = time_to_seconds(11, 30)
end_time_1 = time_to_seconds(11, 50)
start_time_2 = time_to_seconds(12, 40)
end_time_2 = time_to_seconds(13, 40)
simulation.run(start_time=start_time_1, end_time=end_time_1, headway_minutes=10, num_simulations=1000, express=False)
simulation.run(start_time=start_time_2, end_time=end_time_2, headway_minutes=10, num_simulations=1000, express=False)

# Run the express simulation
express_times = [time_to_seconds(11, 35), time_to_seconds(11, 45), time_to_seconds(12, 45), time_to_seconds(12, 55),
                 time_to_seconds(13, 5), time_to_seconds(13, 15), time_to_seconds(13, 25), time_to_seconds(13, 35)]
for time in express_times:
    simulation.run(start_time=time, end_time=time, headway_minutes=10, num_simulations=1000, express=True)

# Summarize and print results
results_by_time = simulation.summarize_results_by_departure_time()
for time_label, stops_data in results_by_time.items():
    print(f"\n===== {time_label} 시간대 결과 =====")
    print("정류장 | 평균 탑승자 수 | 평균 하차자 수 | 평균 정차 시간 | 평균 이동 시간 | 평균 초과 인원")
    for stop_data in stops_data:
        print(f"{stop_data['stop']:>6} | {stop_data['avg_boarded']:>14.2f} | {stop_data['avg_alighted']:>14.2f} | "
              f"{stop_data['avg_stop_time']:>14.2f} | {stop_data['avg_travel_time']:>14} | {stop_data['avg_overflow']:>14.2f}")
