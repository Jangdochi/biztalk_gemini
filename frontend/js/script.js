document.addEventListener('DOMContentLoaded', () => {
    const keywordsInput = document.getElementById('keywordsInput');
    const personaSelect = document.getElementById('personaSelect');
    const convertButton = document.getElementById('convertButton');
    const convertedMessageOutput = document.getElementById('convertedMessageOutput');
    const copyButton = document.getElementById('copyButton');
    const currentCharCount = document.getElementById('currentCharCount');
    const messageContainer = document.getElementById('messageContainer');

    // --- Utility Functions ---

    function showMessage(message, type) {
        messageContainer.textContent = message;
        
        // Reset classes
        messageContainer.classList.remove('bg-green-500', 'bg-red-500', 'opacity-0', 'translate-y-4');
        
        // Apply type-specific classes
        if (type === 'success') {
            messageContainer.classList.add('bg-green-500');
        } else if (type === 'error') {
            messageContainer.classList.add('bg-red-500');
        } else {
            messageContainer.classList.add('bg-gray-800');
        }

        // Show the message
        messageContainer.classList.remove('opacity-0', 'translate-y-4');
        messageContainer.classList.add('opacity-100', 'translate-y-0');

        // Hide after 3 seconds
        setTimeout(() => {
            messageContainer.classList.remove('opacity-100', 'translate-y-0');
            messageContainer.classList.add('opacity-0', 'translate-y-4');
        }, 3000);
    }

    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            showMessage('클립보드에 복사되었습니다!', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
            showMessage('복사 실패!', 'error');
        }
    }

    // --- Event Listeners ---

    keywordsInput.addEventListener('input', () => {
        const currentLength = keywordsInput.value.length;
        currentCharCount.textContent = currentLength;
    });

    convertButton.addEventListener('click', async () => {
        const keywords = keywordsInput.value.trim();
        const persona = personaSelect.value;

        if (!keywords) {
            showMessage('변환할 메시지를 입력해주세요.', 'error');
            return;
        }

        // Disable button and show loading state
        convertButton.disabled = true;
        convertButton.textContent = '변환 중...';
        convertedMessageOutput.value = '변환 중입니다...';
        copyButton.disabled = true;

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keywords, persona }),
            });

            const data = await response.json();

            if (response.ok) {
                convertedMessageOutput.value = data.converted_message;
                copyButton.disabled = false;
                showMessage('메시지 변환 완료!', 'success');
            } else {
                convertedMessageOutput.value = `오류: ${data.error || '알 수 없는 오류 발생'}`;
                showMessage(`오류: ${data.error || '알 수 없는 오류 발생'}`, 'error');
            }
        } catch (error) {
            console.error('API 호출 중 오류 발생:', error);
            convertedMessageOutput.value = 'API 호출 중 오류가 발생했습니다.';
            showMessage('API 호출 중 네트워크 오류 발생.', 'error');
        } finally {
            // Re-enable button
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
        }
    });

    copyButton.addEventListener('click', () => {
        copyToClipboard(convertedMessageOutput.value);
    });

    // Initial character count update
    keywordsInput.dispatchEvent(new Event('input'));
});