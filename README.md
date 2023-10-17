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
| 15/10/2023    | Getting back into the project after a hiatus    | Create the form for the user sign-up and Marathon Plan creation | N/A |
| 16/10/2023    | Creating form. Found bug in plan_algo.py: overload factor not used. Changed to progression factor for each of the phases. Now looking to see if this works. Things work, runs scheduled| 1) The algorithm is very slow, might need to rethink things. 2) The progression factor esculates ridicously fast, might need a logarithmic function that decreaes as time goes on. 3) Ensure that the sets, on and off are done correctly. 4) Make sure that the taper week is done correctly  | Can recommend beginners to have at least 180 day plan. |
| 17/10/2023    | Started messing around with correct implemenation of overload factors | Implement the duration overload factor, and then continue with the other attributes in plan_algo.py | Change the database? How much does sqlite scale too? Maybe rethink the implemenation of the db? Or just need a faster alogrithm |

