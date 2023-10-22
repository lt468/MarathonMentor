"""
This module provides logic for creating a marathon training plan.

It uses a user's fitness level and the date of their marathon to create a tailored training plan split into different phases.
"""
from datetime import date, timedelta
import numpy as np

from ..models import MarathonPlan, ScheduledRun, CompletedRun
from . import p_a_constants as c


class NewMarathonPlan:
    """ 
     A class to represent a marathon training plan.

    This class provides functionalities to create a marathon training plan based on a user's fitness level 
    and the date of their marathon. The training plan is split into different phases with specific workouts 
    and runs scheduled.

    Attributes:
        user (User): The user for whom the marathon plan is being created.
        date_of_marathon (date): The date on which the marathon will take place.
        today (date): The current date.
        plan (MarathonPlan, optional): An instance of MarathonPlan representing the created training plan. 
            Defaults to None.
    """
    # Constructor

    def __init__(self, user) -> None:
        """
        Initializes a new instance of the marathon training plan.

        Args:
            user (User): The user for whom the marathon plan is being created.
        """
        self.user = user
        self.date_of_marathon = user.date_of_marathon
        self.today = date.today()
        self.plan = None

    # Final validation for the date of the marathon
    def _validate_marathon_date(self) -> None:
        """
        Validates that the marathon date is within the allowed range.

        The allowed date range is defined by the MIN_DAYS and MAX_DAYS constants.

        Raises:
            ValueError: If the marathon date is not within the allowed range.
        """

        if not (self.today + timedelta(days=c.MIN_DAYS) <= self.date_of_marathon <= self.today + timedelta(days=c.MAX_DAYS)):
            raise ValueError(
                "Date of marathon is not in allowed range (caught in plan_algo.py)")

    # Create the marathon plan
    def create_plan(self) -> tuple:
        """
        Creates the marathon training plan.

        This method validates the marathon date, initializes a MarathonPlan instance, and saves it.

        Returns:
            tuple: A tuple containing a boolean indicating the success of the operation and the MarathonPlan 
                instance if successful, or an error message if not.
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
        Creates and schedules the runs within the training plan.

        This method calculates the total number of days for the training, divides the training period into 
        different phases, and schedules the runs based on the user's fitness level and the training phase.

        Returns:
            None: Calculates dates and then calls the methods to schedule the runs.
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
        Schedules the runs for a given phase of the training plan.

        Args:
            phase (int): The current training phase.
            phase_start_date (date): The start date of the current training phase.
            weeks_in_phase (int): The total number of weeks in the current training phase.

        Returns:
            None: This method doesn't return anything. It schedules the runs and saves them to the database.
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
        Schedules the taper runs at the end of the training plan.

        Args:
            phase3_end (date): The end date of the third phase of the training plan.
            fit_level (str): The fitness level of the user.

        Returns:
            None: This method doesn't return anything. It schedules the taper runs and saves them to the database.
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
         Calculates the distance for a specific run.

        Args:
            run_id (str): The identifier for the type of run.
            fit_level (str): The fitness level of the user.
            phase (int): The current training phase.
            weeks_in_phase (int): The total number of weeks in the current training phase.
            i (int): The current week in the training plan.

        Returns:
            float: The calculated distance for the run.
        """

        low = c.DEFAULT_RUNS[run_id]["distance"][fit_level][phase]["low"]
        high = c.DEFAULT_RUNS[run_id]["distance"][fit_level][phase]["high"]
        diff = high - low

        addition = diff / (weeks_in_phase - 1)

        return low + (addition * i)

    def _calculate_interval_progression(self, fit_level, phase, weeks_in_phase, i, run_id=5):
        """
        Calculates the progression of intervals for a specific run.

        Args:
            fit_level (str): The fitness level of the user.
            phase (int): The current training phase.
            weeks_in_phase (int): The total number of weeks in the current training phase.
            i (int): The current week in the training plan.
            run_id (str): The identifier for the type of run. Defaults to 5.

        Returns:
            tuple: A tuple containing the calculated values for 'on', 'off', and 'sets'.
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

    def _calculate_duration(self):
        """ Not yet implemented """
        # completed_runs_with_specific_dict_id = CompletedRun.objects.filter(scheduled_run__dict_id=run_id)
        # if not completed_runs_with_specific_dict_id.exists():
        #    pass
        #    #avg_paces = [run.avg_pace for run in completed_runs_with_specific_dict_id if run.avg_pace]
        #    #seconds_list = [pace.total_seconds() for pace in avg_paces]
        #    #avg_seconds = int(np.mean(seconds_list))
        #    #avg_timedelta = timedelta(seconds=avg_seconds)
        return NotImplemented

    # Calculate the run date
    def _calculate_run_date(self, start_date, day_of_week, week_of_phase) -> date:
        """
        Calculates the date on which a specific run should take place.

        Args:
            start_date (date): The start date of the training phase.
            day_of_week (str): The day of the week on which the run should take place.
            week_of_phase (int): The week of the training phase.

        Returns:
            date: The calculated date on which the run should take place.
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