let slideIndex = 1;
let slides = document.querySelectorAll('.slide');
let delay = 5;  
let autoChange = true; 
let intervalId;

document.addEventListener("DOMContentLoaded", function() {
    showSlides(slideIndex);
    if (autoChange) {
        startAutoChange();
    }
});


function showSlides(n) {
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    
    const sliderContainer = document.querySelector('.slider-container');
    sliderContainer.style.transform = 'translateX(' + (-(slideIndex - 1) * 100) + '%)';
    
    document.getElementById('slide-number').textContent = `${slideIndex} / ${slides.length}`;
    
    let dots = document.querySelectorAll('.dot');
    dots.forEach(dot => dot.classList.remove('active'));
    dots[slideIndex - 1].classList.add('active');
}


function changeSlide(n) {
    showSlides(slideIndex += n);
}


function currentSlide(n) {
    showSlides(slideIndex = n);
}


function startAutoChange() {
    intervalId = setInterval(function() {
        if (autoChange) {
            slideIndex++;
            showSlides(slideIndex);
        }
    }, delay * 1000);
}

function updateDelay() {
    delay = parseInt(document.getElementById('delay-input').value);
    clearInterval(intervalId); 
    startAutoChange();
}
