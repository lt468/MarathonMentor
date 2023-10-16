# utils/plan_algo.py
from datetime import date, timedelta

from ..models import MarathonPlan, Run, ScheduledRun

""" Plan constants """
MIN_DAYS = 90 
MAX_DAYS = 365

""" Basic plans """
BASIC_PLANS = {
    "beginner": {
        "phase1": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  2}, 
            {"day": "wed", "run_id":  6}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  1}, 
            {"day": "sun", "run_id":  3} 
        ]
    },
    "intermediate": {
        "phase1": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  2}, 
            {"day": "wed", "run_id":  1}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ]
    },
    "advanced": {
        "phase1": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  2}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  6}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ]
    },
}

""" Scaling factors """
SCALING_FACTORS = {
    "beginner": {
        "duration": 0.4,
        "distance": 0.4,
        "on": 0.4,
        "off": 1.6,
        "sets": 0.5
    },
    "intermediate": {
        "duration": 1,
        "distance": 1,
        "on": 1,
        "off": 1,
        "sets": 1
    },
    "advanced": {
        "duration": 1.2,
        "distance": 1.2,
        "on": 1.2,
        "off": 0.8,
        "sets": 1.2
    }
}

""" Feedback adjustments """
FEEDBACK_ADJUSTMENTS = {
    "too_easy": 1.1,   # Increase by 10%
    "just_right": 1,  # No change
    "too_hard": 0.9   # Decrease by 10%
}

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
    validate_marathon_date():
        Validates the date of the marathon.
    create_plan() -> object:
        Creates the marathon training plan.
    create_runs_in_plan():
        Schedules the runs within the plan.
    schedule_runs_for_phase(phase_name: str, start_date_of_phase: date):
        Schedules the runs for a specific phase.
    calculate_run_date(start_date: date, day_of_week: str) -> date:
        Determines the date for a run given its day of the week.


    Phases for different fitness levels:
    #??    Each phase will be a dictionary containing the days of the week and the ID of the run that the user will be doing. An ID of 0 means that there is no run.
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
    def validate_marathon_date(self) -> None:
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

        self.validate_marathon_date()

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

        self.validate_marathon_date()

        # Calculate total days between start and marathon date
        total_days = (self.date_of_marathon - self.today).days
        
        # Split total days into 3:2:1 ratio
        phase1_days = (3/6) * total_days
        phase2_days = (2/6) * total_days
        phase3_days = (1/6) * total_days
        
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
    def schedule_runs_for_phase(self, phase_name, start_date_of_phase, repeat):
        """
        Schedules the runs for a specific phase.

        Parameters
        ----------
        phase_name : str
            The name of the phase ("phase1", "phase2", or "phase3").
        start_date_of_phase : date
            The date on which the phase starts.
        repeat : int
            The amount weeks within a phase
        """

        # Get the weekly plan for the phase
        plan_for_phase = BASIC_PLANS[self.user.fitness_level][phase_name]

        # For each week in the phase, add all the runs in that week
        # Start with the default run and times it by the necessary scaling factor for the attributes in the run
        # For each week, increase the amount of work by a given amount

        # Base variables
        base_progression_factor = 0.2 
        base_week_number = 12

        changing_scaling_factors = (SCALING_FACTORS[self.user.fitness_level]).copy()
        progression_factor = (base_progression_factor / repeat) * base_week_number

        for i in range(repeat): # Loop over the given weeks in a phase
            for run_info in plan_for_phase: # For each of the runs in the phase plans
                # Scheduled run attributes for each of the scheduled runs (that will be saved into the database)
                run_details = Run.objects.get(id=run_info["run_id"])
                run_date = self.calculate_run_date(start_date_of_phase, run_info["day"], i)

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

            for attribute in changing_scaling_factors:
                changing_scaling_factors[attribute] += (changing_scaling_factors[attribute] * progression_factor)

        # TODO - Maybe as an UpdateMarathonPlan class?
        # Apply the feedback adjustment for this week (assuming you have a method to get feedback for the week)
        # feedback_for_week = self.get_feedback_for_week(run_date) # You'll need to implement this
        # adjusted_overload_factor = overload_factor + FEEDBACK_ADJUSTMENT[feedback_for_week]

        # Calculate overload factor for a given phase
        # total_days_in_plan = (self.date_of_marathon - self.today).days
        # overload_factor = SCALING_FACTORS[self.user.fitness_level] / total_days_in_plan


    # Calculate the run date
    def calculate_run_date(self, start_date, day_of_week, repeat) -> date:
        """
        Determines the date for a run based on its specified day of the week and the start date of the phase.

        Parameters
        ----------
        start_date : date
            The date on which the phase (or week) starts.
        day_of_week : str
            The day of the week (e.g., "mon", "tue").
        repeat : int
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
        return timedelta(days=repeat) + start_date + timedelta(days=delta_days)
