$(document).ready(function() {
    // Open the modal when the Create Folder button is clicked
    $('#createFolderButton').click(function() {
      $('#createFolderModal').modal('show');
    });

    // Fill the input field with a default value
    $('#createFolderModal').on('shown.bs.modal', function() {
      $('#id_folder_name').val('');
    });

    // Submit the form when the Create button is clicked
    $('#createFolderForm').submit(function(event) {
      event.preventDefault(); // Prevent the default form submission

      // Get the form data
      var formData = $(this).serialize();

      // Send an AJAX request to the server
      $.ajax({
        url: "{% url 'create_folder' %}",
        type: "POST",
        data: formData,
        success: function(response) {
          // Reset the form
          $('#createFolderForm')[0].reset();
        },
        error: function(xhr, status, error) {
          // Handle the error
          console.log(error);
        }
      });
    });
  });