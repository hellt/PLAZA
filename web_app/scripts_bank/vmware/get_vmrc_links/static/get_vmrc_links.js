// filling data to the input elements based on selection of predefined hosts
$('#known_hosts_select').change(function () {
    $("#vmware_ip_addr").val($('#known_hosts_select option:selected').attr('ip'));
    $("#vmware_login").val($('#known_hosts_select option:selected').attr('login'));
    $("#vmware_pass").val($('#known_hosts_select option:selected').attr('pass'));
});

$(function() {
    $('#submit_form').click(function() {
        // start showing loading animation
        $.LoadingOverlay("show", {
                        image       : "",
                        fontawesome : "fa fa-cog fa-spin"
                        })
        $.ajax({
            url: window.localtion.pathname, // url: /vmware/get_vmrc_links
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $.LoadingOverlay("hide");
//                alert(response.result);
                if (response.error != "") {
                    $('#output_div').html(response.error)
                } else {
                    $('#output_div').html(response.collected_vm_info)
                }
            }
        });
    });
});
