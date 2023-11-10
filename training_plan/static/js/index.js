// Listen to the index page after it is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dom Content loaded');

    // Get the document values from api
    const valuesPromise = getTodaysRun();
    valuesPromise.then(values => {

        // Render button and label to the DOM (not if a rest day)
        if (values.distance || values.sets) {
            const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete');

            // Render info bar to the dom for the first time when the page loads
            const todaysRunDiv = document.getElementById('todays-run');
            const infoBar = displayRunInfoBar(values);
            todaysRunDiv.appendChild(infoBar);
 
            // If the run is complete, render a well done message
            if (values.completed) {
                rootMarkAsCompletedDiv.classList = 'd-flex justify-content-between mx-5';
                const runCompletedMessage = displayRunCompletedMessage();
                rootMarkAsCompletedDiv.appendChild(runCompletedMessage);
            }

            const buttonWithLabel = displayButton(values.completed);
            rootMarkAsCompletedDiv.appendChild(buttonWithLabel);

            // Get the button within the label and button div
            const buttonElementInDiv = buttonWithLabel.querySelector('button');

            buttonElementInDiv.addEventListener('click', event => {
                event.preventDefault();
                editStatsOnInfoBar(); 
                updateButtonText(values.completed);
            });
        }
    });

    // Get the Main run and change its background colour
    const mainRunBox = document.getElementById('todays-run');
    changeBackground(mainRunBox, runDictId); // runDictId imported from template

    // Get the upcomming runs and change their background
    for (let i = 0; i < upCommingRunsIds.length; i++) {
        let box = document.getElementById(`${upCommingRunsIds[i]}-upcomming-run-${upCommingRunsDictIds[i]}`);
        changeBackground(box, upCommingRunsDictIds[i]);
    }

    // TODO - Ensure correct order of operations
    updateStats();

});

function displayRunCompletedMessage(){

    let message = 'This run has been completed - well done!';

    let div = document.createElement('div');
    div.id = 'completed-message';
    div.classList = 'alert alert-success text-center';
    div.role = 'alert';
    div.innerHTML = `<h5 class="alert-heading">${message}</h5>`;

    return div;
}

// Function to change the background of the divs for each of the run
function changeBackground(runBox, dictId) {
    runBox.classList.remove('bg-white');
    runBox.classList.add(`bg-grad-${dictId}`);
}

// Mark as complete button and label for the index page
function displayButton(completed) {

    let message;
    let labelMessage

    if (completed) {
        message = 'Edit Stats';
        labelMessage = 'Press edit stats to update the run stats';

    } else {
        message = 'Mark As Completed';
        labelMessage = 'Mark as completed to enter your stats';
    }


    // Create the button element
    let button = document.createElement('button');
    button.id = 'mark-complete';
    button.classList = 'btn btn-dark';
    button.type = 'submit';
    button.role = 'button';
    button.innerText = message;

    // Create the label element
    let label = document.createElement('small');
    label.id = 'mark-complete-label'
    label.classList = 'text-muted me-2';
    label.innerText = labelMessage;

    // Create a div to hold the button and label
    let container = document.createElement('div');
    container.classList = 'd-flex align-items-center';
    container.appendChild(label);
    container.appendChild(button);

    return container;
}

// Function to update the button text
function updateButtonText(completed) {

    let message;
    let labelText;
    const button = document.getElementById('mark-complete');
    const label = document.getElementById('mark-complete-label');

    if (completed) {
        message = 'Edit Stats';
        label = 'Press edit stats to update the run stats';
    } else if (button.innerHTML === 'Mark As Completed') {
        // TODO - backend (and frontend loading) update when pressed here 
        message = 'Save';
        labelText = 'Press save to record the completed run and update the run stats'
    } else {
        message = 'Mark As Completed';
        labelText = 'Mark as complete to enter your stats';
    }

    label.innerText = labelText;
    button.innerHTML = message;
}

// The initial info bar is now implemented when the page is loaded for the first time, now implement the system for updating and saving the run for the first
// time and also when the user wants to update the stats. Implement visuals so that the user knows that it's saving (spinner and disable text area), provide
// a front end message to confirm it's the case, and then send the appropriate request to the backend and db. Finally, update the completed run page, and then
// after that, implement the strava linking feature

        //date = models.DateField(help_text="Date when run was completed")
        //distance = models.PositiveIntegerField(help_text="Distance of completed run in km")
        //duration = models.PositiveIntegerField(help_text="Duration of completed run in minutes")
        //avg_pace = models.DurationField(verbose_name="Average Pace", help_text="Please format like mm:ss")  

        // TODO - Need to check if it's completed first by seeing if the api returns something
        // TODO - Need to to check that the inputted text is valid (integers or formatted time!)

// Function to edit the stats and mark the run as complete
function editStatsOnInfoBar() {

    // Get the info bar
    const infoBar = document.getElementById('run-info-bar');
    let new_values = [];

    // Loop through components
    for (let i = 0; i < infoBar.children.length; i++) {
        let infoBarComponent = infoBar.children[i];
        let parts, attribute;

        // Check if the innerHTML contains the word "Estimated"
        if (infoBarComponent.innerHTML.includes("Estimated")) {
          // Remove the word "Estimated" from the innerHTML
          infoBarComponent.innerHTML = infoBarComponent.innerHTML.replace("Estimated", "");
        }

        if (infoBarComponent.children.length !== 0 && infoBarComponent.children[0].tagName === 'SPAN') {
            parts = infoBarComponent.children[0].id.split('-');
            attribute = parts[0];
            let iEdit = changeSpanToTextarea(attribute);
            i += iEdit; // To make sure a div element is not skipped over in the loop

        } else if (infoBarComponent.children.length !== 0 && infoBarComponent.children[0].tagName === 'TEXTAREA') {
            parts = infoBarComponent.children[0].id.split('-');
            attribute = parts[0];
            changeTextareaToSpan(attribute);

            // Saving new values to the database 
        }
    }
}

function updateRunInDatabase() {

}

// Function to display the stats of the run within the today's run div
function displayRunInfoBar(values) {

    let distance, duration, pace, sets, on, off, data;

    // Check to see if the page nees to display the completed run or the scheduled run, and what type of run
    if (values.completed) {
        distance = values.distance;
        duration = values.duration;
        pace = formatTime(values.avg_pace);
        data = {distance, duration, pace};

    } else if (!values.completed && values['distance']) { 
        distance = values.distance;
        duration = values.est_duration;
        pace = formatTime(values.est_avg_pace);
        data = {distance, duration, pace};

    } else if (!values.completed && values['sets']) {
        sets = values.sets;
        on = values.on;
        off = values.off;
        pace = formatTime(values.est_avg_pace);
        data = {on, off, sets, pace};
    }

    let rootDiv = document.createElement('div');
    rootDiv.id = 'run-info-bar';
    rootDiv.classList ='d-flex justify-content-evenly fs-5 mb-1 align-middle';

    // Creating the inner HTML for the info bar
    let lastIndex = 0;

    // Loop over the object's keys (variable names) and values
    for (const variableName in data) {
        comp = new infoBarComponent(variableName, data[variableName], values.completed);
        compDiv = comp.createComponent();
        rootDiv.append(compDiv);

        if (lastIndex === Object.keys(data).length - 1) {
            break; // Exit the loop before the last element
        }
        lastIndex++;
        rootDiv.appendChild(createVerticalDiv());
    }
    return rootDiv;
}

// Create a vertical line div
function createVerticalDiv() {
    let div = document.createElement('div');
    div.classList = 'vr';
    return div;
}

// Change the editable component from a span to a textarea
function changeSpanToTextarea(attribute) {
    // Get the span that needs to be changed
    let span =  document.getElementById(`${attribute}--edit`);

    // If the run was an interval, need to change the attributes to enter, will do this by discarding the 'on' attribute, changing the 
    // 'off' to 'distance' and the 'sets' to 'duration'; the 'pace' will remain the same
    if (attribute === 'on') {
        span.parentNode.remove();
        document.querySelector('.vr').remove(); // Remove the first vr
        return -1; // To make sure a div element is not skipped over in the loop

    } else if (attribute === 'off') {
        span.parentNode.innerHTML = span.parentNode.innerHTML.replace('Off', 'Distance');
        span = document.getElementById(`${attribute}--edit`); // Have to grab it again to make it work
        span.parentNode.innerHTML = span.parentNode.innerHTML.replace('&nbsp;minutes', 'km');
        span = document.getElementById(`${attribute}--edit`); // Grab it one more time for replacing things
        span.innerHTML = ''; // Clearing the value so that user can fill it in
        attribute = 'distance';

    } else if (attribute === 'sets') {
        span.parentNode.innerHTML = span.parentNode.innerHTML.replace('Sets', 'Duration');
        span = document.getElementById(`${attribute}--edit`); // Have to grab it again to make it work
        span.parentNode.innerHTML += 'minutes';
        span = document.getElementById(`${attribute}--edit`); // Grab it one more time for replacing things
        span.innerHTML = ''; // Clearing the value so that user can fill it in
        attribute = 'duration';
    }

    // Create a new textarea element
    const textarea = document.createElement('textarea');
    textarea.id = `${attribute}--edit`; // Same ID

    if (attribute === 'pace')  {
        textarea.classList = 'fs-5 form-control form-control-info-bar';
    } else {
        textarea.classList = 'fs-5 form-control form-control-info-bar-d';
    }

    // Copy the content from the span to the textarea
    textarea.value = span.innerHTML;

    // Replace the span with the textarea in the DOM
    span.parentNode.replaceChild(textarea, span);
    return 0;
}

// Change the editable component from a textarea to a span - Exact opposite operations to the method above
function changeTextareaToSpan(attribute) {

    const textarea =  document.getElementById(`${attribute}--edit`);

    // Create a new textarea element
    const span = document.createElement('span');
    span.id = `${attribute}--edit`; // Same ID
    span.classList = ''; // Remove all the classes

    // Copy the content from the span to the textarea
    span.innerHTML = textarea.value;

    // Replace the span with the textarea in the DOM
    textarea.parentNode.replaceChild(span, textarea);
}


// Creating of the info bar components for displaying the stats
class infoBarComponent {
    constructor(attribute, value, completed) {
        this.attribute = attribute; // The distance, duration, pace, sets, on, off, etc., attribute
        this.value = value; // The value of the attribute, e.g., 8 (km) or 40 (minutes)
        this.completed = completed; // If the run has been completed
    }

    createComponent() {
        const prefix = this.#createPrefix();
        const suffix = this.#createSuffix();

        let span = this.#createSpan();
        let div = this.#createDiv();

        div.innerHTML = `${prefix}&nbsp;`;
        div.appendChild(span);
        if (!(this.attribute === 'distance')) {
            div.innerHTML += '&nbsp;';
        }
        div.innerHTML += suffix;

        return div;
    }

    #createPrefix() {
        let pre = 'Estimated';
        if (this.attribute === 'pace') {
            pre = 'Average';
        } else if (this.completed || !(this.attribute === 'duration')) {
            pre = '';
        }

        const prefix = `${pre}&nbsp;${capitalizeFirstLetter(this.attribute)}:`;
        return prefix;
    }

    #createSuffix() {
        let suf;
        switch (this.attribute) {
            case 'distance':
                suf = 'km';
                break;
            case 'duration':
                suf = 'minutes';
                break;
            case 'on':
                suf = 'minutes';
                break;
            case 'off':
                suf = 'minutes';
                break;
            default:
                suf = '';
                break;
        }

        return suf;
    }

    #createDiv() {
        let div = document.createElement('div');
        div.id = `info-bar--${this.attribute}`;
        div.classList = 'd-flex justify-content-center align-middle';
        return div;
    }

    #createSpan() {
        let span = document.createElement('span');
        span.id = `${this.attribute}--edit`;
        span.innerHTML = this.value;
        return span;
    }
}

// Helper function to capitalize the first letter
function capitalizeFirstLetter(word) {
    if (typeof word !== 'string' || word.length === 0) {
        return word; // Return the word unchanged if it's not a string or an empty string
    }

    return word.charAt(0).toUpperCase() + word.slice(1);
}

// Helper function that formats the time in the mm:ss format
function formatTime(timeString) {
    // Split the time string
    const timeParts = timeString.split(':');
    
    // Extract minutes and seconds
    const minutes = timeParts[1];
    const seconds = Math.round(parseFloat(timeParts[2]));
    
    // Format minutes and seconds with leading zeros
    const formattedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    
    return formattedTime;
}

// API to post updated values to Completed runs and change the front end
async function updateStats() {
    const payload = {
        run_id: 1754,
        date: "9 Oct 2024",
        distance: 8,
        duration: 35,
        avg_pace: "0:04:17.352941"
    } 

    // Payload is: run_id, date, distance, duration, avg_pace
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        };

        // While waiting the response, change the button and textareas to disable it and a spinner loading so that can't change the values
        const response = await fetch('/api/update-completed-run', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                payload: payload
            })
        });

        if (response.ok) {
            console.log('Run updated/posted successfully');
        } else {
            console.error('Error updating run');
        }
    } catch (error) {
        console.error('Error updating run:', error);
    }
}


// API to get the todays run and all of its attributes
async function getTodaysRun() {

    const url = '/api/get-todays-run';
    const response = await fetch(url);
    const data = await response.json();

    console.log(data)

    return data;
}
