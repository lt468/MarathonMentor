// Listen to the index page after it is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Months from numbers
    numbersToMonths = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

    const result = apiGetScheduledRuns();

    const rootDiv = document.getElementById('scheduled-runs-container'); // Get the root div for the page

    // Initialize variables to keep track of the current month
    let currentMonth = '';
    let monthHeading = null;

    // Loop through each of the runs and add them to the page
    result.then(data => {
        for (run of data.all_scheduled_runs) {
            const runDate = formatDate(run.date);
            const runMonth = runDate.split('/')[1]; 

            // Check if the month has changed
            if (runMonth !== currentMonth) {
                // Create a new heading for the month
                currentMonth = runMonth.toString();
                monthHeading = createMonthHeading(numbersToMonths[currentMonth]);
                rootDiv.appendChild(monthHeading);
            }

            // Create a new div for the run
            const runDiv = displayRun(run.id, run.dict_id, run.run, run.run_feel, runDate);
            rootDiv.appendChild(runDiv);
        }
    });


    // Go to top button - (taken from https://www.w3schools.com/howto/howto_js_scroll_to_top.asp)
    let mybutton = document.getElementById('scheduled-top-btn');

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {scrollFunction()};

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

});

// Reformat date
function formatDate(inDate) {

    const [year, month, day] = inDate.split("-");
    // Create a new date string in "dd/mm/yy" format
    const outputDate = `${day}/${month}/${year.slice(2)}`;
    return outputDate;
}

// Function to generate the div of each run to append to the DOM
function displayRun(id, dict_id, run, run_feel, date) {
    let div = document.createElement('div');
    div.id = `${id}-upcomming-run-${dict_id}`;
    div.innerHTML = `
<span <h6> ${run} | <small class="text-body-secondary align-middle">${run_feel}</small> </h6> </span>
<span>${date}</span>
`;
    div.className = `d-flex justify-content-between my-2 p-2 bg-grad-${dict_id} border border-secondary rounded align-middle`;
    return div;
}

// Function to create a heading for the month
function createMonthHeading(month) {
    const heading = document.createElement('h6');
    heading.innerHTML = month;
    heading.className = 'display-6';
    return heading;
}

// API to get the scheduled runs for a user
async function apiGetScheduledRuns() {
    const url = "api/get-scheduled-runs";
    const response = await fetch(url);
    const all_scheduled_runs = await response.json();
    return all_scheduled_runs;
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 
