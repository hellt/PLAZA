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
        // compose URL (newPathname) which will prepend jquery function URL
        // in the case of base URL like this: /vmware/get_vmrc_links.html
        // we need to get /vmware portion, since our flask blueprint is registered at this point
        var base_url = window.location.pathname.split('/')
        var newPathname = "/";
        for (i = 1; i < base_url.length-1; i++) {
          newPathname += base_url[i];
        }
//        alert(newPathname)
        $.ajax({
            url: newPathname + '/get_vmrc_links', // url: /vmware/get_vmrc_links
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