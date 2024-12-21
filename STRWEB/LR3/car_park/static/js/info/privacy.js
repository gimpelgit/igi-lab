document.addEventListener('DOMContentLoaded', function() {
    const toggleSettings = document.getElementById('toggleSettings');
    const settingsDiv = document.getElementById('settings');
    const fontSizeSelect = document.getElementById('fontSize');
    const textColorInput = document.getElementById('textColor');
    const bgColorInput = document.getElementById('bgColor');

    let html = document.documentElement;

    // Показать/скрыть настройки
    toggleSettings.addEventListener('change', function() {
        settingsDiv.style.display = toggleSettings.checked ? 'block' : 'none';
    });

    // Изменение размера шрифта
    fontSizeSelect.addEventListener('change', function() {
        html.style.fontSize = fontSizeSelect.value;
    });

    // Изменение цвета текста
    textColorInput.addEventListener('input', function() {
        document.body.style.color = textColorInput.value;
    });

    // Изменение цвета фона
    bgColorInput.addEventListener('input', function() {
        document.body.style.backgroundColor = bgColorInput.value;
    });
});