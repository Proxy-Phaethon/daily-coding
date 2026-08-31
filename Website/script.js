const selector = document.getElementById("project-select");
const display = document.getElementById("project-display");

selector.addEventListener("change", () => {
    if (selector.value === "calculator") {
        display.innerHTML = `
            <h2>Calculator</h2>
            <p>A simple Python calculator.</p>
            <p>Interactive version coming soon.</p>
        `;
    }
});