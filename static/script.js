function confirmDelete() {
    return confirm(
        "Are you sure you want to delete this student? This action cannot be undone."
    );
}


function validateStudentForm(form) {
    const phone = form.querySelector("[name='phone']").value.trim();
    const year = form.querySelector("[name='year']").value;

    if (!/^\d{10}$/.test(phone)) {
        alert("Phone number must contain exactly 10 digits.");
        return false;
    }

    if (!["1", "2", "3", "4"].includes(year)) {
        alert("Please select a valid year.");
        return false;
    }

    return true;
}


setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        const closeButton = alert.querySelector(".btn-close");

        if (closeButton) {
            closeButton.click();
        }
    });
}, 5000);