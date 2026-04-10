from collections import defaultdict
from typing import Optional

from app.dependencies import DbSessionDep
from app.models import Lap, PitStop, RaceSession, SessionCar, Stint
from app.repositories import lap_crud, pit_crud, session_crud, stint_crud
from app.schemas import RaceReport, StintReport


def _tires_changed(pit: Optional[PitStop]) -> bool:
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


def _repairs_taken(pit: Optional[PitStop]) -> bool:
    if pit is None:
        return False
    return pit.required_repair_time > 0.0 or pit.optional_repair_time > 0.0


def _get_service_time(pit: Optional[PitStop]) -> Optional[float]:
    if pit is None or pit.service_end_time is None:
        return None

    return pit.service_end_time - pit.service_start_time


def _get_refuel_amount(pit: Optional[PitStop]) -> Optional[float]:
    if pit is None or pit.fuel_end_amount is None:
        return None

    return pit.fuel_end_amount - pit.fuel_start_amount


def _get_avg_laptime(times: list[float]) -> Optional[float]:
    if not times:
        return None

    return sum(times) / len(times)


def generate_race_summary(car: SessionCar, db: DbSessionDep) -> RaceReport:
    stint_reports = []
    stints: list[Stint] = stint_crud.get_many(
        db, Stint.session_id == car.session_id, Stint.car_id == car.car_id
    )
    pitstops: list[PitStop] = pit_crud.get_many(
        db, PitStop.session_id == car.session_id, PitStop.car_id == car.car_id
    )
    laps: list[Lap] = lap_crud.get_many(
        db, Lap.session_id == car.session_id, Lap.car_id == car.car_id
    )

    lap_times = defaultdict(list)
    pitstop_map = {}
    for p in pitstops:
        key = int(p.service_start_time)
        pitstop_map[key] = p

    for lap in laps:
        lap_times[lap.stint_id].append(lap.lap_time)

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

    session: RaceSession = session_crud.get_one(db, RaceSession.id == car.session_id)

    return RaceReport(
        session_id=car.session_id,
        session_date=session.session_date,
        race_duration=session.race_duration,
        track=session.track,
        car_class=car.car_class,
        car_name=car.car_name,
        stints=stint_reports,
    )
