# utils/plan_algo.py
from ..models import MarathonPlan, Run, ScheduledRun
from datetime import date, timedelta

""" Plan constants """
MIN_DAYS = 90 
MAX_DAYS = 365

""" Basic plans """
BASIC_PLANS = {
    "beginner": {
        "phase1": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  2}, 
            {"day": "wed", "run_id":  0}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  0}, 
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
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  1}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  0}, 
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
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  3}, 
            {"day": "sun", "run_id":  2} 
        ],
        "phase2": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  2}, 
            {"day": "fri", "run_id":  0}, 
            {"day": "sat", "run_id":  2}, 
            {"day": "sun", "run_id":  3} 
        ],
        "phase3": [
            {"day": "mon", "run_id":  2}, 
            {"day": "tue", "run_id":  5}, 
            {"day": "wed", "run_id":  2}, 
            {"day": "thu", "run_id":  4}, 
            {"day": "fri", "run_id":  0}, 
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

        self.plan = MarathonPlan(user=self.user, start_date=self.today, end_date=self.date_of_marathon, active=False)
        # plan.save() - TODO: make sure not randomly saving plans
        return self.plan

    # Creates the runs given the time frame of dates
    def create_runs_in_plan(self):
        """
        Schedules the runs within the training plan based on the phases and their duration.
        """

        self.validate_marathon_date()

        # Given the end date, the day of marathon, the last training week will be 7 days if marathon is on the Sunday or less days if before Sunday
        marathon_weekday = self.date_of_marathon.weekday()

        # Calculate the end date of Phase 3 (Sunday before marathon or day of marathon if it's on Sunday)
        if marathon_weekday != 6:  # If not Sunday
            p3_end_date = self.date_of_marathon - timedelta(days=(marathon_weekday + 1))
        else:
            p3_end_date = self.date_of_marathon

        # Calculate the start date of the training (next Monday)
        days_until_next_monday = (7 - self.today.weekday()) % 7
        p1_start_date = self.today + timedelta(days=days_until_next_monday)

        # Calculate total available days for training
        total_days_available = (p3_end_date - p1_start_date).days + 1

        # Distribute days according to 3:2:1 ratio
        total_ratio = 3 + 2 + 1
        p1_training_days = (total_days_available * 3) // total_ratio
        p2_training_days = (total_days_available * 2) // total_ratio
        p3_training_days = (total_days_available * 1) // total_ratio

        # Ensure each phase's days are multiples of 7 for full weeks
        p1_training_days = (p1_training_days // 7) * 7
        p2_training_days = (p2_training_days // 7) * 7
        p3_training_days = (p3_training_days // 7) * 7

        # Calculate the start and end dates for each phase
        p3_start_date = p3_end_date - timedelta(days=p3_training_days - 1)
        p2_end_date = p3_start_date - timedelta(days=1)
        p2_start_date = p2_end_date - timedelta(days=p2_training_days - 1)
        p1_end_date = p2_start_date - timedelta(days=1)
        # Note: p1_start_date already defined

        # Calculate spare days
        spare_days = total_days_available - (p1_training_days + p2_training_days + p3_training_days)

        # Schedule runs for each phase
        self.schedule_runs_for_phase("phase1", p1_start_date)
        self.schedule_runs_for_phase("phase2", p2_start_date)
        self.schedule_runs_for_phase("phase3", p3_start_date)

        # Handle spare days if needed

    # Schedule the runs for a given phase
    def schedule_runs_for_phase(self, phase_name, start_date_of_phase):
        """
        Schedules the runs for a specific phase.

        Parameters
        ----------
        phase_name : str
            The name of the phase ("phase1", "phase2", or "phase3").
        start_date_of_phase : date
            The date on which the phase starts.
        """

        plan_for_phase = BASIC_PLANS[self.user.fitness_level][phase_name]


        # Calculate overload factor
        total_days_in_plan = (self.date_of_marathon - self.today).days
        overload_factor = SCALING_FACTORS[self.user.fitness_level] / total_days_in_plan

        for run_info in plan_for_phase:
            run_details = Run.objects.get(id=run_info["run_id"])
            run_date = self.calculate_run_date(start_date_of_phase, run_info["day"])

            # TODO
            # Apply the feedback adjustment for this week (assuming you have a method to get feedback for the week)
            feedback_for_week = self.get_feedback_for_week(run_date) # You'll need to implement this
            adjusted_overload_factor = overload_factor + FEEDBACK_ADJUSTMENT[feedback_for_week]

            if not (run_date == self.date_of_marathon):
                run_name=f"{run_details.feel} Training Run"
            else:
                run_name="Marathon"

            scheduled_run = ScheduledRun(
                run=run_name,
                marathon_plan=self.plan,
                run_type=run_details,
                date=run_date,
                duration=run_details.duration, #, To personalise
                distance=run_details.distance, # To personalise
                on=run_details.on, # To personalise
                off=run_details.off, # To personalise
                sets=run_details.sets # To personalise
            )
            scheduled_run.save()

    # Calculate the run date
    def calculate_run_date(self, start_date, day_of_week) -> date:
        """
        Determines the date for a run based on its specified day of the week and the start date of the phase.

        Parameters
        ----------
        start_date : date
            The date on which the phase (or week) starts.
        day_of_week : str
            The day of the week (e.g., "mon", "tue").

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
        return start_date + timedelta(days=delta_days)
