document.addEventListener("DOMContentLoaded", function() {
    const endTimeKey = 'endTime';
    let endTime = localStorage.getItem(endTimeKey);

    if (!endTime) {
        // Если времени нет в localStorage
        endTime = Date.now() + 60 * 60 * 1000; 
        localStorage.setItem(endTimeKey, endTime);
    }

    // Функция обновления обратного отсчета
    function updateCountdown() {
        const currentTime = Date.now();
        const timeLeft = endTime - currentTime;

        if (timeLeft <= 0) {
            document.getElementById('time-left').textContent = "00:00";
            localStorage.removeItem(endTimeKey);
        } else {
            const hours = Math.floor(timeLeft / (1000 * 60 * 60));
            const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            document.getElementById('time-left').textContent = 
                `${padTime(hours)}:${padTime(minutes)}:${padTime(seconds)}`;
        }
    }

    function padTime(time) {
        return time < 10 ? '0' + time : time;
    }

    setInterval(updateCountdown, 1000);

    updateCountdown();
});
