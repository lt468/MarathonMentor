# MarathonMentor
A Web Application that is able to create a tailored Marathon training plan. This is my CS50w Final Project.

### Note: You will need to run
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Log of progress
As of 15/10/2023, I have decided to keep a log of what I am doing, what needs to be done, etc., for my own personal convenience. I hope to use this in the future
for documnetation.

| **Date**    | **Status**    | **TODO for tomorrow**    | **Notes**    |
|---------------- | --------------- | --------------- | --------------- |
| 15/10/2023    | Getting back into the project after a hiatus    | ~~Create the form for the user sign-up and Marathon Plan creation~~ | N/A |
| 16/10/2023    | Creating form. Found bug in plan_algo.py: overload factor not used. Changed to progression factor for each of the phases. Now looking to see if this works. Things work, runs scheduled| 1) The algorithm is very slow, might need to rethink things. ~~2) The progression factor esculates ridicously fast, might need a logarithmic function that decreaes as time goes on. 3) Ensure that the sets, on and off are done correctly.~~ 4) Make sure that the taper week is done correctly  | Can recommend beginners to have at least 180 day plan. |
| 17/10/2023    | Started messing around with correct implemenation of overload factors | Implement the duration overload factor, and then continue with the other attributes in plan_algo.py | ~~Change the database? How much does sqlite scale too? Maybe rethink the implemenation of the db? Or just need a faster alogrithm~~ |
| 20/10/2023    | Want to change the slqlite3 database to mySQL in django, also realised that the default runs are no longer saved as I used .gitignore, not sure if it's worth making a larger hash table instead to combine a lot of data, system design is a real thing! Things seem to work now and it's faster. | There are runs added to the db on the same date and the dates of runs are very messed up | I will need to implement an extension of the plan_algo to update the runs when a user has completed a run to better predict distance, duration, pace, etc. |
| 21/10/2023    | Going to fix the issue with the run dates, and then that should mean I can start work on the front end | | |

