from shuttle_simulation_v2 import ShuttleBusSimulationByTime
from extract_data import extract_travel_and_stop_times

if __name__ == "__main__":
    # 데이터 파일 경로
    file_path = "shuttlebus_data.csv"  # 기존 데이터 파일 경로를 입력하세요.

    # 데이터 추출
    travel_times, stop_times, arrival_rates, depart_rates = extract_travel_and_stop_times(file_path)

    # 시간대별 시뮬레이션 실행 (10분 단위로)
    time_simulation = ShuttleBusSimulationByTime(
        travel_times=travel_times,
        stop_times=stop_times,
        arrival_rates=arrival_rates,
        depart_rates=depart_rates,
        num_simulations=1000,  # 시뮬레이션 반복 횟수
        bus_capacity=40,  # 버스 용량 (40명)
    )

    # 모든 시뮬레이션 실행
    time_simulation.run_all_simulations()

    # 결과 출력
    time_simulation.display_results()