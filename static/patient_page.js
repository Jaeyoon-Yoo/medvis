function init() {
    $('#category_list').on('click','td',function(){
        var Cate = $(this).text();
        var Cate_txt = Cate.replace(/ /g, '-').replace(/\//g, '');
        var ID = document.getElementById('patient_id').innerText;
        $.getJSON('/get_filtered_data?ID=' + ID + '&Cate=' + Cate, function(response) {
            if (document.getElementById('result_cards-' + Cate_txt) !== null) {
                $('#result_cards-' + Cate_txt).remove();
            } else{
                var card = document.createElement('div');
                card.setAttribute("id", "result_cards-"+Cate_txt);
                card.setAttribute("class", "Result_Block");
                $('.screen_03_detail_results').append(card);
            response.Idx.forEach(function(Idx) {
                var card = document.createElement('div');
                card.setAttribute("id", "Card_"+Idx);
                card.setAttribute("class", "Card result_Cards");
                card.innerText = response.Date[Idx]+'\n'+response.CategoryName[Idx]+'\n'+response.Label[Idx]+'\n'+response.Value[Idx];
                $('#result_cards-' + Cate_txt).append(card);
            });
        };
        });
    });
    
}
$(document).ready(init);