$(document).ready(function() {
    var counter = 0;

    $("#addrow").on("click", function() {
        var newRow = $("<tr>");
        var cols = "";

        cols += '<td><input type="text" class="form-control" name="num-box' + counter + '"/></td>';
        cols += '<td><input type="text" class="form-control" name="lat-box' + counter + '"/></td>';
        cols += '<td><input type="text" class="form-control" name="lng-box' + counter + '"/></td>';
        cols += '<td><input type="text" class="form-control" name="alt-box' + counter + '"/></td>';

        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        newRow.append(cols);
        $("table.order-list").append(newRow);
        counter++;
    });



    $("table.order-list").on("click", ".ibtnDel", function(event) {
        $(this).closest("tr").remove();
        counter -= 1
    });


});



function calculateRow(row) {
    var price = +row.find('input[name^="price"]').val();

}

function calculateGrandTotal() {
    var grandTotal = 0;
    $("table.order-list").find('input[name^="price"]').each(function() {
        grandTotal += +$(this).val();
    });
    $("#grandtotal").text(grandTotal.toFixed(2));
}
