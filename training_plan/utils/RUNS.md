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

Since each run will be adapted to the specifics of a User and their training plan, we save default runs that are defined on the intermediate level.
These runs are then used within ./utils/plan_algo.py to determine the personalized values for a run. For a given run, we define the standard duration,
distance, and rest periods & interval times/distances (for intervals), which are the only variables that will change, as unity, with values

= Recovery == Z1
- Duration = 30' = 1 
- Distance = 4km = 1 

= Base == Z2
- Duration = 60' = 1
- Distance = 10km = 1

= Long Base == Z2
- Duration = 90' = 1
- Distance = 15km = 1

= Long Tempo == 3
- Duration = 30' = 1
- Distance = 6km = 1

= Tempo == Z4
- Duration = 20' = 1
- Distance = 8km = 1

= Interval == Z5
- On = 4' = 1
- Off = 4' = 1
- Sets = 4 = 1


== 20/10 == db_redesign update ====
- I am going to to base the times off of the user's inputted pace for the runs and save them in a database
to calculate the estimated time of completion for all runs but the intervals (which will be done on time anyway).
- I am then going to create a tool in the browser for the user to calculate the pace time if they have a time for the 
entire workout and use that as input OR use the strava API to get their runs and automatically do it for them
- If there is no pace inputted I will ask the user to use select "use default" which will mean that the default values
are used for pace and then give an estimated time


