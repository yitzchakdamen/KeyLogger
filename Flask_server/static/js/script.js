
// פונקציות לטיפול באירועים
document.addEventListener('DOMContentLoaded', function() {
    // טיפול באירועי לחיצה על כפתורים
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('data-action')) {
            const action = e.target.dataset.action;
            const dateFields = document.getElementById('date-fields');
            if (dateFields) {
                dateFields.style.display = 'block';
                const selectedAction = document.getElementById('selected-action');
                if (selectedAction) {
                    selectedAction.value = action;
                }
            }
        }
    });
});
// פונקציה לקבלת מידע על המחשבים המחוברים
async function getMachineInfo() {
    try {
        const response = await fetch("http://localhost:5000/get_info");
        const data = await response.json();

        const machineInfoDiv = document.getElementById("machine-info");
        if (machineInfoDiv) {
            machineInfoDiv.innerHTML = `<h2>🔍 מחשבים מחוברים: ${data.num_machines}</h2>`;

            console.log("Machine data:", data.machine_data);
            Object.entries(data.machine_data).forEach(([machine, info]) => {
                console.log(`Adding machine: ${machine}, Start Date: ${info.start_date}, Event Count: ${info.event_count}`);

                const machineBox = document.createElement("div");
                machineBox.classList.add("result-box");
                machineBox.innerHTML = `
                    <p><strong>🖥️ מחשב:</strong> ${machine}</p>
                    <p><strong>📅 תאריך התחלה:</strong> ${info.start_date}</p>
                    <p><strong>📊 כמות נתונים:</strong> ${info.event_count}</p>
                `;
                machineInfoDiv.appendChild(machineBox);
            });
        }
    } catch (error) {
        console.error("Error loading machine info:", error);
        const machineInfoDiv = document.getElementById("machine-info");
        if (machineInfoDiv) {
            machineInfoDiv.innerHTML = "<p>שגיאה בטעינת הנתונים</p>";
        }
    }
}
// קריאה לפונקציה בעת טעינת הדף
window.onload = function() {
    getMachineInfo();
};
// פונקציה לשליחת בקשה לשרת
async function sendRequest() {
    try {
        const action = document.getElementById('selected-action')?.value;
        if (!action) {
            console.error('No action selected');
            return;
        }

        // בדיקת אישור לפני מחיקת נתונים
        if (action === 'delete_data' && !confirm("האם אתה בטוח שברצונך למחוק את הנתונים?")) {
            return;
        }

        // איסוף כל הפרמטרים
        const params = new URLSearchParams({
            computer_name_device_id: document.getElementById('machine_name')?.value || '',
            year: document.getElementById('year')?.value || '',
            month: document.getElementById('month')?.value || '',
            day: document.getElementById('day')?.value || '',
            hour: document.getElementById('hour')?.value || '',
            minute: document.getElementById('minute')?.value || ''
        });

        // שליחת בקשה לשרת
        const response = await fetch(`http://localhost:5000/${action}?${params}`);
        const data = await response.json();

        // עדכון תיבת התוצאות
        const resultDiv = document.getElementById('result');
        if (resultDiv) {
            resultDiv.innerHTML = '';

            if (action === "get_data" && data.length > 0) {
                data.forEach(event => {
                    resultDiv.innerHTML += `
                        <div class='result-box'>
                            <p><strong>מחשב:</strong> ${event.machine_name}</p>
                            <p><strong>תאריך:</strong> ${event.date}</p>
                            <p><strong>נתונים:</strong> ${event.data.replace(/\\u2193/g, "↓")}</p>
                        </div>
                    `;
                });
            } else {ד
                resultDiv.innerHTML = `<p>${data}</p>`;
            }
        }
    } catch (error) {
        console.error("Error:", error);
        alert("התרחשה שגיאה בטעינת הנתונים");
    }
}