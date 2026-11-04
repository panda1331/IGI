document.addEventListener('DOMContentLoaded', () => {
    const ageCheckBtn = document.getElementById('age-check-btn');

    if (ageCheckBtn) {
        ageCheckBtn.addEventListener('click', () => {
            const dateString = prompt("Please enter your date of birth (format: YYYY-MM-DD):", "2000-01-01");

            if (!dateString) {
                return; 
            }

            const birthDate = new Date(dateString);
            const today = new Date();

            if (isNaN(birthDate.getTime())) {
                alert("Invalid date format. Please use YYYY-MM-DD.");
                return;
            }

            if (birthDate > today) {
                alert("Date of birth cannot be in the future");
                return;
            }

            let age = today.getFullYear() - birthDate.getFullYear();
            const m = today.getMonth() - birthDate.getMonth();
            
            if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }

            const daysOfWeek = [
                "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
            ];
            const dayOfWeekName = daysOfWeek[birthDate.getDay()];

            if (age >= 18) {
                alert(`You are of legal age (${age} years old).\nThe day of the week for your date of birth was: ${dayOfWeekName}.`);
            } else {
                alert(`You are ${age} years old. You are a minor.\nYou need parental permission to use this site.`);
            }
        });
    }
});