// Listen to the index page after it is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dom Content loaded');

    // Get the document values from api
    const valuesPromise = getTodaysRun();
    valuesPromise.then(values => {

        // Render button and label to the DOM (not if a rest day)
        if (values.distance || values.sets) {
            const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete');
            const buttonWithLabel = displayButton();
            rootMarkAsCompletedDiv.appendChild(buttonWithLabel);

            // Get the button within the label and button div
            const buttonElementInDiv = buttonWithLabel.querySelector('button');

            buttonElementInDiv.addEventListener('click', event => {
                event.preventDefault();
                editStatsAndMarkRunComplete(values); 
                updateButtonText();
            });
        }

        // Render info bar to the dom for the first time when the page loads
        const todaysRunDiv = document.getElementById('todays-run');
        const infoBar = displayRunInfoBar(values);
        todaysRunDiv.appendChild(infoBar);

    });

    // Get the Main run and change its background colour
    const mainRunBox = document.getElementById('todays-run');
    changeBackground(mainRunBox, runDictId); // runDictId imported from template

    // Get the upcomming runs and change their background
    for (let i = 0; i < upCommingRunsIds.length; i++) {
        let box = document.getElementById(`${upCommingRunsIds[i]}-upcomming-run-${upCommingRunsDictIds[i]}`);
        changeBackground(box, upCommingRunsDictIds[i]);
    }

    updateStats();

});

// Function to change the background of the divs for each of the run
function changeBackground(runBox, dictId) {
    runBox.classList.remove('bg-white');
    runBox.classList.add(`bg-grad-${dictId}`);
}

// Mark as complete button and label for the index page
function displayButton() {
    let message = 'Mark As Completed';

    // Create the button element
    let button = document.createElement('button');
    button.id = 'mark-complete';
    button.classList = 'btn btn-dark';
    button.type = 'submit';
    button.role = 'button';
    button.innerHTML = `${message}`;

    // Create the label element
    let label = document.createElement('small');
    label.id = 'mark-complete-label'
    label.classList = 'text-muted me-2';
    label.innerText = 'Mark as completed to enter your stats';

    // Create a div to hold the button and label
    let container = document.createElement('div');
    container.classList = 'd-flex align-items-center';
    container.appendChild(label);
    container.appendChild(button);

    return container;
}

// Function to update the button text
function updateButtonText() {
    // Check here to see if there is already a completed run in the database, if so, then use 'edit' and 'save' and no 'mark as complete'

    let message;
    let labelText;
    const button = document.getElementById('mark-complete');
    const label = document.getElementById('mark-complete-label');

    if (button.innerHTML === 'Mark As Completed') {
        message = 'Save';
        labelText = 'Press save to record the completed run and update the run stats'
    } else {
        message = 'Mark As Completed';
        labelText = 'Mark as complete to enter your stats';
    }

    label.innerText = labelText;
    button.innerHTML = message;
}

// Function to edit the stats and mark the run as complete
function editStatsAndMarkRunComplete(values) {

    // Check to see if the run is a distance or interval based run
    if (values['distance']) {
        // Grab the stats in the info bar for the distance based runs
        let distDiv;  

        let durDiv = {
            element: document.getElementById('info-bar--duration'),
            editableElement: document.getElementById('duration--edit'),
            duration: values.est_duration
        }

        let paceDiv = {
            element: document.getElementById('info-bar--pace'),
            editableElement: document.getElementById('pace--edit'),
            pace: values.est_avg_pace
        }

        let payload = {}

        //date = models.DateField(help_text="Date when run was completed")
        //distance = models.PositiveIntegerField(help_text="Distance of completed run in km")
        //duration = models.PositiveIntegerField(help_text="Duration of completed run in minutes")
        //avg_pace = models.DurationField(verbose_name="Average Pace", help_text="Please format like mm:ss")  

        // Will need to change three different divs to a text area in edit mode
        const inEditMode = document.getElementById('distance--edit').tagName === 'TEXTAREA'; // Look to see if in edit mode or not
        
        // TODO - Need to check if it's completed first by seeing if the api returns something
        // TODO - Need to to check that the inputted text is valid (integers or formatted time!)
        if (inEditMode) {

            // Grab the current value
            distDiv = {
                element: document.getElementById('info-bar--distance'),
                editableElement: document.getElementById('distance--edit'),
                distance : function() {
                    return document.getElementById('distance--edit').value;
                }
            }

            // TODO - Save the stats and mark as completed (via api)
            distDiv.element.outerHTML = `<div id="info-bar--distance" class="d-flex justify-content-center m-auto align-middle">Distance:&nbsp;<span id="distance--edit">${distDiv.distance()}</span>km</div>`
            durDiv.element.outerHTML = `<div id="info-bar--duration" class="d-flex justify-content-center m-auto align-middle">Duration:&nbsp;<span id="duration--edit">${durDiv.duration}</span>&nbsp;minutes</div>`
            paceDiv.element.outerHTML = `<div id="info-bar--pace" class="d-flex justify-content-center m-auto align-middle">Average Pace:&nbsp;<span id="pace--edit">${formatTime(paceDiv.pace)}</span></div>`

        } else {

            // Grab the current value
                distDiv = {
                element: document.getElementById('info-bar--distance'),
                editableElement: document.getElementById('distance--edit'),
                distance: values.distance
            }


            const currentDistDivContent = distDiv.editableElement.textContent;
            distDiv.editableElement.outerHTML = `<textarea id="distance--edit" class="align-middle fs-5 mx-1 form-control form-control-info-bar">${currentDistDivContent}</textarea>`;

            const currentDurDivContent = durDiv.editableElement.textContent;
            const durDivEditableContent = `<textarea id="duration--edit" class="align-middle fs-5 mx-1 form-control form-control-info-bar">${currentDurDivContent}</textarea>`;
            durDiv.editableElement.outerHTML = durDivEditableContent;
            durDiv.element.outerHTML = `<div id="info-bar--duration" class="d-flex justify-content-center m-auto align-middle">Duration:&nbsp;${durDivEditableContent}&nbsp;minutes</div>`

            const currentPaceDivContent = paceDiv.editableElement.textContent;
            const paceDivEditableContent = `<textarea id="pace--edit" class="align-middle fs-5 mx-1 form-control form-control-info-bar">${currentPaceDivContent}</textarea>`;
            paceDiv.editableElement.outerHTML = paceDivEditableContent;
            paceDiv.element.outerHTML = `<div id="info-bar--pace" class="d-flex justify-content-center m-auto align-middle">Average Pace:&nbsp;${paceDivEditableContent}</div>`
        }

    } else if (values['sets']) {
        type = 'interval';
    } else {
        alert('You cannot mark a rest day as complete!');
        return;
    }

}

// Function to display the stats of the run within the today's run div
function displayRunInfoBar(values) {

    // Check to see if the run is a distance or interval based run
    let type;
    if (values['distance']) {
        type = 'distance';
    } else if (values['sets']) {
        type = 'interval';
    } else {
        type = 'rest';
    }

    let rootDiv = document.createElement('div');
    rootDiv.id = 'run-info-bar';
    rootDiv.classList ='m-1 hstack gap-3 fs-5 align-middle';

    // Creating the inner HTML for the info bar
    if (type === 'distance') {
        rootDiv.innerHTML = `
            <div id="info-bar--distance" class="d-flex justify-content-center m-auto align-middle">Distance:&nbsp;<span id="distance--edit">${values.distance}</span>km</div>
            <div class="vr"></div>
            <div id="info-bar--duration" class="d-flex justify-content-center m-auto align-middle">Estimated Duration:&nbsp;<span id="duration--edit">${values.est_duration}</span>&nbsp;minutes</div>
            <div class="vr"></div>
            <div id="info-bar--pace" class="d-flex justify-content-center m-auto align-middle">Estimated Pace:&nbsp;<span id="pace--edit">${formatTime(values.est_avg_pace)}</span></div>
        `
    } else if (type === 'interval') {
        rootDiv.innerHTML = `
            <div id="info-bar--time" class="m-auto">Working time: ${values.on}km</div>
            <div class="vr"></div>
            <div id="info-bar--duration" class="m-auto">Rest time: ${values.off} minutes</div>
            <div class="vr"></div>
            <div id="info-bar--pace" class="m-auto">Sets: ${values.sets}</div>
            <div class="vr"></div>
            <div id="info-bar--pace" class="m-auto">Estimated Pace: ${formatTime(values.est_avg_pace)}</div>
        `
    } else {
        rootDiv.innerHTML = `
            <div id="info-bar--rest" class="fs-5">Enjoy your rest day</div>
        `
    }
    return rootDiv;
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
        date: "8 Nov 2023",
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

    return data;
}
