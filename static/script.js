let selectedFiles = [];
let currentJobId = null;
let statusInterval = null;

// DOM elements
const videoForm = document.getElementById('video-form');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('images');
const previewContainer = document.getElementById('preview-container');
const statusSection = document.getElementById('status-section');
const resultSection = document.getElementById('result-section');
const errorSection = document.getElementById('error-section');
const progressBar = document.getElementById('progress-bar');
const statusMessage = document.getElementById('status-message');
const errorMessage = document.getElementById('error-message');
const downloadBtn = document.getElementById('download-btn');
const loadingSpinner = document.getElementById('loading-spinner');

// File drag and drop handlers
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragenter', handleDragEnter);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);

function handleDragOver(e) {
    e.preventDefault();
}

function handleDragEnter(e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    if (!dropZone.contains(e.relatedTarget)) {
        dropZone.classList.remove('dragover');
    }
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function addFiles(files) {
    // Lọc chỉ lấy file hình ảnh và tối đa 3 file
    const imageFiles = files.filter(file => file.type.startsWith('image/'));
    const remainingSlots = 3 - selectedFiles.length;
    const filesToAdd = imageFiles.slice(0, remainingSlots);
    
    if (filesToAdd.length === 0 && imageFiles.length > 0) {
        alert('Bạn chỉ có thể chọn tối đa 3 hình ảnh!');
        return;
    }
    
    filesToAdd.forEach(file => {
        // Kiểm tra kích thước file (16MB)
        if (file.size > 16 * 1024 * 1024) {
            alert(`File ${file.name} quá lớn! Tối đa 16MB.`);
            return;
        }
        
        selectedFiles.push(file);
        addPreviewImage(file);
    });
    
    updateDropZoneText();
}

function addPreviewImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'preview-image';
        img.alt = file.name;
        
        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '×';
        removeBtn.className = 'remove-image';
        removeBtn.onclick = () => removeImage(file, previewItem);
        
        previewItem.appendChild(img);
        previewItem.appendChild(removeBtn);
        previewContainer.appendChild(previewItem);
    };
    reader.readAsDataURL(file);
}

function removeImage(file, previewElement) {
    selectedFiles = selectedFiles.filter(f => f !== file);
    previewElement.remove();
    updateDropZoneText();
}

function updateDropZoneText() {
    const remainingSlots = 3 - selectedFiles.length;
    if (remainingSlots === 0) {
        dropZone.style.display = 'none';
    } else {
        dropZone.style.display = 'block';
        const pluralText = remainingSlots === 1 ? 'hình' : 'hình';
        dropZone.querySelector('p').textContent = `Còn có thể chọn thêm ${remainingSlots} ${pluralText}`;
    }
}

// Form submission
videoForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const textContent = document.getElementById('text').value.trim();
    if (!textContent) {
        alert('Vui lòng nhập nội dung text!');
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append('text', textContent);
    
    const voiceSelect = document.getElementById('voice');
    if (voiceSelect) {
        formData.append('voice', voiceSelect.value);
    }
    
    selectedFiles.forEach((file, index) => {
        formData.append('images', file);
    });
    
    // Show loading state
    const submitBtn = videoForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    loadingSpinner.style.display = 'inline-block';
    
    try {
        const response = await fetch('/create_video', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            currentJobId = result.job_id;
            showStatusSection();
            hideFormSection();
            startStatusPolling();
        } else {
            throw new Error(result.error || 'Có lỗi xảy ra khi tạo video');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
});

function showStatusSection() {
    statusSection.style.display = 'block';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressBar.style.width = '0%';
    statusMessage.textContent = 'Đang xử lý...';
}

function hideFormSection() {
    videoForm.style.display = 'none';
}

function showFormSection() {
    videoForm.style.display = 'block';
}

function startStatusPolling() {
    if (statusInterval) {
        clearInterval(statusInterval);
    }
    
    statusInterval = setInterval(async () => {
        if (!currentJobId) return;
        
        try {
            const response = await fetch(`/job_status/${currentJobId}`);
            const status = await response.json();
            
            if (response.ok) {
                updateProgress(status);
                
                if (status.status === 'completed') {
                    showSuccess(status.result);
                    clearInterval(statusInterval);
                } else if (status.status === 'error') {
                    showError(status.error || 'Có lỗi xảy ra');
                    clearInterval(statusInterval);
                }
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }, 2000); // Check every 2 seconds
}

function updateProgress(status) {
    const progress = status.progress || 0;
    progressBar.style.width = `${progress}%`;
    statusMessage.textContent = status.message || 'Đang xử lý...';
}

function showSuccess(filename) {
    resultSection.style.display = 'block';
    downloadBtn.href = `/download/${filename}`;
    downloadBtn.onclick = () => {
        // Clean up after download
        setTimeout(() => {
            if (currentJobId) {
                fetch(`/cleanup/${currentJobId}`);
            }
        }, 1000);
    };
}

function showError(message) {
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
}

function resetForm() {
    // Clear form
    document.getElementById('text').value = '';
    selectedFiles = [];
    previewContainer.innerHTML = '';
    currentJobId = null;
    
    // Reset file input
    fileInput.value = '';
    
    // Reset voice selection
    const voiceSelect = document.getElementById('voice');
    if (voiceSelect) {
        voiceSelect.value = 'vi-VN-Neural2-A';
    }
    
    // Clear intervals
    if (statusInterval) {
        clearInterval(statusInterval);
        statusInterval = null;
    }
    
    // Hide status sections
    statusSection.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Show form
    showFormSection();
    updateDropZoneText();
    
    // Reset progress
    progressBar.style.width = '0%';
    statusMessage.textContent = 'Đang xử lý...';
}

// Initialize
updateDropZoneText();