var days = ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun',];

function deleteHabit(url) {
    return makeDeleteRequest(url, refreshHabitListAfterDelete);
}

function makeDeleteRequest(url, refreshHabitListAfterDelete) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            refreshHabitListAfterDelete(JSON.parse(xhttp.responseText));
        }
    };
    xhttp.open('DELETE', url);
    xhttp.send();
}

refreshHabitListAfterDelete = (response) => {
    document.getElementById(response['id']).remove()
};

function toggleCreateHabitForm() {
    var createHabitForm = document.getElementById('create-habit-form');
    createHabitForm.classList.toggle('visible');
    var toggleCreateHabitButton = document.getElementById('toggle-create-habit-button');
    toggleCreateHabitButton.classList.toggle('up');
    toggleCreateHabitButton.classList.toggle('down');
}

function formSubmitted(e) {
    e.preventDefault();
    var form = document.getElementById('create-habit-form');
    var data = new FormData(form);
    var url = data.get('url')
    data.set('keywords', [])
    data.delete('url')
    createHabit(url, JSON.stringify(Object.fromEntries(data)));
}

function createHabit(url, data) {
    return makeCreateRequest(url, data, refreshHabitListAfterCreate);
}

function makeCreateRequest(url, data, refreshHabitListAfterCreate) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            refreshHabitListAfterCreate(JSON.parse(xhttp.responseText));
        }
    };
    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(data);
}

refreshHabitListAfterCreate = (response) => {
    console.log(response);
    location.reload();
}

function initForm() {
    $('.ui.form').form({
        inline: true,
        fields: {
            keywords: {
                identifier: 'keywords',
                rules: [{
                    type: 'regExp',
                    value: /^([a-zA-Z]*(\,|\:|\;|$))+/i,
                    prompt: 'Please enter comma separated list of words.'
                }]
            },
            body: {
                identifier: 'body',
                rules: [{
                    type: 'maxLength[100]',
                    prompt: 'Habit body cannot be longer than {ruleValue} characters.'
                }]
            }
        },
        onSuccess: formSubmitted
    });
}

// TODO: Rewrite this to account for other weeks.
function setToday() {
    var startOfWeek = document.getElementById('previous-week').dataset.weekstart;
    var startDate = getDateFromStartWeek(startOfWeek);
    var endDate = addDaysToDate(startDate, 6);
    var d = new Date();
    if (startDate <= d && d <= endDate) {
        var todayInt = (d.getDay() == 0 ? 6: d.getDay() -1)
        var today = days[todayInt];
        var todayButtons = document.querySelectorAll('button.' + today);
        for (var i = 0; i < todayButtons.length; i++) {
            todayButtons[i].classList.toggle('current-day');
        }
    }
}

function completeHabitButtonPressed(element) {
    var indexOfPressed = element.dataset.day
    var startOfWeek = document.getElementById('previous-week').dataset.weekstart;
    var startOfWeekDate = getDateFromStartWeek(startOfWeek);
    var datePressed = addDaysToDate(startOfWeekDate, indexOfPressed - 1);
    datePressed = formatDate(datePressed);
    url = element.parentNode.parentNode.dataset.delete + datePressed;
    var sound = new Audio('/static/sounds/click.wav')
    sound.play();
    var buttonOn = element.classList.contains('positive')
    refreshCompletedHabitsListAfterUpdate(element);
    if (buttonOn) {
        deleteHabitRequest(url, element);
    } else {
        completeHabitRequest(url, element);
    }
}

function getDateFromStartWeek(startOfWeekDate) {
    var y = startOfWeekDate.substr(0, 4);
    var m = startOfWeekDate.substr(4, 2) - 1;
    var d = startOfWeekDate.substr(6, 2);
    var tDate = new Date(y, m, d);
    return tDate;
}

function addDaysToDate(date, dayNum) {
    Date.prototype.addDays = function (daysToAdd) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + daysToAdd)
        return date
    }
    return date.addDays(dayNum);
}

function formatDate(date) {
    var dd = date.getDate();
    var mm = date.getMonth() + 1;
    var yy = date.getFullYear();
    if (mm < 10) {
        mm = '0' + mm;
    }
    if (dd < 10) {
        dd = '0' + dd;
    }
    var formattedDate = [yy, mm, dd].join('')
    return formattedDate;
}

function completeHabitRequest(url, element) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', url);
    xhttp.send();
}

function deleteHabitRequest(url, element) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('DELETE', url);
    xhttp.send();
}

function refreshCompletedHabitsListAfterUpdate(element) {
    element.classList.toggle('positive');
}

function previousWeek() {
    var startOfWeek = document.getElementById('previous-week').dataset.weekstart;
    var startOfWeekDate = getDateFromStartWeek(startOfWeek);
    var date = addDaysToDate(startOfWeekDate, - 7);
    date = formatDate(date);
}

function nextWeek() {
    var startOfWeek = document.getElementById('previous-week').dataset.weekstart;
    var startOfWeekDate = getDateFromStartWeek(startOfWeek);
    var date = addDaysToDate(startOfWeekDate, + 7);
    date = formatDate(date);
}

function initUrlForToggleWeek() {
    var startOfWeek = document.getElementById('previous-week').dataset.weekstart;
    var startOfWeekDate = getDateFromStartWeek(startOfWeek);
    var previous = formatDate(addDaysToDate(startOfWeekDate, - 7));
    var next = formatDate(addDaysToDate(startOfWeekDate, + 7));
    var nextWeekUrl = document.getElementById('next-week-url').href;
    var previousWeekUrl = document.getElementById('previous-week-url').href;
    document.getElementById('next-week-url').href = nextWeekUrl + '/' + next;
    document.getElementById('previous-week-url').href = previousWeekUrl + '/' + previous;

}

$(document).ready(function () {
    initForm();
    setToday();
    initUrlForToggleWeek();
});
