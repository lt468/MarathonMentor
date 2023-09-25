# utils/plan_algo.py

from ..models import MarathonPlan
from datetime import date, timedelta
"""
Training Plan Algorithm - MarathonMentor
---------------------------------------

This algorithm is designed to create a comprehensive training plan based on user inputs and predefined workout templates. 
The primary structure of the plan adheres to an 80/20 split between Base runs (long distance, steady-state) 
and Higher intensity runs, which include longer threshold/tempo runs and very short anaerobic runs. 
Recovery runs are also incorporated on recovery days and are considered optional.

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

Note: The actual training plan generated will consider user-specific inputs like current fitness level, 
target marathon time, availability, and other factors to tailor the plan to individual needs.

This file serves as the core logic for generating the training plan, utilizing the workout templates 
defined in the Django models.
"""


class NewMarathonPlan:
    """
    The NewMarathonPlan class represents a marathon training plan.
    The plan will be split into 3 phases:
    - Phase 1 - Base: The first half of the programme focusing on mainly base workouts.
    - Phase 2 - Peak 1: The start of the second half with the focus on more longer intense runs.
    - Phase 3 - Peak 2: Final part of the programme to peak into the marathon day.
        Phases are split with a ratio of 3:2:1 for Phases 1:2:3 respectively.

        Steps in allocating runs to training days:
    1) Get the total number of training days and spare days for the plan in the plan then get the number of training weeks and spare days in each phase.
    2) Build phase 1: ...

    Phases for different fitness levels:
#??    Each phase will be a dictionary containing the days of the week and the ID of the run that the user will be doing. An ID of 0 means that there is no run.
    """

    """ Plan constants """
    MIN_DAYS = 90 
    MAX_DAYS = 365

    def __init__(self, user) -> None:
        self.user = user
        self.date_of_marathon = user.date_of_marathon
        self.today = date.today()

    def validate_marathon_date(self):
        if not (self.today + timedelta(days=self.MIN_DAYS) <= self.date_of_marathon <= self.today + timedelta(days=self.MAX_DAYS)):
            raise ValueError("Date of Marathon is invalid")

    def create_plan(self):
        self.validate_marathon_date()
        
        days = (self.date_of_marathon - self.today).days
        end_date = self.today + timedelta(days=days)
        
        plan = MarathonPlan(user=self.user, start_date=self.today, end_date=end_date, active=False)
        # plan.save() - TODO: make sure not randomly saving plans
        return plan

    def create_runs_in_plan(self):
        self.validate_marathon_date() # TODO in views, if the value error is raised, then render a certain page/html saying the date is invalid and its a server error, etc.
        # As the user should have not been able to get this far anyway with an invalid date
        
        days = (self.date_of_marathon - self.today).days

        # Firstly get the number of training days and spare days
        training_days = (days // 7) * 7

        # Get the number of training days and the plan spare days
        p1_training_days = (training_days // 6) * 3
        p2_training_days = (training_days // 6) * 2
        p3_training_days = (training_days // 6) * 1
        plan_spare_days = days - (p1_training_days + p2_training_days + p3_training_days)

        # Get the number of training weeks and spare days for each of the training phases
        p1_training_weeks = p1_training_days // 7
        p2_training_weeks = p2_training_days // 7
        p3_training_weeks = p3_training_days // 7

        p1_spare_days = p1_training_days % 7
        p2_spare_days = p2_training_days % 7
        p3_spare_days = p3_training_days % 7



