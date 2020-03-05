$(function() {


$("#search-normal-text").focus();
$("#search-field").focus();


$('#checkbox-all-languages').click(function(event) {
        if(this.checked) {
            // Iterate each checkbox
            $(':checkbox').each(function() {
                if (this.name == 'language') {
                    this.checked = true;
                }

            });
        }
    });

$('#checkbox-all-categories').click(function(event) {
    if(this.checked) {
        // Iterate each checkbox
        $(':checkbox').each(function() {
            if (this.name == 'category') {
                this.checked = true;
            }

        });
    }
});



});