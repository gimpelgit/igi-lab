document.querySelector('form.styled-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const dateOfBirthInput = document.getElementById('id_date_of_birth');
    const dateOfBirth = new Date(dateOfBirthInput.value);

    if (isNaN(dateOfBirth.getTime())) {
        alert('Пожалуйста, введите корректную дату рождения.');
        return;
    }
    
    const today = new Date();
    age = today.getFullYear() - dateOfBirth.getFullYear();
    const monthDifference = today.getMonth() - dateOfBirth.getMonth();
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dateOfBirth.getDate())) {
        age--;
    }

    const daysOfWeek = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    const dayOfWeek = daysOfWeek[dateOfBirth.getDay()];

    if (age >= 18) {
        alert(`Вы родились в ${dayOfWeek}. Ваш возраст: ${age} лет. Добро пожаловать на сайт!`);
        this.submit();
    } else {
        alert(`Вы родились в ${dayOfWeek}. Ваш возраст: ${age} лет.` +  
            "Для использования нашего сайта необходимо быть старше 18 лет или иметь разрешение" + 
            "от родителей или законных представителей.");
    }
});