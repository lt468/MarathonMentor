// Listen to the index page after it is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dom Content loaded');

    const result = apiGetScheduledRuns();
    result.then(data => console.log(data));
});

async function apiGetScheduledRuns() {
    const url = "api/get-scheduled-runs";
    const response = await fetch(url);
    const all_scheduled_runs = await response.json();
    console.log(all_scheduled_runs);
}
