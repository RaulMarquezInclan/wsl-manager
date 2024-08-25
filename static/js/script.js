$(document).ready(function() {
    // Enable/Disable action buttons based on selection
    $('.instance-radio').on('change', function() {
        var selectedInstance = $('.instance-radio:checked');
        if (selectedInstance.length > 0) {
            $('#deleteBtn').prop('disabled', false);
            $('#cloneBtn').prop('disabled', false);
        } else {
            $('#deleteBtn').prop('disabled', true);
            $('#cloneBtn').prop('disabled', true);
        }
    });

    $('.distribution-radio').on('change', function() {
        $('#installBtn').prop('disabled', false);
    });

    // Handle Clone Action
    $('#cloneBtn').click(function() {
        var selectedInstance = $('.instance-radio:checked').data('instance');
        $('#newInstanceName').val(selectedInstance); // Pre-populate the name
        $('#nameError').hide(); // Reset error message visibility
        $('#confirmationModal').modal('show');

        $('#confirmActionBtn').off('click').on('click', function() {
            var newInstanceName = $('#newInstanceName').val().trim();

            if (newInstanceName === '') {
                $('#nameError').text('Instance name cannot be empty.').show();
                return;
            }

            // Check if the instance name already exists
            $.get('/check-instance-name', { instance_name: newInstanceName }, function(response) {
                if (response.exists) {
                    $('#nameError').text('An instance with this name already exists. Please choose a different name.').show();
                } else {
                    // Proceed with cloning
                    $.ajax({
                        url: '/clone',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ 
                            original_instance: selectedInstance, 
                            new_instance_name: newInstanceName 
                        }),
                        success: function(response) {
                            if (response.status === 'success') {
                                $('#confirmationModal').modal('hide'); // Close the modal
                                location.reload(); // Reload the page to refresh the list
                            } else {
                                $('#nameError').text('Cloning failed: ' + response.message).show();
                            }
                        },
                        error: function(xhr) {
                            $('#nameError').text('An error occurred: ' + xhr.responseText).show();
                        }
                    });
                }
            });
        });
    });

    // Handle Delete Action
    $('#deleteBtn').click(function() {
        $('#confirmationModal').modal('show');
        $('#confirmActionBtn').off('click').on('click', function() {
            var selectedInstance = $('.instance-radio:checked').data('instance');
            $.ajax({
                url: '/delete',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ instances: [selectedInstance] }),
                success: function(response) {
                    $('#confirmationModal').modal('hide'); // Close the modal
                    location.reload(); // Reload the page to refresh the list
                }
            });
        });
    });

    // Handle Install Action
    $('#installBtn').click(function() {
        var selectedDistribution = $('.distribution-radio:checked').data('distribution');
        $.ajax({
            url: '/install',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ distribution: selectedDistribution }),
            success: function(response) {
                alert('Installation started');
            }
        });
    });

    // Enable the install button when a distribution is selected
    $('input[name="distribution"]').change(function() {
        $('#installBtn').prop('disabled', false);
    });

    function refreshInstancesList() {
        $.get("/fetch-wsl-instances", function(data) {
            // Update the instances list in Section 1 with the new data
            $("#instances-list").html(data);
        });
    }
});
