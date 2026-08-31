/* Vanilla JS HTML5 Drag and Drop Kanban Board Controller */
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".kanban-card");
    const columns = document.querySelectorAll(".kanban-cards");

    let draggedCard = null;

    cards.forEach(card => {
        card.addEventListener("dragstart", (e) => {
            draggedCard = card;
            card.classList.add("dragging");
            e.dataTransfer.setData("text/plain", card.dataset.taskId);
        });

        card.addEventListener("dragend", () => {
            card.classList.remove("dragging");
            draggedCard = null;
        });
    });

    columns.forEach(column => {
        column.addEventListener("dragover", (e) => {
            e.preventDefault();
            column.style.background = "#e0e7ff";
        });

        column.addEventListener("dragleave", () => {
            column.style.background = "";
        });

        column.addEventListener("drop", async (e) => {
            e.preventDefault();
            column.style.background = "";
            const taskId = e.dataTransfer.getData("text/plain");
            const newStatus = column.dataset.status;

            if (draggedCard && taskId) {
                column.appendChild(draggedCard);

                // Send AJAX update
                try {
                    const response = await fetch("/kanban/move", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-Requested-With": "XMLHttpRequest"
                        },
                        body: JSON.stringify({ task_id: taskId, new_status: newStatus })
                    });
                    const res = await response.json();
                    if (res.success) {
                        console.log("Card moved successfully:", res.message);
                    } else {
                        alert("Error moving task: " + res.error);
                    }
                } catch (err) {
                    console.error("Failed to move card:", err);
                }
            }
        });
    });
});
