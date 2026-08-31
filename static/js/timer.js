/* Live Timer Counter JS */
document.addEventListener("DOMContentLoaded", () => {
    const timerDisplay = document.getElementById("live-timer-display");
    if (!timerDisplay) return;

    const startTimeStr = timerDisplay.dataset.startTime;
    if (!startTimeStr) return;

    const startDate = new Date(startTimeStr);

    setInterval(() => {
        const now = new Date();
        const diffMs = now - startDate;
        const diffSecs = Math.floor(diffMs / 1000);
        const hrs = String(Math.floor(diffSecs / 3600)).padStart(2, '0');
        const mins = String(Math.floor((diffSecs % 3600) / 60)).padStart(2, '0');
        const secs = String(diffSecs % 60).padStart(2, '0');
        timerDisplay.textContent = `${hrs}:${mins}:${secs}`;
    }, 1000);
});
