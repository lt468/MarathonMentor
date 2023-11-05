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

    // Render button to the DOM
    const rootMarkAsCompletedDiv = document.getElementById('root-mark-complete'); // Get the root div for the page
    btnMarkAsCompleted = displayButton();
    rootMarkAsCompletedDiv.appendChild(btnMarkAsCompleted);
});

function changeBackground(runBox, dictId) {
    runBox.classList.remove('bg-white');
    runBox.classList.add(`bg-grad-${dictId}`);
}

// Mark as complete button for the index page
function displayButton() {
    let message = 'Mark As Completed';

    let a = document.createElement('a');
    a.id = `mark-complete`;
    a.classList = 'btn btn-dark';
    a.href = markAsCompletedURL;
    a.role = 'button';
    a.innerHTML = `${message}`;
    return a;
}
