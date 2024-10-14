// Update the label text with selected file names and count
$('.custom-file-input').on('change', function() {
    let files = this.files;
    let filenames = Array.from(files).map(file => file.name);
    $(this).next('.custom-file-label').text(filenames.join(', '));
    
    let fileCount = files.length;
    $(this).siblings('.file-count').text("Number of files: " + fileCount);
});