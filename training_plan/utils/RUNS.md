# Training Plan Algorithm - MarathonMentor

This algorithm is designed to create a comprehensive training plan based on user inputs and predefined workout templates. The primary structure of the plan adheres to an 80/20 split between Base runs (long distance, steady-state) and Higher intensity runs, which include longer threshold/tempo runs and very short anaerobic runs. Recovery runs are also incorporated on recovery days and are considered optional.

## Run Formats:
- **zone (1-5)**: Heart rate zone to be in.
    * **1**: Z1 - Recovery
    * **2**: Z2 - Base
    * **3**: Z3 - Tempo
    * **4**: Z4 - High Tempo
    * **5**: Z5 - Interval/Anaerobic

- **feel (recovery, base, hard, max-effort)**: Subjective description of run intensity.
    * **recovery**: Low intensity, focused on easy movement and muscle recovery.
    * **base**: Steady state, building aerobic capacity.
    * **hard**: Pushing above comfortable limits, challenging but not maximal.
    * **max-effort**: Short bursts of all-out effort, maximizing anaerobic capacity.

- **duration (mins)**: Duration of the run in minutes.
- **distance (km)**: Distance of the run in kilometers.

## Run Types:
- **Recovery runs (Z1)**: Low intensity, aiding in muscle recovery and easy aerobic development.
- **Base runs (Z2)**: Steady-state runs building the foundational aerobic capacity.
- **Tempo runs (Z3 - Z4)**: Pushing the boundaries of aerobic capacity, running at or near the lactate threshold.
- **Interval runs (Z4 - Z5)**: Short, high-intensity intervals focused on anaerobic capacity and speed.

> **Note**: The actual training plan generated will consider user-specific inputs like current fitness level, target marathon time, availability, and other factors to tailor the plan to individual needs.

## NewMarathonPlan Class Overview:
This class represents a marathon training plan. It's split into three phases: Base, Peak 1, and Peak 2. Each phase focuses on different types of workouts, ranging from foundational aerobic exercises to intense peak performance preparations.

### Methods:

- **_validate_marathon_date()**: Validates the date of the marathon based on the difference from the current date.
- **_calculate_run_date(start_date, day_of_week, weeks_in_phase)**: Determines the date for a run based on its specified day of the week and the start date of the phase.
- **create_plan()**: Validates the marathon date and creates the marathon training plan.
- **create_runs_in_plan()**: Schedules the runs within the training plan based on the phases and their duration.
- **_schedule_runs_for_phase(phase, phase_start_date, weeks_in_phase)**: Schedules the runs for a specific phase.
- **_calculate_distance(run_id, fit_level, phase, weeks_in_phase, i)**: Calculates the distance of a run based on various parameters.
- **_calculate_interval_progression(fit_level, phase, weeks_in_phase, i, run_id)**: Calculates the progression of interval runs.
- **_calculate_duration()**: Placeholder for a method to calculate the duration of a run. (Currently not implemented)
- **_calculate_run_date(start_date, day_of_week, weeks_in_phase)**: Determines the date for a run based on its day of the week and the start date of the phase.

## Constants (from p_a_constants.py):
This file contains various constants used throughout the marathon training plan algorithm. This includes parameters for different fitness levels, various run attributes like zones and feelings, and default plans for different fitness levels.

---
