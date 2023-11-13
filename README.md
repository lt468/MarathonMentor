# MarathonMentor
A Web Application that is able to create a tailored Marathon training plan. This is my CS50w Final Project.

## Overview
Brief overview of your project.

## Distinctiveness and Complexity
### Why your project satisfies the distinctiveness and complexity requirements
Explain how your project is distinct from others in the course, especially from projects like the social network or e-commerce site. Discuss the complexity of your project.

## Project Files
### Django App Files
- **`MarathonMentor/`**: Django project folder.
  - **`settings.py`**: Django settings.
  - **`urls.py`**: URL patterns.

### Training Plan App Files
- **`training_plan/`**: Django app folder.
  - **`admin.py`**: Django admin configuration.
  - **`apps.py`**: App configuration.
  - **`forms.py`**: Forms used in the app.
  - **`models.py`**: Django models for the app.
  - **`static/`**: Folder for static files (CSS, JS, images).
    - **`css/`**: Folder for CSS files.
      - **`styles.scss`**: Main SCSS file.
    - **`js/`**: Folder for JavaScript files.
      - **`completedRuns.js`**: JavaScript file for completed runs.
      - **`index.js`**: Main JavaScript file.
      - **`scheduledRuns.js`**: JavaScript file for scheduled runs.
  - **`templates/`**: Folder for HTML templates.
    - **`registration/`**: Folder for registration-related templates.
      - **`login.html`**: Login template.
      - **`nonavbar.html`**: Template without a navigation bar.
      - **`password_reset_complete.html`**: Password reset completion template.
      - **`password_reset_confirm.html`**: Password reset confirmation template.
      - **`password_reset_done.html`**: Password reset done template.
      - **`password_reset_form.html`**: Password reset form template.
      - **`register.html`**: Registration template.
    - **`training_plan/`**: Folder for training plan-related templates.
      - **`completed_runs.html`**: Template for completed runs.
      - **`index.html`**: Main index template.
      - **`navbar_layout.html`**: Template with a navigation bar.
      - **`scheduled_runs.html`**: Template for scheduled runs.
      - **`settings.html`**: Settings template.
  - **`templatetags/`**: Folder for template tags.
    - **`custom_filters.py`**: Custom template filters.
  - **`tests.py`**: Test cases for the app.
  - **`urls.py`**: URL patterns for the app.
  - **`utils/`**: Folder for utility files.
    - **`p_a_constants.py`**: Constants used in the training plan algorithm.
    - **`plan_algo.py`**: Main training plan algorithm.
    - **`RUNS.md`**: Information about different run formats and types.
    - **`strava_funcs.py`**: Functions related to Strava integration.
  - **`views.py`**: Views for the app.

## How to Run
Explain the steps to run your application. Include any prerequisites and commands.

### Requirements

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
- Tell the user when registering that their plan is being created
- Create some Tests
- Need to improve the plan_algo pyton code, make it more efficient, add more features, improve the javascript files!

### Potential bugs / features to implement
- What happens to the home page when I finish a plan, what happens to the upcomming runs after I finish a plan, what happens to the pages after I finish a plan

## License
Include details about your project's license.

## Acknowledgments
Any acknowledgments or credits you want to give.

