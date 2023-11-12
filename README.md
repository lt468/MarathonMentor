# MarathonMentor
A Web Application that is able to create a tailored Marathon training plan. This is my CS50w Final Project.

## Overview
Brief overview of your project.

## Distinctiveness and Complexity
### Why your project satisfies the distinctiveness and complexity requirements
Explain how your project is distinct from others in the course, especially from projects like the social network or e-commerce site. Discuss the complexity of your project.

## Project Files
### Django App Files
- **`LICENSE`**: License file for your project.
- **`manage.py`**: Django management script.
- **`MarathonMentor/`**: Django project folder.
  - **`asgi.py`**: ASGI configuration.
  - **`__init__.py`**: Initialization file.
  - **`settings.py`**: Django settings.
  - **`urls.py`**: URL patterns.
  - **`wsgi.py`**: WSGI configuration.

### Training Plan App Files
- **`training_plan/`**: Django app folder.
  - ... (List other important files and folders)

### Static Files
- **`static/`**: Folder for static files (CSS, JS, images).
  - ... (List important static files and subdirectories)

### Templates
- **`templates/`**: Folder for HTML templates.
  - ... (List important template files and subdirectories)

### Utils Files
- **`utils/`**: Folder for utility files.
  - **`p_a_constants.py`**: Constants used in the training plan algorithm.
  - **`plan_algo.py`**: Main training plan algorithm.
  - **`RUNS.md`**: Information about different run formats and types.
  - **`strava_funcs.py`**: Functions related to Strava integration.

### Other Important Files
- **`README.md`**: This file.

## How to Run
Explain the steps to run your application. Include any prerequisites and commands.

### Note: You will need to run
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Additional Information
Any other relevant information the staff should know about your project.

## NewMarathonPlan Class Overview
Provide a brief overview of the `NewMarathonPlan` class and its methods.

## Constants (from p_a_constants.py)
Brief explanation of the constants file and its purpose.

## Future 
### TODOs:
- ~~Need to to check that the inputted text is valid (integers or formatted time!)~~
- ~~Implement the strava linking feature~~
- ~~Complete the completed runs template/view~~

### Future features to implement:
- Complete a better estimate for average pace
- Have a better system for recording data

### Potential bugs / features to implement
- What happens to the home page when I finish a plan, what happens to the upcomming runs after I finish a plan, what happens to the pages after I finish a plan

## License
Include details about your project's license.

## Acknowledgments
Any acknowledgments or credits you want to give.

