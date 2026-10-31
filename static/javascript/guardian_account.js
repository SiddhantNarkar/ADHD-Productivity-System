document.addEventListener("DOMContentLoaded", function () {

    // MAIN Guardian Image Preview
    const mainInput = document.getElementById("guardianProfileImageInput");
    const mainPreview = document.getElementById("guardianProfilePreview");

    if (mainInput) {
        mainInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                mainPreview.src = URL.createObjectURL(file);
            }
        });
    }

    // ---------- MULTIPLE SUB-GUARDIANS (WITH UNIQUE IDs) ----------
    let subGuardianCounter = 0;   // total sub-guardians added
    const MAX_SUB_GUARDIANS = 2;  // limit allowed

    window.addSubGuardian = function () {

        // STOP if limit reached
        if (subGuardianCounter >= MAX_SUB_GUARDIANS) {
            alert("You can add only 2 Sub-Guardians.");
            return;
        }

        subGuardianCounter++; // increase count

        const container = document.getElementById("guardianSubContainer");
        let template = document.getElementById("guardianSubTemplate").innerHTML;

        // Create unique IDs for preview + input
        const previewId = "subguardianProfilePreview_" + subGuardianCounter;
        const inputId = "subguardianProfileImageInput_" + subGuardianCounter;

        // Replace placeholders
        template = template.replace(/sub_preview_ID/g, previewId);
        template = template.replace(/sub_input_ID/g, inputId);

        // Prepare DOM
        const wrapper = document.createElement("div");
        wrapper.innerHTML = template;
        wrapper.classList.add("subguardian-wrapper");
        wrapper.style.animation = "fadeIn 0.3s ease-in-out";
        container.appendChild(wrapper);

        // Add event listener for this new image input
        const newInput = document.getElementById(inputId);
        const newPreview = document.getElementById(previewId);

        newInput.addEventListener("change", function () {
            const imgFile = this.files[0];
            if (imgFile) {
                newPreview.src = URL.createObjectURL(imgFile);
            }
        });

        // Enable removing a sub-guardian and updating count
        const removeBtn = wrapper.querySelector(".guardian-remove-sub-btn");
        removeBtn.addEventListener("click", function () {
            wrapper.remove();
            subGuardianCounter--;  // decrease count when removed
        });
    };

});
