from shuttle_simulation import ShuttleBusSimulationByTime
from extract_data import extract_travel_and_stop_times

if __name__ == "__main__":
    # 데이터 파일 경로
    file_path = "shuttlebus_data.csv"  # 데이터 파일 이름을 실제 경로로 수정하세요.

    # 데이터 추출
    travel_times, stop_times, arrival_rates, depart_rates = extract_travel_and_stop_times(file_path)

    # 시간대별 시뮬레이션 실행
    time_simulation = ShuttleBusSimulationByTime(
        travel_times=travel_times,
        stop_times=stop_times,
        arrival_rates=arrival_rates,
        depart_rates=depart_rates,
        num_simulations=1000,  # 시뮬레이션 반복 횟수
    )

    # 모든 시뮬레이션 실행 및 결과 출력
    time_simulation.run_all_simulations()
    time_simulation.display_results()