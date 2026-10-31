const imageInput = document.getElementById('profileImageInput');
const previewImg = document.getElementById('profilePreview');

imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        previewImg.src = URL.createObjectURL(file);
    }
});