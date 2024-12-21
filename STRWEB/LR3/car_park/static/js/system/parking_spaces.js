const cardWrappers = document.querySelectorAll(".card-wrapper");

cardWrappers.forEach(wrapper => {
    wrapper.addEventListener('mousemove', event => {
        const rect = wrapper.getBoundingClientRect();
        const [x, y] = [event.offsetX, event.offsetY];
        const [width, height] = [rect.width, rect.height];
        const middleX = width / 2;
        const middleY = height / 2;
        const offsetX = ((x - middleX) / middleX) * 25;
        const offsetY = ((y - middleY) / middleY) * 25;

        wrapper.style.setProperty("--rotateX", 1 * offsetX + "deg");
        wrapper.style.setProperty("--rotateY", -1 * offsetY + "deg");
    });
});