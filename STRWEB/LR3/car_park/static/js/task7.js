// function Person(lastName, initials) {
//     this.lastName = lastName;
//     this.initials = initials;
// }

// Person.prototype.getLastName = function () {
//     return this.lastName;
// };
// Person.prototype.setLastName = function (lastName) {
//     this.lastName = lastName;
// };
// Person.prototype.getInitials = function () {
//     return this.initials;
// };
// Person.prototype.setInitials = function (initials) {
//     this.initials = initials;
// };

// Employee.prototype = Object.create(Person.prototype);
// Employee.prototype.constructor = Employee;

// function Employee(lastName, initials, phoneNumber) {
//     Person.call(this, lastName, initials); 
//     this.phoneNumber = phoneNumber;
// }

// Employee.prototype.getPhoneNumber = function () {
//     return this.phoneNumber;
// };


// Employee.prototype.setPhoneNumber = function (phoneNumber) {
//     this.phoneNumber = phoneNumber;
// };


// function EmployeeManager() {
//     this.employees = [
//         new Employee('Гимпель', 'K. A.', '+375-33-888-66-55'),
//         new Employee('Иванов', 'И. И.', '+375-29-111-22-33'),
//         new Employee('Петров', 'П. П.', '+375-25-222-33-44'),
//         new Employee('Сидоров', 'С. С.', '+375-44-333-44-55'),
//         new Employee('Козлов', 'К. К.', '+375-33-444-55-66'),
//         new Employee('Морозов', 'М. М.', '+375-29-555-66-77'),
//     ];
//     this.displayEmployees();
// }


// EmployeeManager.prototype.addEmployee = function (employee) {
//     this.employees.push(employee);
//     this.displayEmployees();
// };

// EmployeeManager.prototype.findEmployee = function (lastName, initials) {
//     const result = this.employees.find(
//         emp => emp.getLastName() === lastName.trim() && 
//         emp.getInitials() === initials.trim());
//     this.displayResult(result);
// };

// EmployeeManager.prototype.displayEmployees = function () {
//     const employeeListDiv = document.getElementById('employeeList');
//     employeeListDiv.innerHTML = '<h3>Список сотрудников:</h3>';
//     this.employees.forEach(emp => {
//         const empDiv = document.createElement('div');
//         empDiv.textContent = `${emp.getLastName()} ${emp.getInitials()} ${emp.getPhoneNumber()}`;
//         employeeListDiv.appendChild(empDiv);
//     });
// };

// EmployeeManager.prototype.displayResult = function (result) {
//     const resultDiv = document.getElementById('result');
//     if (result) {
//         resultDiv.textContent = `Телефон сотрудника: ${result.getPhoneNumber()}`;
//     } else {
//         resultDiv.textContent = 'Сотрудник не найден.';
//     }
// };


////////////// Второй вариант
class Person {
    constructor(lastName, initials) {
        this.lastName = lastName;
        this.initials = initials;
    }

    getLastName() {
        return this.lastName;
    }

    setLastName(lastName) {
        this.lastName = lastName;
    }

    getInitials() {
        return this.initials;
    }

    setInitials(initials) {
        this.initials = initials;
    }
}


class Employee extends Person {
    constructor(lastName, initials, phoneNumber) {
        super(lastName, initials);
        this.phoneNumber = phoneNumber;
    }

    getPhoneNumber() {
        return this.phoneNumber;
    }

    setPhoneNumber(phoneNumber) {
        this.phoneNumber = phoneNumber;
    }
}


class EmployeeManager {
    constructor() {
        this.employees = [
            new Employee('Гимпель', 'K. A.', '+375-33-888-66-55'),
            new Employee('Иванов', 'И. И.', '+375-29-111-22-33'),
            new Employee('Петров', 'П. П.', '+375-25-222-33-44'),
            new Employee('Сидоров', 'С. С.', '+375-44-333-44-55'),
            new Employee('Козлов', 'К. К.', '+375-33-444-55-66'),
            new Employee('Морозов', 'М. М.', '+375-29-555-66-77'),
        ];
        this.displayEmployees();
    }

    addEmployee(employee) {
        this.employees.push(employee);
        this.displayEmployees();
    }

    findEmployee(lastName, initials) {
        const result = this.employees.find(
            emp => emp.getLastName() === lastName.trim() &&
            emp.getInitials() === initials.trim());
        this.displayResult(result);
    }

    displayEmployees() {
        const employeeListDiv = document.getElementById('employeeList');
        employeeListDiv.innerHTML = '<h3>Список сотрудников:</h3>';
        this.employees.forEach(emp => {
            const empDiv = document.createElement('div');
            empDiv.textContent = `${emp.getLastName()} ${emp.getInitials()} ${emp.getPhoneNumber()}`;
            employeeListDiv.appendChild(empDiv);
        });
    }

    displayResult(result) {
        const resultDiv = document.getElementById('result');
        if (result) {
            resultDiv.textContent = `Телефон сотрудника: ${result.getPhoneNumber()}`;
        } else {
            resultDiv.textContent = 'Сотрудник не найден.';
        }
    }
}


const employeeManager = new EmployeeManager();

document.getElementById('addEmployeeForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const lastName = document.getElementById('lastName').value;
    const initials = document.getElementById('initials').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const employee = new Employee(lastName, initials, phoneNumber);
    employeeManager.addEmployee(employee);
});

document.getElementById('findEmployeeForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const searchLastName = document.getElementById('searchLastName').value;
    const searchInitials = document.getElementById('searchInitials').value;
    employeeManager.findEmployee(searchLastName, searchInitials);
});



document.getElementById('phoneNumber').addEventListener('input', function (event) {
    const input = event.target;
    let value = input.value;
    let firstSymbol = '';

    if (value.length === 1) {
        firstSymbol = value.replace(/\D/, '');
    }

    if (!value.startsWith('+375-')) {
        input.value = '+375-' + firstSymbol;
        return;
    }
    
    let digits = value.replace(/\D/g, ''); 
    if (digits.startsWith('375')) {
        digits = digits.slice(3); 
    }

    let formatted = '+375-';
    if (digits.length > 0) formatted += digits.slice(0, 2);
    if (digits.length > 2) formatted += '-' + digits.slice(2, 5); 
    if (digits.length > 5) formatted += '-' + digits.slice(5, 7); 
    if (digits.length > 7) formatted += '-' + digits.slice(7, 9); 

    if (value.endsWith('-') && value.length < formatted.length) {
        formatted = formatted.slice(0, -1);
    }

    value = formatted;
});
