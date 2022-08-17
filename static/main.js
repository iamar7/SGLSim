// /SGLSim_Basic/templates/main.js
$(document).ready(function() {

var MaxInputs       = 3;
var InputsWrapper   = $("#InputsWrapper");
var AddButton       = $("#AddMoreFileBox");

var x = InputsWrapper.length;
var FieldCount=1;


$(AddButton).click(function (e)
{
        if(x <= MaxInputs)
        {
            FieldCount++;
            $(InputsWrapper).append('<tbody class = "r1ow">'+
              '<tr>'+
                // '<td  style="text-align: center;">'+FieldCount+'</td>'+
                '<td  style="text-align: center;"><input type="text" id="uValue" name="uvalue[]" value="1.812" class="form-control" /></td>'+
                '<td  style="text-align: center;"><input type="text" id="shgc" name="shgc[]" value="0.227" class="form-control" /></td>'+
                '<td  style="text-align: center;"><input type="text" id="vlt" name="vlt[]" value="0.229" class="form-control" /></td>'+
                '<td  style="text-align: center;"><a href="#" class="btn btn-danger removeclass">Remove</a></td>'+
                // '<td  style="text-align: center;"><input type="checkbox" class="foo" id="checkbox" name="checkbox" value="pv">'+
                // 'Add PV</td>'+
              '</tr>'+
            '</tbody>'+
            '<br><br>');
            x++;
        }
return false;
});
$("body").on("click",".removeclass", function(e){
        if(x>1){
                $(this).closest(".r1ow").remove()
                FieldCount--;
                x--;
        }
return false;
})
 $('#submit').click(function(){
           $.ajax({
                url:"/postskill",
                method:"POST",
                data:$('#add_skills').serialize(),
                success:function(data)
                {  alert(data)
                     $('#resultbox').html(data);
                     $('#add_skills')[0].reset();
                }
           });
      });
});
