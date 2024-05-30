function init() {
    $(document).on('click', '.click_for_detail', function() {
        // handle click event for class click_for_detail
        let rowID = $(this).closest('tr').attr('id').split('-')[1];
        console.log('Clicked row ID:', rowID);
        window.open('/patient_page?ID=' + rowID);
        // add your logic here...
    });

    $('#table_refresh_btn').click(function() {
        $('#main_table').empty();
        $.getJSON('/get_main_table', function(data) {
            console.log(data.IDs);
            $('#main_table').append('<tr>');
            $('#main_table').append('<td> </td>');
            data.Categories.forEach(function(Cates) {
                $('#main_table').append('<td>' + Cates + '</td>');
            });
            $('#main_table').append('</tr>');

            data.IDs.forEach(function(IDs) {
                $('#main_table').append('<tr id="row-'+IDs+'"></tr>');
                console.log(IDs);
                let new_block = basic_block([String(IDs)]);
                let $new_block = $(new_block); // Convert to jQuery object
                $new_block.addClass('click_for_detail'); // Add class to the jQuery object
                new_block = $new_block[0].outerHTML; // Convert back to string
                $('#row-' + IDs).append(new_block);
                data.Categories.forEach(function(Cates) {
                    
                    $('#row-' + IDs).append('<td id=row-' + IDs + '-' + Cates.replace(/ /g, '-').replace(/\//g, '') + '></td>');
                    $.getJSON('/main_table_card?ID=' + IDs + '&Cate=' + Cates, function(response) {
                        let new_block = basic_block([response.value[0],response.value[1]]);
                        $('#row-' + IDs + '-'+Cates.replace(/ /g, '-').replace(/\//g, '') ).append(new_block);
                    });
                    
                });

            });
        });
    });
}
$(document).ready(init);

function basic_block(text_list){
    let output = '<td class="main_table_card">'
    if (text_list.length>1){
    output += '<div class="main_table_past">'+text_list[1]+'</div>'
    }
    output += '<div class="main_table_now">'+text_list[0]+'</div>'
    output += '</td>'
    return output
}

