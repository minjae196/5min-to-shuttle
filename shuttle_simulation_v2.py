import numpy as np

class ShuttleBusSimulation:
    def __init__(self, num_stops=9, travel_times=None, arrival_rates=None, depart_rates=None, stop_times=None, bus_capacity=40):
        self.num_stops = num_stops
        self.travel_times = travel_times or [(5, 1) for _ in range(num_stops - 1)]
        self.arrival_rates = arrival_rates or [1.0 for _ in range(num_stops)]
        self.depart_rates = depart_rates or [0.5 for _ in range(num_stops)]
        self.stop_times = stop_times or [(10, 2) for _ in range(num_stops)]
        self.bus_capacity = bus_capacity

        self.results = {
            "boardings": [0] * self.num_stops,
            "alightings": [0] * self.num_stops,
            "stop_times": [0] * self.num_stops,
            "travel_times": [0] * (self.num_stops - 1),
            "overflows": [0] * self.num_stops,  # 초과 인원 누적
        }

        self.passengers = 0

    def simulate_stop(self, stop_number):
        arrival_rate = self.arrival_rates[stop_number - 1]
        passengers_boarding = np.random.poisson(arrival_rate)

        total_passengers = self.passengers + passengers_boarding
        if total_passengers > self.bus_capacity:
            overflow = total_passengers - self.bus_capacity
            self.results["overflows"][stop_number - 1] += overflow
            passengers_boarding -= overflow

        self.passengers += passengers_boarding
        self.results["boardings"][stop_number - 1] += passengers_boarding

        depart_rate = self.depart_rates[stop_number - 1]
        passengers_alighting = min(self.passengers, np.random.poisson(depart_rate))
        self.passengers -= passengers_alighting
        self.results["alightings"][stop_number - 1] += passengers_alighting

        mean, std = self.stop_times[stop_number - 1]
        stop_time = max(0, np.random.normal(mean, std))
        self.results["stop_times"][stop_number - 1] += stop_time

        return stop_time

    def simulate_travel(self, stop_number):
        if stop_number < self.num_stops:
            mean, std = self.travel_times[stop_number - 1]
            travel_time = max(0, np.random.normal(mean, std))
            self.results["travel_times"][stop_number - 1] += travel_time
            return travel_time
        return 0

    def run(self):
        total_time = 0
        for stop in range(1, self.num_stops + 1):
            total_time += self.simulate_stop(stop)
            if stop < self.num_stops:
                total_time += self.simulate_travel(stop)
        return total_time


class ShuttleBusSimulationByTime:
    def __init__(self, travel_times, stop_times, arrival_rates, depart_rates, num_simulations=1000, bus_capacity=40):
        self.travel_times = travel_times
        self.stop_times = stop_times
        self.arrival_rates = arrival_rates
        self.depart_rates = depart_rates
        self.num_simulations = num_simulations
        self.bus_capacity = bus_capacity
        self.results = {}

    def run_all_simulations(self):
        for time_slot in self.travel_times.keys():
            simulation_results = {
                "boardings": [0] * len(self.arrival_rates[time_slot]),
                "alightings": [0] * len(self.depart_rates[time_slot]),
                "stop_times": [0] * len(self.stop_times[time_slot]),
                "travel_times": [0] * len(self.travel_times[time_slot]),
                "overflows": [0] * len(self.arrival_rates[time_slot]),
            }

            for _ in range(self.num_simulations):
                simulation = ShuttleBusSimulation(
                    num_stops=len(self.arrival_rates[time_slot]),
                    travel_times=self.travel_times[time_slot],
                    arrival_rates=self.arrival_rates[time_slot],
                    depart_rates=self.depart_rates[time_slot],
                    stop_times=self.stop_times[time_slot],
                    bus_capacity=self.bus_capacity,
                )
                simulation.run()

                for i in range(len(self.arrival_rates[time_slot])):
                    simulation_results["boardings"][i] += simulation.results["boardings"][i]
                    simulation_results["alightings"][i] += simulation.results["alightings"][i]
                    simulation_results["stop_times"][i] += simulation.results["stop_times"][i]
                    simulation_results["overflows"][i] += simulation.results["overflows"][i]

                for i in range(len(self.travel_times[time_slot])):
                    simulation_results["travel_times"][i] += simulation.results["travel_times"][i]

            for key in simulation_results:
                simulation_results[key] = [x / self.num_simulations for x in simulation_results[key]]

            self.results[time_slot] = simulation_results

    def display_results(self):
        for time_slot, results in self.results.items():
            print(f"\n===== {time_slot} 시간대 결과 =====")
            print("정류장 | 평균 탑승자 수 | 평균 하차자 수 | 평균 정차 시간 | 평균 이동 시간 | 평균 초과 인원")
            for i in range(len(results["boardings"])):
                travel_time = results["travel_times"][i] if i < len(results["travel_times"]) else "-"
                formatted_travel_time = f"{travel_time:.2f}" if isinstance(travel_time, (int, float)) else travel_time
                print(f"{i+1:^7} | {results['boardings'][i]:^14.2f} | {results['alightings'][i]:^14.2f} | {results['stop_times'][i]:^14.2f} | {formatted_travel_time:^14} | {results['overflows'][i]:^14.2f}")