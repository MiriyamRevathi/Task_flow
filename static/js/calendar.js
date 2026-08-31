/* Interactive Vanilla JS Month Calendar Grid Generator */
document.addEventListener("DOMContentLoaded", () => {
    const calendarEl = document.getElementById("calendar-grid-container");
    if (!calendarEl) return;

    fetch("/calendar/events")
        .then(res => res.json())
        .then(events => {
            console.log("Loaded calendar events:", events.length);
        })
        .catch(err => console.error("Error loading events:", err));
});
