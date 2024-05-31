function init() {
    $('#category_list').on('click','td',function(){
        var Cate = $(this).text();
        var $this = $(this);
        if ($this.next().is('div')) {
            var chk = 1;
        } else {var chk = 0;}
        var ID = document.getElementById('patient_id').innerText;
        $.getJSON('/get_filtered_data?ID=' + ID + '&Cate=' + Cate, function(response) {
            var uniqueLabels = new Set(response.Label);
            uniqueLabels.forEach(function(Label){
                if (chk) {
                $this.next().remove();
                } else {
                var cell = document.createElement('div');
                cell.setAttribute("id", "idx_categories_detail");
                cell.setAttribute("class", "btn btn-secondary");
                cell.style.width = "80%";
                cell.appendChild(document.createTextNode(Label));
                $this.after(cell);
            }

            });
        });
    });
    
    $('#category_list').on('click','div',function(){
        var Label = $(this).text();
        var Label_txt = Label.replace(/ /g, '-').replace(/\//g, '');
        var ID = document.getElementById('patient_id').innerText;
        $.getJSON('/get_filtered_data?ID=' + ID + '&Label=' + Label, function(response) {
            if (document.getElementById('result_cards-' + Label_txt) !== null) {
                $('#result_cards-' + Label_txt).remove();
            } else{
                var card = document.createElement('div');
                card.setAttribute("id", "result_cards-"+Label_txt);
                card.setAttribute("class", "Result_Block");
                card.appendChild(document.createTextNode(Label));
                $('.screen_03_detail_results').append(card);

            var plot_btn = document.createElement('div');
            plot_btn.setAttribute("id", "plot_btn");
            plot_btn.setAttribute("class", "btn btn-secondary");
            plot_btn.style.width = "5wv";
            plot_btn.style.height = "5hv";
            $('#result_cards-' + Label_txt).append(plot_btn);
            response.Idx.forEach(function(Idx) {
                var card = document.createElement('div');
                card.setAttribute("id", "Card_"+Idx);
                card.setAttribute("class", "Card result_Cards");
                card.innerText = response.Date[Idx]+'\n'+response.CategoryName[Idx]+'\n'+response.Label[Idx]+'\n'+response.Value[Idx];
                $('#result_cards-' + Label_txt).append(card);
            });
        };
        });
    });
    $('#plot_btn').click(function(){
        var $this = $(this);
        var card = document.createElement('div');
        card.setAttribute("id", "scatter_plot");
        $this.next(card);
        var Label = $this.parent().text();
        var ID = document.getElementById('patient_id').innerText;
        $.getJSON('/get_filtered_data?ID=' + ID + '&Label=' + Label, function(response) {
            scatter_plot(response);
        });
    });
    
}
$(document).ready(init);
function scatter_plot(data){
    var scatter_data = [];
    data.Idx.forEach(function(Idx){
        scatter_data += [{x: data.Date[Idx], y: data.Value[Idx]}];
    });
    var margin = {top: 20, right: 30, bottom: 30, left: 40},
        width = 800 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    var svg = d3.select("#scatter_plot")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var x = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d.x; })])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d.y; })])
        .range([height, 0]);
    // Add X axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    svg.append("g")
        .call(d3.axisLeft(y));

    // Add dots
    svg.selectAll("dot")
        .data(scatter_data)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("cx", function(d) { return x(d.x); })
        .attr("cy", function(d) { return y(d.y); })
        .attr("r", 5);

}