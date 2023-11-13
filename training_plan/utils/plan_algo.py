"""
Module implementing the MarathonMentor training plan algorithm.

This module defines the NewMarathonPlan class, which is responsible for creating a new marathon training plan
for a user based on their fitness level and the date of their marathon.

Training Plan Algorithm - MarathonMentor

This algorithm is designed to create a comprehensive training plan based on user inputs and predefined workout templates. The primary structure of the plan adheres to an 80/20 split between Base runs (long distance, steady-state) and Higher intensity runs, which include longer threshold/tempo runs and very short anaerobic runs. Recovery runs are also incorporated on recovery days and are considered optional.

The actual training plan generated will consider user-specific inputs like current fitness level, target marathon time, availability, and other factors to tailor the plan to individual needs.

Run Formats:
- zone (1-5): Heart rate zone to be in.
  * 1: Z1 - Recovery
  * 2: Z2 - Base
  * 3: Z3 - Tempo
  * 4: Z4 - High Tempo
  * 5: Z5 - Interval/Anaerobic

- feel (recovery, base, hard, max-effort): Subjective description of run intensity.
  * recovery: Low intensity, focused on easy movement and muscle recovery.
  * base: Steady state, building aerobic capacity.
  * hard: Pushing above comfortable limits, challenging but not maximal.
  * max-effort: Short bursts of all-out effort, maximizing anaerobic capacity.

- duration (mins): Duration of the run in minutes.
- distance (km): Distance of the run in kilometers.

Run Types:
- Recovery runs (Z1): Low intensity, aiding in muscle recovery and easy aerobic development.
- Base runs (Z2): Steady-state runs building the foundational aerobic capacity.
- Tempo runs (Z3 - Z4): Pushing the boundaries of aerobic capacity, running at or near the lactate threshold.
- Interval runs (Z4 - Z5): Short, high-intensity intervals focused on anaerobic capacity and speed.

Classes:
- NewMarathonPlan: Creates a new marathon training plan for a user.

Attributes:
- user (object): The user for whom the plan is created.
- date_of_marathon (date): The date of the user's marathon.
- today (date): The current date.
- plan (object): The generated marathon training plan.

Methods:
- _validate_marathon_date: Performs final validation for the date of the marathon.
- create_plan: Creates the marathon training plan and saves it.
- create_runs_in_plan: Creates the scheduled runs within the plan.
- _schedule_runs_for_phase: Schedules runs for a specific phase of the plan.
- _schedule_runs_for_taper: Schedules taper runs at the end of the plan.
- _calculate_distance: Calculates the distance for a run based on user's fitness level and phase.
- _calculate_interval_progression: Calculates the progression of interval values (on, off, sets) during a phase.
- _calculate_duration: Not implemented. Placeholder for calculating run duration.
- _calculate_run_date: Calculates the date for a scheduled run based on the start date, day of the week, and week of the phase.

Example:
python
# Create a new marathon plan for a user
user = RunnerUser.objects.get(username='example_user')
new_plan = NewMarathonPlan(user)
success, plan = new_plan.create_plan()

# Check the success status and access the plan
if success:
    print(f"Marathon plan created successfully: {plan}")
else:
    print(f"Error creating marathon plan: {plan}")

"""

from datetime import date, timedelta
import numpy as np

from ..models import MarathonPlan, ScheduledRun
from . import p_a_constants as c


class NewMarathonPlan:
    def __init__(self, user) -> None:
        self.user = user
        self.date_of_marathon = user.date_of_marathon
        self.today = date.today()
        self.plan = None

    # Final validation for the date of the marathon
    def _validate_marathon_date(self) -> None:
        """
        Perform final validation for the date of the marathon.

        Raises:
        - ValueError: If the marathon date is not in the allowed range.

        Example:
        python
        self._validate_marathon_date()
        
        """
        if not (self.today + timedelta(days=c.MIN_DAYS) <= self.date_of_marathon <= self.today + timedelta(days=c.MAX_DAYS)):
            raise ValueError(
                "Date of marathon is not in allowed range (caught in plan_algo.py)")

    # Create the marathon plan
    def create_plan(self) -> tuple:
        """
        Create the marathon training plan and save it.

        Returns:
        - tuple: A tuple indicating success status (True or False) and the generated plan.

        Example:
        python
        success, plan = self.create_plan()
        if success:
            print(f"Marathon plan created successfully: {plan}")
        else:
            print(f"Error creating marathon plan: {plan}")
        
        """

        try:
            self._validate_marathon_date()
        except ValueError as i:
            return False, f"The marathon date is invalid: {i}"

        self.plan = MarathonPlan(user=self.user, start_date=self.today,
                                 end_date=self.date_of_marathon)  # TODO - no weeks!!
        self.plan.save()
        return True, self.plan

    # Creates the runs given the time frame of dates
    def create_runs_in_plan(self) -> None:
        """
        Create the scheduled runs within the plan.

        Example:
        python
        self.create_runs_in_plan()
        
        """

        # Calculate total days between start and marathon date
        total_days = (self.date_of_marathon - self.today).days

        # Split total days into 3:2:1 ratio
        phase1_days = (3/6) * total_days
        phase2_days = (2/6) * total_days
        # phase3_days = (1/6) * total_days # Not used

        # Adjust phase 1 start date to next Monday
        phase1_start = self.today
        while phase1_start.weekday() != 0:  # 0 represents Monday
            phase1_start += timedelta(days=1)

        # Adjust phase 1 end date to a Sunday
        phase1_end = phase1_start + timedelta(days=phase1_days-1)
        while phase1_end.weekday() != 6:  # 6 represents Sunday
            phase1_end += timedelta(days=1)

        # Adjust phase 2 start date to next Monday
        phase2_start = phase1_end + timedelta(days=1)

        # Adjust phase 2 end date to a Sunday
        phase2_end = phase2_start + timedelta(days=phase2_days-1)
        while phase2_end.weekday() != 6:  # 6 represents Sunday
            phase2_end += timedelta(days=1)

        # Adjust phase 3 start date to next Monday
        phase3_start = phase2_end + timedelta(days=1)
        # End phase 3 a week before marathon date for week of taper
        phase3_end = self.date_of_marathon - timedelta(days=7)

        # Calculate weeks in each phase
        phase1_weeks = (phase1_end - phase1_start).days // 7
        phase2_weeks = (phase2_end - phase2_start).days // 7
        phase3_weeks = (phase3_end - phase3_start).days // 7

        # There is a whole week missing when the runs are scheduleds at the end of phase 1 and 2 due to the // division - need to + 1 to the total weeks
        # Schedule runs for each phase
        self._schedule_runs_for_phase("phase1", phase1_start, phase1_weeks + 1)
        self._schedule_runs_for_phase("phase2", phase2_start, phase2_weeks + 1)
        self._schedule_runs_for_phase("phase3", phase3_start, phase3_weeks + 1)
        self._schedule_runs_for_taper(phase3_end, self.user.fitness_level)

    # Schedule the runs for a given phase
    def _schedule_runs_for_phase(self, phase, phase_start_date, weeks_in_phase) -> None:
        """
        Schedule runs for a specific phase of the plan.

        Args:
        - phase (str): The phase for which runs are to be scheduled.
        - phase_start_date (date): The start date of the phase.
        - weeks_in_phase (int): The number of weeks in the phase.

        Example:
        python
        self._schedule_runs_for_phase("phase1", phase1_start, phase1_weeks + 1)
        
        """

        # Data required for getting workouts from DEFAULT_RUNS dictonary
        fit_level = self.user.fitness_level
        phase = phase

        # Loop
        for i in range(weeks_in_phase):
            for day in c.WEEK:
                # Create the run attributes
                run_id = c.BASIC_PLANS[fit_level][phase][day]

                if run_id == 0:
                    distance = 0
                    duration = 0
                    est_avg_pace = timedelta(minutes=0)
                    on = off = sets = 0
                elif run_id != 5:
                    distance = self._calculate_distance(
                        run_id, fit_level, phase, weeks_in_phase, i)
                    duration = c.DEFAULT_RUNS[run_id]["first_duration"][fit_level]
                    pace = 1 / (distance / duration)
                    est_avg_pace = timedelta(minutes=pace)

                    on = off = sets = 0
                else:
                    if fit_level == "beginner":
                        est_avg_pace = timedelta(minutes=5, seconds=30)
                    elif fit_level == "intermediate":
                        est_avg_pace = timedelta(minutes=4, seconds=30)
                    else:
                        est_avg_pace = timedelta(minutes=3, seconds=30)

                    on, off, sets = self._calculate_interval_progression(
                        fit_level, phase, weeks_in_phase, i)
                    distance = 0
                    duration = (on + off) * sets

                scheduled_run = ScheduledRun(
                    dict_id=run_id,
                    run=c.DEFAULT_RUNS[run_id]["name"],
                    marathon_plan=self.plan,
                    run_feel=c.DEFAULT_RUNS[run_id]["feel"],
                    date=self._calculate_run_date(phase_start_date, day, i),
                    distance=distance,
                    est_duration=duration,
                    est_avg_pace=est_avg_pace,
                    on=on,
                    off=off,
                    sets=sets
                )
                scheduled_run.save()

    def _schedule_runs_for_taper(self, phase3_end, fit_level) -> None:
        """
        Schedule taper runs at the end of the plan.

        Args:
        - phase3_end (date): The end date of phase 3.
        - fit_level (str): The user's fitness level.

        Example:
        python
        self._schedule_runs_for_taper(phase3_end, self.user.fitness_level)
        
        """

        phase3_end_weekday = phase3_end.weekday()

        # We always know the current last scheduled day in phase 3 is a sunday, so a weekday of 6
        amount_to_delete = 6 - phase3_end_weekday
        current_phase3_end_date = phase3_end + timedelta(days=amount_to_delete)

        # Query for scheduled_runs to be removed for taper
        # Query the ScheduledRun model for runs between the two dates
        taper_start_date = phase3_end + timedelta(days=1)
        runs_to_delete = ScheduledRun.objects.filter(
            date__range=(taper_start_date, current_phase3_end_date))

        # Delete the retrieved runs
        runs_to_delete.delete()

        # Add the scheduled taper runs
        for i, day in enumerate(c.WEEK):
            # Create the run attributes
            # I know that it techincally isn't the correct day of the week in the loop to the actual day of the week but it works
            run_id = c.LAST[day]["dict_id"]

            if run_id == 0:
                distance = 0
                duration = 0
                est_avg_pace = timedelta(minutes=0)
                on = off = sets = 0

            elif run_id == 5:
                if fit_level == "beginner":
                    est_avg_pace = timedelta(minutes=5, seconds=30)
                elif fit_level == "intermediate":
                    est_avg_pace = timedelta(minutes=4, seconds=30)
                else:
                    est_avg_pace = timedelta(minutes=3, seconds=30)

                on, off, sets = c.LAST[day]["on"], c.LAST[day]["off"], c.LAST[day]["sets"]
                distance = 0
                duration = (on + off) * sets

            elif run_id == 9:
                distance = c.DEFAULT_RUNS[run_id]["distance"]
                duration = c.DEFAULT_RUNS[run_id]["first_duration"][fit_level]
                pace = 1 / (distance / duration)
                est_avg_pace = timedelta(minutes=pace)

                on = off = sets = 0

            else:
                distance = c.LAST[day]["distance"]
                duration = c.LAST[day]["duration"][fit_level]
                pace = 1 / (distance / duration)
                est_avg_pace = timedelta(minutes=pace)

                on = off = sets = 0

            scheduled_run = ScheduledRun(
                dict_id=run_id,
                run=c.DEFAULT_RUNS[run_id]["name"],
                marathon_plan=self.plan,
                run_feel=c.DEFAULT_RUNS[run_id]["feel"],
                date=taper_start_date + timedelta(days=i),
                distance=distance,
                est_duration=duration,
                est_avg_pace=est_avg_pace,
                on=on,
                off=off,
                sets=sets
            )
            scheduled_run.save()

    def _calculate_distance(self, run_id, fit_level, phase, weeks_in_phase, i) -> float:
        """
        Calculate the distance for a run based on user's fitness level and phase.

        Args:
        - run_id (int): The ID of the run.
        - fit_level (str): The user's fitness level.
        - phase (str): The phase of the plan.
        - weeks_in_phase (int): The number of weeks in the phase.
        - i (int): The current week within the phase.

        Returns:
        - float: The calculated distance for the run.

        Example:
        python
        distance = self._calculate_distance(run_id, fit_level, phase, weeks_in_phase, i)
        
        """

        low = c.DEFAULT_RUNS[run_id]["distance"][fit_level][phase]["low"]
        high = c.DEFAULT_RUNS[run_id]["distance"][fit_level][phase]["high"]
        diff = high - low

        addition = diff / (weeks_in_phase - 1)

        return low + (addition * i)

    def _calculate_interval_progression(self, fit_level, phase, weeks_in_phase, i, run_id=5):
        """
        Calculate the progression of interval values (on, off, sets) during a phase.

        Args:
        - fit_level (str): The user's fitness level.
        - phase (str): The phase of the plan.
        - weeks_in_phase (int): The number of weeks in the phase.
        - i (int): The current week within the phase.
        - run_id (int): The ID of the run.

        Returns:
        - tuple: A tuple containing the calculated values for on, off, and sets.

        Example:
        python
        on, off, sets = self._calculate_interval_progression(fit_level, phase, weeks_in_phase, i)
        
        """
        def calculate_weekly_value(low, high, weeks, current_week):
            diff = high - low

            # Calculate the ideal change, considering total weeks
            ideal_change = round(diff * current_week / weeks)

            # Calculate the weekly value based on the ideal change
            weekly_value = low + ideal_change

            return weekly_value

        on_low = c.DEFAULT_RUNS[run_id]["on"]
        on_high = c.DEFAULT_RUNS[run_id]["on"]
        off_low = c.DEFAULT_RUNS[run_id]["off"]
        off_high = c.DEFAULT_RUNS[run_id]["off"]
        sets_low = c.DEFAULT_RUNS[run_id]["sets"][fit_level][phase]["low"]
        sets_high = c.DEFAULT_RUNS[run_id]["sets"][fit_level][phase]["high"]

        on_value = calculate_weekly_value(on_low, on_high, weeks_in_phase, i)
        off_value = calculate_weekly_value(
            off_low, off_high, weeks_in_phase, i)
        sets_value = calculate_weekly_value(
            sets_low, sets_high, weeks_in_phase, i)

        return (on_value, off_value, sets_value)

    # Calculate the run date
    def _calculate_run_date(self, start_date, day_of_week, week_of_phase) -> date:
        """
        Calculate the run date.

        Args:
        - start_date (date): The start date of the phase.
        - day_of_week (str): The day of the week for the scheduled run.
        - week_of_phase (int): The week within the phase.

        Returns:
        - date: The calculated date for the scheduled run.

        Example:
        python
        run_date = self._calculate_run_date(phase_start_date, day, i)
        
        """
        days_mapping = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6
        }
        delta_days = days_mapping[day_of_week] - start_date.weekday()
        if delta_days < 0:
            delta_days += 7
        return timedelta(days=(week_of_phase * 7)) + start_date + timedelta(days=delta_days)
