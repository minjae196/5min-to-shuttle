import pandas as pd

def extract_travel_and_stop_times(file_path):
    """
    주어진 CSV 파일에서 bus_time별 평균과 표준편차를 계산하여
    travel_times, stop_times, arrival_rates, depart_rates를 생성합니다.

    Args:
        file_path (str): CSV 파일 경로.

    Returns:
        tuple: (travel_times, stop_times, arrival_rates, depart_rates)
    """
    # 데이터 읽기
    data = pd.read_csv(file_path)

    # bus_time별 평균과 표준편차 계산
    grouped_data = data.groupby('bus_time').agg(['mean', 'std'])
    grouped_data.columns = ['_'.join(col).strip() for col in grouped_data.columns.values]

    # 파라미터 생성
    travel_times = {}
    stop_times = {}
    arrival_rates = {}
    depart_rates = {}

    for time_slot in grouped_data.index:
        travel_time_data = []
        stop_time_data = []
        arrival_rate_data = []
        depart_rate_data = []

        # Travel times와 Stop times
        for i in range(1, 9):  # Assuming stops 1 to 9 for travel times
            travel_mean_col = f"{i}_to_{i+1}_mean"
            travel_std_col = f"{i}_to_{i+1}_std"
            if travel_mean_col in grouped_data.columns and travel_std_col in grouped_data.columns:
                travel_time_data.append((
                    grouped_data.at[time_slot, travel_mean_col],
                    grouped_data.at[time_slot, travel_std_col]
                ))
        
        for i in range(1, 10):  # Assuming stops 1 to 9 for stop times
            stop_mean_col = f"{i}_stop_time_mean"
            stop_std_col = f"{i}_stop_time_std"
            if stop_mean_col in grouped_data.columns and stop_std_col in grouped_data.columns:
                stop_time_data.append((
                    grouped_data.at[time_slot, stop_mean_col],
                    grouped_data.at[time_slot, stop_std_col]
                ))

        # Arrival rates와 Depart rates (10분 기준 그대로 사용)
        for i in range(1, 10):  # Assuming stops 1 to 9
            arrival_col = f"{i}_arrival_count_mean"
            depart_col = f"{i}_depart_count_mean"
            if arrival_col in grouped_data.columns:
                arrival_rate_data.append(grouped_data.at[time_slot, arrival_col])
            if depart_col in grouped_data.columns:
                depart_rate_data.append(grouped_data.at[time_slot, depart_col])

        travel_times[time_slot] = travel_time_data
        stop_times[time_slot] = stop_time_data
        arrival_rates[time_slot] = arrival_rate_data
        depart_rates[time_slot] = depart_rate_data

    return travel_times, stop_times, arrival_rates, depart_rates