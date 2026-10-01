// --- Edit Summary Modal Functionality ---
const editModal = document.getElementById("edit-modal");
const editForm = document.getElementById("edit-summary-form");

function openEditModal(id, videoTitle, channelName, summaryText, sentiment) {
    document.getElementById("edit-summary-id").value = id;
    document.getElementById("edit-video-title").value = videoTitle || "";
    document.getElementById("edit-channel-name").value = channelName || "";
    document.getElementById("edit-summary-text").value = summaryText || "";
    document.getElementById("edit-sentiment").value = sentiment || "Neutral";

    if (editModal) {
        editModal.style.display = "flex";
    }
}

function closeEditModal() {
    if (editModal) {
        editModal.style.display = "none";
    }
    if (editForm) {
        editForm.reset();
    }
}

// Close modal when clicking the backdrop overlay (outside the modal box)
if (editModal) {
    editModal.addEventListener("click", function (e) {
        if (e.target === editModal) {
            closeEditModal();
        }
    });
}

// Close modal when pressing the Escape key
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && editModal && editModal.style.display === "flex") {
        closeEditModal();
    }
});