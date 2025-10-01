function initializeCountdown(options) {
    const { codeLifetimeSeconds, createdAtTimestamp } = options;
    const countdownElement = document.getElementById('countdown');
    const submitButton = document.querySelector('button[type="submit"]'); // Получаем кнопку подтверждения кода

    if (!countdownElement) {
        console.error("Элемент с идентификатором обратный отсчет не найден.");
        return;
    }

    function updateCountdown() {
        if (createdAtTimestamp === null || createdAtTimestamp === undefined) {
            countdownElement.textContent = "Не удалось получить время";
            return;
        }

        const nowTimestamp = Math.floor(Date.now() / 1000);
        const expiryTimestamp = createdAtTimestamp + codeLifetimeSeconds;
        let timeLeft = expiryTimestamp - nowTimestamp;

        if (timeLeft < 0) {
            timeLeft = 0;
        }

        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;

        const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        countdownElement.textContent = formattedTime;

        if (timeLeft === 0) {
            countdownElement.textContent = "Время истекло";
            if (submitButton) {
                submitButton.disabled = true; // Отключаем кнопку подтверждения кода
            }
            alert("Время для ввода кода истекло. Пожалуйста, запросите новый код.");

            // Автоматический запрос нового кода !!!
            const newCodeRequestForm = document.getElementById('requestNewCodeForm'); // Предполагаем, что у формы запроса нового кода есть id="requestNewCodeForm"
            if (newCodeRequestForm) {
                newCodeRequestForm.submit(); // Отправляем форму запроса нового кода
            } else {
                console.error("Form with ID 'requestNewCodeForm' not found. Cannot automatically request new code.");
                // Можно добавить перенаправление на другую страницу, если форма не найдена
            }
        } else {
            setTimeout(updateCountdown, 1000);
        }
    }

    updateCountdown();
}
