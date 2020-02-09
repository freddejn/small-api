
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

// document.getElementById('create-habit-form').addEventListener('submit', formSubmitted)

function formSubmitted(e) {
    e.preventDefault();
    console.log('running');
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

function setToday() {
    var d = new Date();
    var today = days[d.getDay()];
    var todayButtons = document.querySelectorAll('button.' + today);
    for (var x = 0; x < todayButtons.length; x++) {
        todayButtons[x].classList.toggle('current-day');
    }
}

function completeHabitButtonPressed(day, element) {
    var date = getDateFromDay(day);
    console.log(date);
    url = element.parentNode.parentNode.dataset.delete + date;
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

function getDateFromDay(day) {
    Date.prototype.addDays = function (daysToAdd) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + daysToAdd)
        return date
    }
    var todayAsNum = new Date().getDay();
    var todayAsNum = (todayAsNum == 0 ? 6 : todayAsNum - 1);
    console.log(todayAsNum);
    var selectedDayAsNum = days.indexOf(day);
    var daysToAdd = selectedDayAsNum - todayAsNum;
    var tNewDate = new Date();
    var newDate = tNewDate.addDays(daysToAdd);
    var dd = newDate.getDate();
    var mm = newDate.getMonth() + 1;
    var yy = newDate.getFullYear();
    if (mm < 10) {
        mm = '0' + mm;
    }
    if (dd < 10) {
        dd = '0' + dd;
    }
    var formattedDate = [yy, mm, dd].join('')
    return formattedDate;
}

$(document).ready(function () {
    initForm();
    setToday();
});
