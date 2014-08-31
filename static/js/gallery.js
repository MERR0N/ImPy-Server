$(function(){
  var selectMode = false;
  
  $('#select').click( function(e){
    if($('#select').hasClass('active')){
      $('#select').removeClass('active');
      $('#all, #none, #delete').hide();
      selectMode = false;

    }else{
      $('#select').addClass('active');
      $('#all, #none, #delete').show();
      selectMode = true;
    }
    return false;
  });
  
  $('#all').click( function(e){
    $('.image img').addClass('selected')
  });
  
  $('#none').click( function(e){
    $('.image img').removeClass('selected')
  });
  
  $('#delete').click( function(e){
    $('.selected').each(function( index ) {
      $.get( host+'/del/'+userkey+$(this).parent().attr("href"), function( data ) {
        
      });
      $(this).parent().parent().remove();
    });
  });

  $('.image a').click( function(e){
    if(selectMode){
      if($(e.target).hasClass("selected")){
        $(e.target).removeClass("selected");
      }else{
        $(e.target).addClass("selected");
      }
      return false;
    }
  });
  
});