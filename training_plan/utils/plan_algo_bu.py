# utils/plan_algo.py
from datetime import date, timedelta
import numpy as np

from ..models import MarathonPlan, Run, ScheduledRun
from . import p_a_constants as c

class NewMarathonPlan:
    """
    A class to represent a marathon training plan.

    The plan is split into three phases:
    - Phase 1 (Base): Focuses on base workouts.
    - Phase 2 (Peak 1): Longer, more intense runs.
    - Phase 3 (Peak 2): Final preparations leading up to marathon day.

    Attributes
    ----------
    user : object
        The user object, which should have the date_of_marathon attribute.
    date_of_marathon : date
        The date on which the marathon will take place.
    today : date
        The current date.
    plan : object, optional
        The training plan, by default None.

    Methods
    -------
    _validate_marathon_date():
        Validates the date of the marathon.
    create_plan() -> object:
        Creates the marathon training plan.
    create_runs_in_plan():
        Schedules the runs within the plan.
    schedule_runs_for_phase(phase_name: str, start_date_of_phase: date):
        Schedules the runs for a specific phase.
    _calculate_run_date(start_date: date, day_of_week: str) -> date:
        Determines the date for a run given its day of the week.


    Phases for different fitness levels:
    Each phase will be a dictionary containing the days of the week and the ID of the run that the user will be doing. An ID of 6 means that there is no run.
    """

    # Constructor
    def __init__(self, user) -> None:
        """
        Parameters
        ----------
        user : object
            The user object, which should have the date_of_marathon attribute.
        """

        self.user = user
        self.date_of_marathon = user.date_of_marathon
        self.today = date.today()
        self.plan = None

    # Final validation for the date of the marathon
    def _validate_marathon_date(self) -> None:
        """
        Validates the date of the marathon based on the difference from the current date.

        Raises
        ------
        ValueError
            If the date of the marathon is not within the allowed range.
        """

        if not (self.today + timedelta(days=MIN_DAYS) <= self.date_of_marathon <= self.today + timedelta(days=MAX_DAYS)):
            raise ValueError("Date of Marathon is invalid")

    # Create the marathon plan
    def create_plan(self) -> MarathonPlan:
        """
        Creates a marathon training plan.

        Returns
        -------
        object
            The created marathon plan.
        """

        self._validate_marathon_date()

        self.plan = MarathonPlan(user=self.user, start_date=self.today, end_date=self.date_of_marathon) # TODO - no weeks!!
        self.plan.save()
        return self.plan

    # Creates the runs given the time frame of dates
    def create_runs_in_plan(self):
        """
        Schedules the runs within the training plan based on the phases and their duration.

        The start of phase 1 always starts on a Monday. If the start date is the current day and it is a Monday, then it will start it from the current day,
        e.g., if today is Monday, and then start day is today, then phase 1 will start from today

        Phase 3 will always taper and end on the Marathon date.
        """

        self._validate_marathon_date()

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
        phase3_end = self.date_of_marathon
        
        # Calculate weeks in each phase
        phase1_weeks = (phase1_end - phase1_start).days // 7
        phase2_weeks = (phase2_end - phase2_start).days // 7
        phase3_weeks = (phase3_end - phase3_start).days // 7

        # Schedule runs for each phase
        self.schedule_runs_for_phase("phase1", phase1_start, phase1_weeks)
        self.schedule_runs_for_phase("phase2", phase2_start, phase2_weeks)
        self.schedule_runs_for_phase("phase3", phase3_start, phase3_weeks)
        
    # Schedule the runs for a given phase
    def schedule_runs_for_phase(self, phase_name, start_date_of_phase, weeks_in_phase):
        """
        Schedules the runs for a specific phase.

        Parameters
        ----------
        phase_name : str
            The name of the phase ("phase1", "phase2", or "phase3").
        start_date_of_phase : date
            The date on which the phase starts.
        weeks_in_phase : int
            The amount weeks within a phase
        """

        # Get the weekly plan for the phase
        plan_for_phase = c.BASIC_PLANS[self.user.fitness_level][phase_name]

        # Base variables
        changing_scaling_factors = c.SCALING_FACTORS[self.user.fitness_level].copy()

        for i in range(weeks_in_phase): # Loop over the given weeks in a phase
            for run_info in plan_for_phase: # For each of the runs in the phase plans
                # Scheduled run attributes for each of the scheduled runs (that will be saved into the database)
                run_details = Run.objects.get(id=run_info["run_id"])
                run_date = self._calculate_run_date(start_date_of_phase, run_info["day"], i)

                if not (run_date == self.date_of_marathon):
                    run_name=f"{run_details.feel} Training Run".capitalize()
                else:
                    run_name="Marathon"

                scheduled_run = ScheduledRun(
                    run=run_name,
                    marathon_plan=self.plan,
                    run_type=run_details,
                    date=run_date,
                    duration=run_details.duration * changing_scaling_factors["duration"], #, To adjust
                    distance=run_details.distance * changing_scaling_factors["distance"], # To adjust
                    on=run_details.on * changing_scaling_factors["on"], # To adjust
                    off=run_details.off * changing_scaling_factors["off"], # To adjust
                    sets=run_details.sets * changing_scaling_factors["sets"] # To adjust
                )
                scheduled_run.save()


            progression_factor = self._calc_progression_factor(weeks_in_phase, changing_scaling_factors)
            for attribute in changing_scaling_factors:
                changing_scaling_factors[attribute] += (changing_scaling_factors[attribute] * progression_factor[attribute])

        # TODO - Maybe as an UpdateMarathonPlan class?
        # Apply the feedback adjustment for this week (assuming you have a method to get feedback for the week)
        # feedback_for_week = self.get_feedback_for_week(run_date) # You'll need to implement this
        # adjusted_overload_factor = overload_factor + FEEDBACK_ADJUSTMENT[feedback_for_week]

        # Calculate overload factor for a given phase
        # total_days_in_plan = (self.date_of_marathon - self.today).days
        # overload_factor = SCALING_FACTORS[self.user.fitness_level] / total_days_in_plan


    def _calc_progression_factor(self, weeks_in_phase, scale_factors, bpf=0.1, bwn=12):
        """
        Determines the progression factor for each of the attributes of within a workout (duration, distance, on, off, sets, etc.)

        Parameters
        ----------
        scale_factors : dict
            Scale factor dictionary that is changed for each itteration of progressive overload
        bpf : float
            Base progression factor - how each week progesses. Arbitrary default value of 0.1
        bwn : int
            Base week number for calculation. Arbitrary default value of 12

        Returns
        -------
        dictionary
            Dictionary with the individual progression factors for the attributes
        """
    #"beginner": {
    #    "duration": 0.4,
    #    "distance": 0.4,
    #    "on": 0.4,
    #    "off": 1.6,
    #    "sets": 0.5

        # Progression for duration


        progression_factor = (bpf / weeks_in_phase) * bwn
        return scale_factors

    def _progressive_duration(self, n_weeks, start_duration, end_duration, b_value=2.735):
        """
        Returns a list of progressive durations for each week up to n_weeks.
        
        Parameters
        ----------
        n_weeks : int
            The number of weeks.
        start_duration : float
            The starting duration in minutes for week 1.
        end_duration : float
            The desired ending duration in minutes for the last week.
        b_value : float, optional
            The base value for the logarithm (default is the optimal value found by considering plateau after many weeks **TODO need more explanation).

        Returns
        -------
        numpy.ndarray
            An array of durations, with each entry representing the duration for a week.
        
        Examples
        --------
        >>> progressive_duration(12, 24, 120)
        array([ 24.        ,  50.94271358,  66.70319069, ..., 117.20647524, 120.58861784])
        """

        #default_end_duration = 

        # Calculate the value of 'a' based on the number of weeks and start/end durations
        a_value = (end_duration - start_duration) * np.log(b_value) / np.log(n_weeks)
        
        # Calculate the progression for each week
        x = np.arange(1, n_weeks + 1)
        y = a_value * np.log(x) + start_duration
        
        return y
            
    # Calculate the run date
    def _calculate_run_date(self, start_date, day_of_week, weeks_in_phase) -> date:
        """
        Determines the date for a run based on its specified day of the week and the start date of the phase.

        Parameters
        ----------
        start_date : date
            The date on which the phase (or week) starts.
        day_of_week : str
            The day of the week (e.g., "mon", "tue").
        weeks_in_phase : int
            How many weeks in to the phase so that each week there are runs (rather than always the same week)

        Returns
        -------
        date
            The date on which the run should take place.
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
        return timedelta(days=weeks_in_phase) + start_date + timedelta(days=delta_days)
