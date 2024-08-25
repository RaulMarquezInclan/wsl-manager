$(document).ready(function() {
    // Enable/Disable action buttons based on selection
    $('.instance-checkbox').on('change', function() {
        var selectedInstances = $('.instance-checkbox:checked');
        if (selectedInstances.length > 0) {
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

    // Handle Delete Action
    $('#deleteBtn').click(function() {
        $('#confirmationModal').modal('show');
        $('#confirmActionBtn').off('click').on('click', function() {
            var selectedInstances = $('.instance-checkbox:checked').map(function() {
                return $(this).data('instance');
            }).get();
            $.ajax({
                url: '/delete',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ instances: selectedInstances }),
                success: function(response) {
                    location.reload();
                }
            });
        });
    });

    // Handle Clone Action
    $('#cloneBtn').click(function() {
        $('#confirmationModal').modal('show');
        $('#confirmActionBtn').off('click').on('click', function() {
            var selectedInstances = $('.instance-checkbox:checked').map(function() {
                return $(this).data('instance');
            }).get();
            $.ajax({
                url: '/clone',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ instances: selectedInstances }),
                success: function(response) {
                    location.reload();
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
});
