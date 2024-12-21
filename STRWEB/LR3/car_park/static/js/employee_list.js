let currentPage = 1;
let sortBy = 'user';
let searchQuery = '';

// Функция для загрузки данных сотрудников
function loadEmployees() {
    const url = `/table-contacts/?page=${currentPage}&sort_by=${sortBy}&search=${searchQuery}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#employee-table tbody');
            tableBody.innerHTML = '';  // Очистка текущей таблицы
            

            // Заполнение таблицы
            data.employees.forEach(employee => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${employee.name}</td>
                    <td>${employee.phone_number}</td>
                    <td>${employee.email}</td>
                    <td><button onclick="showEmployeeDetails(${employee.id})">Посмотреть</button></td>
                    <td><input type="checkbox" class="employee-checkbox" value="${employee.id}"></td>
                `;
                tableBody.appendChild(row);
            });

            // Обновляем пагинацию
            const pagination = document.querySelector('#pagination');
            pagination.innerHTML = `
                <button ${!data.has_previous ? 'disabled' : ''} onclick="changePage(1)">Первая</button>
                <button ${!data.has_previous ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">Предыдущая</button>
                <span>Страница ${data.page_number} из ${data.num_pages}</span>
                <button ${!data.has_next ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">Следующая</button>
                <button ${!data.has_next ? 'disabled' : ''} onclick="changePage(${data.num_pages})">Последняя</button>
            `;
        });
}

// Функция для изменения страницы
function changePage(page) {
    currentPage = page;
    loadEmployees();
}

// Функция сортировки по колонке
function changeSort(by) {
    if (sortBy === by) {
        sortBy = `-${by}`;  // Обратный порядок
    } else {
        sortBy = by;
    }
    loadEmployees();
}

// Функция для поиска
document.querySelector('#search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    searchQuery = document.querySelector('#search-input').value;
    loadEmployees();
});

// Функции сортировки по столбцам
document.querySelector('#sort-name').addEventListener('click', () => changeSort('user'));
document.querySelector('#sort-phone').addEventListener('click', () => changeSort('phone_number'));
document.querySelector('#sort-email').addEventListener('click', () => changeSort('user__email'));

// Выбор всех чекбоксов
function selectAllCheckboxes() {
    const checkboxes = document.querySelectorAll('.employee-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = document.querySelector('#select-all').checked;
    });
}

// Показать подробности сотрудника
function showEmployeeDetails(id) {
    fetch(`/contact-details/${id}`)
        .then(response => response.json())
        .then(data => {
            const detailsBlock = document.querySelector('#employee-details');
            detailsBlock.innerHTML = `
                <div class="employee-card">
                    <img class="employee-img" src="${data.image_url}" alt="Здесь должно быть изображение">
                    <div class="employee-info">
                        <h3>${data.vacancy_name}</h3>
                        <p><b>Имя:</b> ${data.name}</p>
                        <p><b>Телефон:</b> ${data.phone_number}</p>
                        <p><b>Почта:</b> ${data.email}</p>
                    </div>
                </div>
            `;
        });
}

const employeeForm = document.getElementById('employee-form');
const addEmployeeForm = document.getElementById('add-employee-form');

function hideForm() {
    addEmployeeForm.style.display = 'none';
}

document.getElementById('add-employee-button').addEventListener('click', e => {
    addEmployeeForm.style.display = 'block';
});

employeeForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const firstName = document.getElementById('first_name').value.trim();
    const lastName = document.getElementById('last_name').value.trim();
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const phoneNumber = document.getElementById('phone_number').value.trim();
    const salary = document.getElementById('salary').value.trim();
    const dateOfBirth = document.getElementById('date_of_birth').value.trim();
    const vacancy = document.getElementById('vacancy').value.trim();

    // Валидация данных
    let isValid = true;
    const validationMessage = document.getElementById('validation-message');
    validationMessage.textContent = '';

    if (!firstName) {
        validationMessage.textContent += 'Имя обязательно для заполнения. ';
        isValid = false;
    }

    if (!lastName) {
        validationMessage.textContent += 'Фамилия обязательна для заполнения. ';
        isValid = false;
    }

    if (!username) {
        validationMessage.textContent += 'Имя пользователя обязательно для заполнения. ';
        isValid = false;
    }

    if (!email) {
        validationMessage.textContent += 'Email обязателен для заполнения. ';
        isValid = false;
    } else if (!validateEmail(email)) {
        validationMessage.textContent += 'Некорректный email. ';
        isValid = false;
    }

    if (!password) {
        validationMessage.textContent += 'Пароль обязателен для заполнения. ';
        isValid = false;
    } else if (password.length < 8) {
        validationMessage.textContent += 'Пароль должен быть не менее 8 символов. ';
        isValid = false;
    }

    if (!phoneNumber) {
        validationMessage.textContent += 'Телефон обязателен для заполнения. ';
        isValid = false;
    } else if (!validatePhoneNumber(phoneNumber)) {
        validationMessage.textContent += 'Некорректный номер телефона. ';
        isValid = false;
    }

    if (!salary) {
        validationMessage.textContent += 'Зарплата обязательна для заполнения. ';
        isValid = false;
    }

    if (!dateOfBirth) {
        validationMessage.textContent += 'Дата рождения обязательна для заполнения. ';
        isValid = false;
    }

    if (!vacancy) {
        validationMessage.textContent += 'Вакансия обязательна для заполнения. ';
        isValid = false;
    }

    // Если валидация не пройдена, останавливаем отправку
    if (!isValid) {
        return;
    }

    const csrfToken = getCookie('csrftoken');
    const formData = new FormData(this);
    fetch('/add-employee/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Сотрудник успешно добавлен!');
            hideForm();
            loadEmployees();  // Обновляем таблицу
        } else {
            document.getElementById('validation-message').textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('validation-message').textContent = 'Произошла ошибка при добавлении сотрудника.';
    });
});

// Загрузка данных сотрудников при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadEmployees();
});


function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function validatePhoneNumber(phone) {
    const phonePattern = /^\+?375\s*\(?\d{2}\)?\s*\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    return phonePattern.test(phone);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}