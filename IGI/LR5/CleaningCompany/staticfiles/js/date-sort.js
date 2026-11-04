document.addEventListener('DOMContentLoaded', () => {
    let datesArray = [];

    class BaseDate {
        constructor(month, day) {
            this.month = month;
            this.day = day;
        }
        getMonth() { return this.month; }
        setMonth(m) { this.month = m; }
        getDay() { return this.day; }
        setDay(d) { this.day = d; }

        addFromForm(month, day, year) {
            this.month = month;
            this.day = day;
        }

        static displayAll(arr, containerId) {
            const container = document.getElementById(containerId);
            if (arr.length === 0) { 
                container.innerText = "Empty array."; 
                return;
            }
            container.innerHTML = arr.map((obj, i) => 
                `${i + 1}. ${obj.month} ${obj.day}${obj.year ? ', ' + obj.year : ''}`
            ).join('\n');
        }

        static displayResult(arr, containerId, season) {
            const container = document.getElementById(containerId);
            const filtered = arr.filter(obj => obj.getSeason() === season);
            container.innerText = filtered.length > 0 
                ? filtered.map(obj => `${obj.month} ${obj.day}, ${obj.year}`).join('\n')
                : "No dates found.";
            return filtered;
        }

        getSeason() {
            const summer = ['June', 'July', 'August'];
            const winter = ['December', 'January', 'February'];
            if (summer.includes(this.month)) return 'Summer';
            if (winter.includes(this.month)) return 'Winter';
            return 'Other';
        }
    }

    class DetailedDate extends BaseDate {
        constructor(month, day, year) {
            super(month, day);
            this.year = year; 
        }
    }

    function BaseDateProto(month, day) {
        this.month = month;
        this.day = day;
    }

    BaseDateProto.prototype.getMonth = function() { return this.month; };
    BaseDateProto.prototype.setMonth = function(m) { this.month = m; };
    BaseDateProto.prototype.getDay = function() { return this.day; };
    BaseDateProto.prototype.setDay = function(d) { this.day = d; };

    BaseDateProto.prototype.addFromForm = function(month, day, year) {
        this.month = month;
        this.day = day;
    };

    BaseDateProto.prototype.displayAll = function(arr, containerId) {
        const container = document.getElementById(containerId);
        if (arr.length === 0) { 
            container.innerText = "Empty array."; 
            return; 
        }
        container.innerHTML = arr.map((obj, i) => 
            `${i + 1}. ${obj.month} ${obj.day}${obj.year ? ', ' + obj.year : ''}`
        ).join('\n');
    };

    BaseDateProto.prototype.displayResult = function(arr, containerId, season) {
        const container = document.getElementById(containerId);
        const filtered = arr.filter(obj => obj.getSeason() === season);
        container.innerText = filtered.length > 0 
            ? filtered.map(obj => `${obj.month} ${obj.day}`).join('\n')
            : "No dates found.";
        return filtered;
    };

    BaseDateProto.prototype.getSeason = function() {
        const summer = ['June', 'July', 'August'];
        const winter = ['December', 'January', 'February'];
        if (summer.includes(this.month)) return 'Summer';
        if (winter.includes(this.month)) return 'Winter';
        return 'Other';
    };

    function DetailedDateProto(month, day, year) {
        BaseDateProto.call(this, month, day);
        this.year = year;
    }
    DetailedDateProto.prototype = Object.create(BaseDateProto.prototype);
    DetailedDateProto.prototype.constructor = DetailedDateProto;

    const form = document.getElementById('date-form');
    const showAllBtn = document.getElementById('show-all-btn');
    const sortBtn = document.getElementById('sort-btn');

    const monthInput = document.getElementById('month-input');
    const dayInput = document.getElementById('day-input');
    const yearInput = document.getElementById('year-input');

    const updateMaxDays = () => {
        const monthStr = monthInput.value;
        const year = parseInt(yearInput.value) || 2000; 
        
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const monthIndex = monthNames.indexOf(monthStr);

        if (monthIndex !== -1) {
            const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();
            dayInput.max = daysInMonth;
        }
    };

    monthInput.addEventListener('change', updateMaxDays);
    yearInput.addEventListener('input', updateMaxDays);

    const getImpl = () => document.querySelector('input[name="impl-type"]:checked').value;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const month = document.getElementById('month-input').value;
        const day = parseInt(document.getElementById('day-input').value);
        const year = parseInt(document.getElementById('year-input').value);

        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const monthIndex = monthNames.indexOf(month);
        const maxDays = new Date(year, monthIndex + 1, 0).getDate();

        if (day > maxDays) {
            alert(`Invalid date! ${month} ${year} only has ${maxDays} days.`);
            return; 
        }

        let newDate;
        if (getImpl() === 'class') {
            newDate = new DetailedDate(month, day, year);
        } else {
            newDate = new DetailedDateProto(month, day, year);
        }

        datesArray.push(newDate);
        form.reset();
        showAllBtn.click(); 
    });

    showAllBtn.addEventListener('click', () => {
        if (datesArray.length === 0) {
            document.getElementById('all-dates-output').innerText = "Empty array.";
            return;
        }

        if (getImpl() === 'class') {
            DetailedDate.displayAll(datesArray, 'all-dates-output');
        } else {
            BaseDateProto.prototype.displayAll(datesArray, 'all-dates-output');
        }
    });

    sortBtn.addEventListener('click', () => {
        if (datesArray.length === 0) {
            alert("Please add some dates first");
            return;
        }

        let summerDates, winterDates;

        if (getImpl() === 'class') {
            summerDates = DetailedDate.displayResult(datesArray, 'summer-output', 'Summer');
            winterDates = DetailedDate.displayResult(datesArray, 'winter-output', 'Winter');
        } else {
            summerDates = BaseDateProto.prototype.displayResult(datesArray, 'summer-output', 'Summer');
            winterDates = BaseDateProto.prototype.displayResult(datesArray, 'winter-output', 'Winter');
        }

        downloadFile('summer.txt', summerDates.map(d => `${d.month} ${d.day}, ${d.year}`).join('\n'));
        downloadFile('winter.txt', winterDates.map(d => `${d.month} ${d.day}, ${d.year}`).join('\n'));

        alert("Sorted. The files 'summer.txt' and 'winter.txt' have been downloaded.");
    });

    function downloadFile(filename, text) {
        if (!text) text = "No dates in this season.";
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
});