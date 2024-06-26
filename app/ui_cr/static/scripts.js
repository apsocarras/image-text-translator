document.getElementById('image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('img-upload');
            img.src = e.target.result;
            img.style.display = 'block';

            // Update hidden input with base64 image data
            document.getElementById('img_data').value = e.target.result;

            // Enable the button if image is selected
            toggleButtonState();
        };
        reader.readAsDataURL(file);
    }
});

document.addEventListener('paste', function(event) {
    const items = (event.clipboardData || window.clipboardData).items;
    for (let index in items) {
        const item = items[index];
        if (item.kind === 'file' && item.type.startsWith('image/')) {
            const file = item.getAsFile();
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.getElementById('img-upload');
                img.src = e.target.result;
                img.style.display = 'block';

                // Update hidden input with base64 image data
                document.getElementById('img_data').value = e.target.result;

                // Enable the button if image is selected
                toggleButtonState();

                // Create a new FileList and set it to the file input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                document.getElementById('image').files = dataTransfer.files;
            };
            reader.readAsDataURL(file);
        }
    }
});

document.getElementById('to_lang').addEventListener('change', function() {
    const imgData = document.getElementById('img_data').value;
    if (imgData && imgData !== '#src-placeholder') {
        // Create a Blob from the base64 data
        const byteString = atob(imgData.split(',')[1]);
        const mimeString = imgData.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], { type: mimeString });

        // Create a new File object
        const file = new File([blob], "image.jpg", { type: mimeString });

        // Create a new FileList and set it to the file input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.getElementById('image').files = dataTransfer.files;
    }

    // Enable the button if language is changed
    toggleButtonState();
});

function toggleButtonState() {
    const imgData = document.getElementById('img_data').value;
    const currentLang = document.getElementById('to_lang').value;
    const initialLang = "{{ to_lang }}"; // Assuming this is the initial selected language

    if (imgData && imgData !== '#src-placeholder' && currentLang !== initialLang) {
        document.getElementById('translate-button').disabled = false;
    } else {
        document.getElementById('translate-button').disabled = true;
    }
}

// Initial button state check
toggleButtonState();
