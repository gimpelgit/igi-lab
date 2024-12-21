const START_POSITION = -300; 
const END_POSITION = 10;
const HEIGHT_CAR = 90;     
const car = document.getElementById('main-car');

window.addEventListener('DOMContentLoaded', () => {
    car.style.left = `${START_POSITION}px`;
    car.style.height = `${HEIGHT_CAR}px`;
});

const parkingArea = document.querySelector('.parking-area');
const parkingAreaTop = parkingArea.offsetTop; 
const parkingAreaHeight = parkingArea.offsetHeight; 
const scrollHeight = (parkingAreaHeight - HEIGHT_CAR) / 2;

const totalDistance = END_POSITION - START_POSITION; 

window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY; 

    const scrollPercentage = Math.max(0, Math.min(1, (scrollPosition - parkingAreaTop + 120) / scrollHeight));

    const currentPosition = START_POSITION + (scrollPercentage * totalDistance);
    car.style.left = `${Math.min(END_POSITION, Math.max(START_POSITION, currentPosition))}px`;
});