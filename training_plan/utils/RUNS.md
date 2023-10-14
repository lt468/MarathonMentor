# For documentation purposes

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


