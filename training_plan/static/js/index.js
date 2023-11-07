// Listen to the index page after it is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dom Content loaded');

    // Get the Main run and change its background colour
    const mainRunBox = document.getElementById('todays-run');
    changeBackground(mainRunBox, runDictId); // runDictId imported from template

    // Get the upcomming runs and change their background
    for (let i = 0; i < upCommingRunsIds.length; i++) {
        let box = document.getElementById(`${upCommingRunsIds[i]}-upcomming-run-${upCommingRunsDictIds[i]}`);
        changeBackground(box, upCommingRunsDictIds[i]);
    }

    // Get the document values from
    const values = isRunDistance()

    // Render button and label to the DOM (not if a rest day)
    if (values.distance || values.sets) {
        const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete');
        const buttonWithLabel = displayButton();
        rootMarkAsCompletedDiv.appendChild(buttonWithLabel);
    }

    // Render info bar to the dom
    const todaysRunDiv = document.getElementById('todays-run');
    const infoBar = displayRunInfoBar(values);
    todaysRunDiv.appendChild(infoBar);

});

function changeBackground(runBox, dictId) {
    runBox.classList.remove('bg-white');
    runBox.classList.add(`bg-grad-${dictId}`);
}

// Mark as complete button and label for the index page
function displayButton() {
    let message = 'Mark As Completed';

    // Create the button element
    let button = document.createElement('a');
    button.id = `mark-complete`;
    button.classList = 'btn btn-dark';
    button.href = markAsCompletedURL;
    button.role = 'button';
    button.innerHTML = `${message}`;

    // Create the label element
    let label = document.createElement('small');
    label.classList = 'text-muted me-2';
    label.innerText = 'Mark as complete to enter your stats';

    // Create a div to hold the button and label
    let container = document.createElement('div');
    container.classList = 'd-flex align-items-center';
    container.appendChild(label);
    container.appendChild(button);

    return container;
}

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
    rootDiv.id = 'run-info-bar'
    rootDiv.classList ='m-1 hstack gap-3 fs-5'

    // I need to make it dynamic so I change both the value labels and the values!
    if (type === 'distance') {
        rootDiv.innerHTML = `
            <div id="info-bar--distance" class="m-auto">Distance: ${values.distance}km</div>
            <div class="vr"></div>
            <div id="infor-bar--duration" class="m-auto">Estimated Duration: ${values.est_duration} minutes</div>
            <div class="vr"></div>
            <div id="infor-bar--pace" class="m-auto">Estimated Pace: ${formatTime(values.est_avg_pace)}</div>
        `
    } else if (type === 'interval') {
        rootDiv.innerHTML = `
            <div id="info-bar--time" class="m-auto">Working time: ${values.on}km</div>
            <div class="vr"></div>
            <div id="infor-bar--duration" class="m-auto">Rest time: ${values.off} minutes</div>
            <div class="vr"></div>
            <div id="infor-bar--pace" class="m-auto">Sets: ${values.sets}</div>
            <div class="vr"></div>
            <div id="infor-bar--pace" class="m-auto">Estimated Pace: ${formatTime(values.est_avg_pace)}</div>
        `
    } else {
        rootDiv.innerHTML = `
            <div id="infor-bar--rest" class="fs-5">Enjoy your rest day</div>
        `
    }
    return rootDiv;
}

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

