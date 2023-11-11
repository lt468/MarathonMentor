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
                if (values.completed) {
                    editStatsOnInfoBar([values.scheduled_run, values.date, values.distance, values.duration, formatTime(values.avg_pace)]); 
                } else {
                    editStatsOnInfoBar([values.run_id, values.date, values.distance, values.est_duration, formatTime(values.est_avg_pace)]); 
                }
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

function displayRunFailureMessage(){

    let message = 'Error updating stats - check your input!';

    let div = document.createElement('div');
    div.id = 'completed-message';
    div.classList = 'alert alert-danger text-center';
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
        labelMessage = 'Press edit stats to update the run statistics';

        // Get and remove the old button
        const oldBtn = document.getElementById('mark-complete');
        if (oldBtn) {
            oldBtn.parentNode.remove();
        }

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
function updateButtonText(msg) {

    let labelText;
    let button = document.getElementById('mark-complete');
    let label = document.getElementById('mark-complete-label');

    if (msg === 'Save') {
        labelText = 'Press save to record the completed run and update the run stats';
    } else if (msg === 'Edit Stats') {
        labelText = 'Press edit stats to update the run statistics';
    }

    label.innerText = labelText;
    button.innerHTML = msg;
}

// TODO - implement the strava linking feature

// Function to edit the stats and mark the run as complete
function editStatsOnInfoBar(values) {
    // Get the info bar
    const infoBar = document.getElementById('run-info-bar');
    let valueObj = {
        run_id: values[0],
        date: values[1],
        distance: values[2],
        duration: values[3],
        pace: values[4],
    }

    let val, update, msg;

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

            update = false;
            parts = infoBarComponent.children[0].id.split('-');
            attribute = parts[0];
            let iEdit = changeSpanToTextarea(attribute);
            i += iEdit; // To make sure a div element is not skipped over in the loop

        } else if (infoBarComponent.children.length !== 0 && infoBarComponent.children[0].tagName === 'TEXTAREA') {
            update = true;
            parts = infoBarComponent.children[0].id.split('-');
            attribute = parts[0];

            val = changeTextareaToSpan(attribute); // Get the value in the textarea

            valueObj[attribute] = val;
        }
    }

    // Saving new values to the database
    if (update) {
        saveAndUpdateStats(valueObj);

    } else {
        msg = 'Save';
        updateButtonText(msg); // Update the button text 
    }
}

function saveAndUpdateStats(payload) {
    // Create the loading button
    const loadingButton = document.createElement('button');
    loadingButton.id = 'mark-complete';
    loadingButton.classList = 'btn btn-dark';
    loadingButton.type = 'button';
    loadingButton.disabled = true;

    // Create Span content for inside the button
    const spanSpinner = document.createElement('span');
    spanSpinner.classList = 'spinner-border spinner-border-sm';

    const spanLoading = document.createElement('span');
    spanLoading.role = 'status';
    spanLoading.innerHTML = `&nbsp;Saving...`;

    loadingButton.appendChild(spanSpinner);
    loadingButton.appendChild(spanLoading);

    // Get the button element inside the div
    let button = document.getElementById('mark-complete');

    // Replace the button inside the div with the loading button
    button.parentNode.replaceChild(loadingButton, button);

    button = document.getElementById('mark-complete'); // Have to get it again 
    // Changing the label of the button
    button.parentNode.children[0].innerHTML = `Updating stats, please don't refresh or exit`;

    // Validating the inputs
    const validatedPayload = validateInputPayload(payload);
    if (!validatedPayload[0]) {

        // Toast failure
        // Dismiss existing toast
        const existingToast = document.getElementById('liveToast');
        const existingToastInstance = bootstrap.Toast.getInstance(existingToast);
        if (existingToastInstance) {
            existingToastInstance.hide();
        }

        // Create and show new toast
        const pageContent = document.getElementsByClassName('page-content');
        pageContent[0].appendChild(createFailureToast());
        const newToast = document.getElementById('liveFailureToast');
        const newToastInstance = new bootstrap.Toast(newToast);
        newToastInstance.show();

        // Add the pop up failure message
        const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete');
        rootMarkAsCompletedDiv.classList = 'd-flex justify-content-between mx-5';

        rootMarkAsCompletedDiv.children[0].remove(); // Remove previous one

        const runFailureMessage = displayRunFailureMessage();
        rootMarkAsCompletedDiv.appendChild(runFailureMessage);

        // Adding button again
        const buttonWithLabel = displayButton(true);
        rootMarkAsCompletedDiv.appendChild(buttonWithLabel);
        
        // Have to attach another event listener
        const buttonElementInDiv = document.getElementById('mark-complete');

        buttonElementInDiv.addEventListener('click', event => {
            event.preventDefault();
            let payloadArr = [];
            for (const [key, value] of Object.entries(payload)) {
                payloadArr.push(value);
            }
            editStatsOnInfoBar([payloadArr[0], payloadArr[1], payloadArr[2], payloadArr[3], payloadArr[4]]);
        });
        return;
    } 

    let cleanedPayload = validatedPayload[1]; // If payload is valid;

    // Make the post request
    const prom = updateStats(cleanedPayload);

    prom.then((val) => {

        // Dismiss existing toast
        const existingToast = document.getElementById('liveToast');
        const existingToastInstance = bootstrap.Toast.getInstance(existingToast);
        if (existingToastInstance) {
            existingToastInstance.hide();
        }

        // Create and show new toast
        const pageContent = document.getElementsByClassName('page-content');
        pageContent[0].appendChild(createToast());
        const newToast = document.getElementById('liveToast');
        const newToastInstance = new bootstrap.Toast(newToast);
        newToastInstance.show();

        const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete');

        // Add the pop up success message
        rootMarkAsCompletedDiv.classList = 'd-flex justify-content-between mx-5';

        rootMarkAsCompletedDiv.children[0].remove(); // Remove previous one

        const runCompletedMessage = displayRunCompletedMessage();
        rootMarkAsCompletedDiv.appendChild(runCompletedMessage);

        // Adding button again
        const buttonWithLabel = displayButton(true);
        rootMarkAsCompletedDiv.appendChild(buttonWithLabel);
        
        // Have to attach another event listener
        const buttonElementInDiv = document.getElementById('mark-complete');

        buttonElementInDiv.addEventListener('click', event => {
            event.preventDefault();
            const paceDuration = moment.duration(val.payload.avg_pace);
            const formattedPace = moment.utc().startOf('day').add(paceDuration).format('HH:mm:ss.SSS');

            const formattedDate = moment(val.payload.date).format('YYYY-MM-DD');
            editStatsOnInfoBar([val.payload.run_id, formattedDate, val.payload.distance, val.payload.duration, formatTime(formattedPace)]);
        });

    }).catch((error) => {
        console.error('Update failed: ', error);
        // Additional code to handle the error
    });
}

function validateInputPayload(payload) {

    for (const [key, value] of Object.entries(payload)) {
        switch (key) {
            case 'distance':
            case 'duration':
                let trimmedInput = value.trim(); // Remove leading and trailing whitespaces
                const regex = /^[0-9]+(\.[0-9]+)?$/;
                if (!(regex.test(trimmedInput))) {
                    return [false, payload]; // Contains non-numbers
                }

                let numericValue = parseFloat(trimmedInput); // Parse the input as a float

                let intValue = parseInt(numericValue);

                // Check for fail conditions
                if (
                    trimmedInput === '' ||            // Empty string
                    isNaN(intValue)             // Not a number (NaN)
                ) {
                    return [false, payload];
                }

                // Update value if data is valid
                payload[key] = Math.floor(intValue); // Use Math.floor to remove the decimal part
                break;

            case 'pace':
                let paceValue = value.trim(); // Remove leading and trailing whitespaces
                let paceRegex = /^(\d+):(\d+)$/; // Regular expression for mm:ss format

                // Check for fail conditions
                if (
                    paceValue === '' ||                    // Empty string
                        !paceRegex.test(paceValue) ||          // Not matching mm:ss format
                        paceValue.includes('-') ||             // Contains a nonnumeric value or a hyphen
                        paceValue.includes(' ') ||             // Contains whitespace
                        paceValue.includes(':') === false      // Does not contain ':'
                ) {
                    return [false, payload];
                }

                // Parse minutes and seconds
                let match = paceValue.match(paceRegex);
                let minutes = parseInt(match[1], 10);
                let seconds = parseInt(match[2], 10);

                // Check for invalid integer values
                if (isNaN(minutes) || isNaN(seconds)) {
                    return [false, payload];
                }

                // Update value if data is valid
                payload[key] = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                break;

            default:
                payload[key] = value;
                break;
        }
    }
    return [true, payload];
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

    // Copy the content from the textarea to the span
    let innerHTMLObj = {
        [attribute]: textarea.value
    }
    let cleanedInner = validateInputPayload(innerHTMLObj);

    if (cleanedInner[0]) {
        span.innerHTML = cleanedInner[1][attribute];
    } else {
        span.classList = 'text-danger';
        span.innerHTML = textarea.value;
    }

    // Replace the span with the textarea in the DOM
    textarea.parentNode.replaceChild(span, textarea);

    return span.innerHTML;
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
async function updateStats(payload) {

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
            const responseData = await response.json();  // Parse the response data
            return responseData;  // Return the response data (including the payload)
        } else {
            const errorResponse = await response.json();  // Parse the error response data
            console.error('Error updating run:', errorResponse.error);  // Log the error message
            throw new Error('Error updating run');
        }
    } catch (error) {
        throw error;  // Re-throw the error to propagate it to the caller
    }
}

// API to get the todays run and all of its attributes
async function getTodaysRun() {
    const url = '/api/get-todays-run';
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

// Adding toast
function createToast(){
    const toastDiv = document.createElement('div');
    toastDiv.classList = 'toast-container position-fixed bottom-0 end-0 p-3';
    toastDiv.innerHTML = `
        <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <img src="${logoImagePath}" class="rounded me-2" width="24" height="24" alt="Marathon Mentor Dark Logo">
                <strong class="me-auto">Marathon Mentor</strong>
                <small class="text-body-secondary">now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                Run Statistics Saved!
            </div>
        </div>
    `;

    return toastDiv;
}

// Adding failure toast
function createFailureToast(){
    const toastDiv = document.createElement('div');
    toastDiv.classList = 'toast-container position-fixed bottom-0 end-0 p-3';
    toastDiv.innerHTML = `
        <div id="liveFailureToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <img src="${logoImagePath}" class="rounded me-2" width="24" height="24" alt="Marathon Mentor Dark Logo">
                <strong class="me-auto">Marathon Mentor</strong>
                <small class="text-body-secondary">now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                Run Statistics Failed to Save - Error In Input
            </div>
        </div>
    `;

    return toastDiv;
}
