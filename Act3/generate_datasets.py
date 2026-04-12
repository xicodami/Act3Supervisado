from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

STATIONS = [
    ('ST01','Portal Norte','terminal'),
    ('ST02','Lago Azul','intermedia'),
    ('ST03','Centro Histórico','central'),
    ('ST04','Universidad','intermedia'),
    ('ST05','San Pedro','intermedia'),
    ('ST06','Parque Industrial','industrial'),
    ('ST07','Aeropuerto','terminal'),
    ('ST08','Terminal Sur','terminal'),
    ('ST09','Villa Nueva','barrial'),
    ('ST10','Hospital Central','central'),
    ('ST11','Mercado Distrital','barrial'),
    ('ST12','Tecnoparque','industrial'),
]

ROUTES = {
    'R1': ['ST01','ST02','ST03','ST04','ST05'],
    'R2': ['ST03','ST10','ST11','ST08'],
    'R3': ['ST02','ST09','ST08'],
    'R4': ['ST04','ST12','ST06','ST07'],
    'R5': ['ST05','ST10','ST06']
}

DISTANCE_BETWEEN_STATIONS = {
    ('ST01','ST02'): 3.2, ('ST02','ST03'): 2.8, ('ST03','ST04'): 2.4, ('ST04','ST05'): 3.1,
    ('ST03','ST10'): 2.1, ('ST10','ST11'): 1.8, ('ST11','ST08'): 4.0,
    ('ST02','ST09'): 3.5, ('ST09','ST08'): 5.2,
    ('ST04','ST12'): 4.3, ('ST12','ST06'): 3.0, ('ST06','ST07'): 6.1,
    ('ST05','ST10'): 2.7, ('ST10','ST06'): 3.4
}

DAY_TYPES = ['weekday','saturday','sunday']
HOUR_BLOCKS = ['05-07','07-09','09-12','12-15','15-18','18-21','21-23']
WEATHER_CONDITIONS = ['clear','rain','heavy_rain']
TRAFFIC_LEVELS = ['low','medium','high']
PEAK_BLOCKS = {'07-09','15-18','18-21'}

def build_network_helpers():
    station_df = pd.DataFrame(STATIONS, columns=['station_id','station_name','station_type'])
    station_type_map = dict(zip(station_df.station_id, station_df.station_type))
    station_name_map = dict(zip(station_df.station_id, station_df.station_name))

    dist_map = {}
    for (a, b), d in DISTANCE_BETWEEN_STATIONS.items():
        dist_map[(a, b)] = d
        dist_map[(b, a)] = d

    route_lookup = {}
    for route_id, stops in ROUTES.items():
        for idx, station_id in enumerate(stops):
            route_lookup.setdefault(station_id, []).append((route_id, idx))

    return station_df, station_type_map, station_name_map, dist_map, route_lookup

def find_trip(origin, destination, dist_map, route_lookup):
    if origin == destination:
        return None

    shared = []
    for route_id, idx_o in route_lookup.get(origin, []):
        for route_id_2, idx_d in route_lookup.get(destination, []):
            if route_id == route_id_2:
                segment_count = abs(idx_d - idx_o)
                if segment_count > 0:
                    stops = ROUTES[route_id]
                    step = 1 if idx_d > idx_o else -1
                    distance_km = 0.0
                    i = idx_o
                    while i != idx_d:
                        a = stops[i]
                        b = stops[i + step]
                        distance_km += dist_map[(a, b)]
                        i += step
                    shared.append((segment_count, distance_km, route_id))
    if shared:
        segment_count, distance_km, route_id = sorted(shared, key=lambda x: (x[0], x[1]))[0]
        return route_id, segment_count, 0, round(distance_km, 2)

    best = None
    for route_o, idx_o in route_lookup.get(origin, []):
        for route_d, idx_d in route_lookup.get(destination, []):
            if route_o == route_d:
                continue
            common_stations = set(ROUTES[route_o]).intersection(ROUTES[route_d])
            for transfer_station in common_stations:
                idx_t_o = ROUTES[route_o].index(transfer_station)
                idx_t_d = ROUTES[route_d].index(transfer_station)
                segment_count = abs(idx_t_o - idx_o) + abs(idx_d - idx_t_d)
                if segment_count <= 0:
                    continue

                distance_km = 0.0
                step = 1 if idx_t_o > idx_o else -1
                i = idx_o
                while i != idx_t_o:
                    a = ROUTES[route_o][i]
                    b = ROUTES[route_o][i + step]
                    distance_km += dist_map[(a, b)]
                    i += step

                step = 1 if idx_d > idx_t_d else -1
                i = idx_t_d
                while i != idx_d:
                    a = ROUTES[route_d][i]
                    b = ROUTES[route_d][i + step]
                    distance_km += dist_map[(a, b)]
                    i += step

                candidate = (segment_count, distance_km, f'{route_o}+{route_d}')
                if best is None or (segment_count, distance_km) < (best[0], best[1]):
                    best = candidate

    if best:
        segment_count, distance_km, route_id = best
        return route_id, segment_count, 1, round(distance_km, 2)

    return None

def generate_datasets(n_rows=1800, seed=42):
    rng = np.random.default_rng(seed)
    station_df, station_type_map, station_name_map, dist_map, route_lookup = build_network_helpers()
    station_ids = station_df.station_id.tolist()

    station_df.to_csv(DATA_DIR / 'stations_reference.csv', index=False)
    pd.DataFrame([(route_id, ' -> '.join(stops)) for route_id, stops in ROUTES.items()], columns=['route_id', 'path']).to_csv(
        DATA_DIR / 'routes_reference.csv', index=False
    )

    records = []
    for i in range(n_rows):
        while True:
            origin, destination = rng.choice(station_ids, size=2, replace=False)
            trip = find_trip(origin, destination, dist_map, route_lookup)
            if trip is not None:
                break

        route_id, segment_count, transfer_count, distance_km = trip
        day_type = rng.choice(DAY_TYPES, p=[0.66, 0.18, 0.16])
        hour_block = rng.choice(HOUR_BLOCKS, p=[0.10, 0.18, 0.18, 0.16, 0.18, 0.15, 0.05])
        is_peak_hour = int(hour_block in PEAK_BLOCKS)
        weather_condition = rng.choice(WEATHER_CONDITIONS, p=[0.73, 0.21, 0.06])

        if is_peak_hour and weather_condition != 'clear':
            traffic_level = rng.choice(TRAFFIC_LEVELS, p=[0.02, 0.28, 0.70])
        elif is_peak_hour:
            traffic_level = rng.choice(TRAFFIC_LEVELS, p=[0.08, 0.37, 0.55])
        elif day_type == 'sunday':
            traffic_level = rng.choice(TRAFFIC_LEVELS, p=[0.62, 0.30, 0.08])
        else:
            traffic_level = rng.choice(TRAFFIC_LEVELS, p=[0.28, 0.52, 0.20])

        station_type_origin = station_type_map[origin]
        station_type_destination = station_type_map[destination]

        travel_time = 6.5 + distance_km * 1.55 + (distance_km ** 1.18) * 0.42
        travel_time += segment_count * 1.35
        travel_time += transfer_count * 7.8
        travel_time += {'low': 0.0, 'medium': 2.8, 'high': 7.0}[traffic_level]

        if traffic_level == 'high' and distance_km > 7:
            travel_time += 0.9 * (distance_km - 7)
        if weather_condition == 'rain':
            travel_time += 1.8
        elif weather_condition == 'heavy_rain':
            travel_time += 4.6 + 0.4 * segment_count
        if weather_condition == 'heavy_rain' and traffic_level == 'high':
            travel_time += 4.5
        if is_peak_hour:
            travel_time += 3.2
        if is_peak_hour and transfer_count > 0:
            travel_time += 2.0
        if day_type == 'sunday':
            travel_time -= 2.1
        elif day_type == 'saturday':
            travel_time -= 0.8
        if station_type_origin == 'terminal' and station_type_destination == 'central':
            travel_time += 2.4
        if station_type_origin == 'industrial' or station_type_destination == 'industrial':
            travel_time += 1.4
        if 'R4' in route_id and hour_block in {'15-18', '18-21'}:
            travel_time += 3.0
        if 'R2' in route_id and weather_condition != 'clear':
            travel_time += 1.5
        if distance_km > 10 and transfer_count > 0:
            travel_time += 3.5

        noise = float(rng.normal(0, 1.0 + 0.18 * segment_count + 0.8 * transfer_count))
        travel_time += noise
        travel_time_min = max(8, round(travel_time, 2))

        records.append({
            'trip_id': f'TRIP_{i + 1:04d}',
            'origin_station': station_name_map[origin],
            'destination_station': station_name_map[destination],
            'route_id': route_id,
            'day_type': day_type,
            'hour_block': hour_block,
            'distance_km': round(distance_km, 2),
            'segment_count': int(segment_count),
            'transfer_count': int(transfer_count),
            'is_peak_hour': int(is_peak_hour),
            'weather_condition': weather_condition,
            'traffic_level': traffic_level,
            'station_type_origin': station_type_origin,
            'station_type_destination': station_type_destination,
            'travel_time_min': travel_time_min,
        })

    supervised_df = pd.DataFrame(records)
    supervised_df.to_csv(DATA_DIR / 'transport_supervised_dataset.csv', index=False)

    unsupervised_df = supervised_df[
        ['trip_id', 'distance_km', 'segment_count', 'transfer_count', 'is_peak_hour',
         'traffic_level', 'day_type', 'weather_condition', 'hour_block']
    ].copy()
    unsupervised_df.to_csv(DATA_DIR / 'transport_unsupervised_dataset.csv', index=False)

    print('Datasets generados correctamente en la carpeta data/')

if __name__ == '__main__':
    generate_datasets()