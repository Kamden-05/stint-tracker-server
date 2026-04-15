from collections import defaultdict
from typing import Optional

from app.dependencies import DbSessionDep
from app.models import Laps, PitStops, Sessions, SessionCars, Stints
from app.repositories import lap_crud, pit_crud, session_crud, stint_crud
from app.schemas import RaceReport, StintReport


def _tires_changed(pit: Optional[PitStops]) -> bool:
    if pit is None:
        return False

    return any(
        [
            pit.left_front_tire_change,
            pit.right_front_tire_change,
            pit.left_rear_tire_change,
            pit.right_rear_tire_change,
        ]
    )


def _repairs_taken(pit: Optional[PitStops]) -> bool:
    if pit is None:
        return False
    return pit.required_repair_time > 0.0 or pit.optional_repair_time > 0.0


def _get_service_time(pit: Optional[PitStops]) -> Optional[float]:
    if pit is None or pit.service_end_time is None:
        return None

    return pit.service_end_time - pit.service_start_time


def _get_refuel_amount(pit: Optional[PitStops]) -> Optional[float]:
    if pit is None or pit.fuel_end_amount is None:
        return None

    return pit.fuel_end_amount - pit.fuel_start_amount


def _get_avg_laptime(times: list[float]) -> Optional[float]:
    if not times:
        return None

    return sum(times) / len(times)


def generate_race_summary(car: SessionCars, db: DbSessionDep) -> RaceReport:
    stint_reports = []
    stints: list[Stints] = stint_crud.get_many(
        db, Stints.session_id == car.session_id, Stints.car_id == car.car_id
    )
    pitstops: list[PitStops] = pit_crud.get_many(
        db, PitStops.session_id == car.session_id, PitStops.car_id == car.car_id
    )
    laps: list[Laps] = lap_crud.get_many(
        db, Laps.session_id == car.session_id, Laps.car_id == car.car_id
    )

    lap_times = defaultdict(list)
    pitstop_map = {}
    for p in pitstops:
        key = int(p.service_start_time)
        pitstop_map[key] = p

    for i, lap in enumerate(laps):
        derived_time = None

        if lap.lap_time > 0:
            derived_time = lap.lap_time
        else:
            if i > 0:
                derived_time = lap.end_time - laps[i - 1].end_time
            else:
                stint = next((s for s in stints if s.id == laps.stint_id), None)
                if stint:
                    derived_time = lap.end_time - stint.start_time

        if derived_time is not None:
            lap_times[lap.stint_id].append(derived_time)

    for stint in stints:
        p_key = int(stint.end_time)
        pitstop = pitstop_map.get(p_key, None)

        stint_lap_times = lap_times[stint.id]

        stint_report = StintReport(
            driver_name=stint.driver_name,
            start_time=stint.start_time,
            duration=(
                stint.end_time - stint.start_time
                if stint.end_time is not None
                else None
            ),
            num_laps=len(stint_lap_times),
            avg_lap_time=_get_avg_laptime(stint_lap_times),
            fastest_lap_time=min(stint_lap_times) if stint_lap_times else None,
            out_lap_time=stint_lap_times[0] if stint_lap_times else None,
            in_lap_time=stint_lap_times[-1] if stint_lap_times else None,
            start_fuel=stint.start_fuel,
            end_fuel=stint.end_fuel,
            refuel_amount=_get_refuel_amount(pitstop),
            tire_change=_tires_changed(pitstop),
            repairs=_repairs_taken(pitstop),
            service_time=_get_service_time(pitstop),
            num_incidents=(
                stint.end_incidents - stint.start_incidents
                if stint.end_incidents is not None
                else None
            ),
            start_position=stint.start_position,
            end_position=stint.end_position,
        )

        stint_reports.append(stint_report)

    session: Sessions = session_crud.get_one(db, Sessions.id == car.session_id)

    return RaceReport(
        session_id=car.session_id,
        session_date=session.session_date,
        race_duration=session.race_duration,
        track=session.track,
        car_class=car.car_class,
        car_name=car.car_name,
        stints=stint_reports,
    )
