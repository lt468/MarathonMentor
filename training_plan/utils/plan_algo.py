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


""" Plan constants """
MIN_DAYS = 90 
MAX_DAYS = 365

def CreatePlan(user):
    """
    The plan will be split into 3 phases
    Phase 1 - Base: The first half of the programme focusing on mainly base workouts
    Phase 2 - Peak 1: The start of the second half with the focus on more longer intense runs
    Phase 3 - Peak 2: Final part of the programme to peak into the marathon day

    Phases spilt with a ratio of 3:2:1 for Phases 1:2:3 respectively
    """
    date_of_marathon = user.date_of_marathon
    today = date.today()

    # Calculate the difference of days from now
    if date_of_marathon >= today + timedelta(days=MIN_DAYS) and date_of_marathon <= today + timedelta(days=MAX_DAYS) and date_of_marathon >= today:
        days = (user.date_of_marathon - today).days

    else:
        raise ValueError("Date of Marathon is invalid")

    # Model for MarathonPlan variables
    start_date = today
    end_date = today + timedelta(days=days)

    plan = MarathonPlan(user=user, start_date=start_date, end_date=end_date, active=False) # TODO - change to active when adding the new active one
    # plan.save() - TODO -  make sure random plans aren't saved
    return plan
    
def CreateRunsInPlan(plan):

    # Firstly get the number of training days and spare days
    training_days = (days // 7) * 7

    # Get the number of training days and spare days for phases
    p1_training_days = (training_days // 6) * 3
    p2_training_days = (training_days // 6) * 2
    p3_training_days = (training_days // 6) * 1
    spare_days = days - (p1_training_days + p2_training_days + p3_training_days)

    pass

