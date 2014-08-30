$(function(){
  var host = 'dev.merron.ru';
  var tpl = $('.working');
  $('#drop img').click(function(){
    $(this).parent().find('input').click();
  });

  $('#upload').fileupload({
    dropZone: $('#drop'),
    add: function (e, data) {
      tpl.find('p').text("Uploading...").append('<i>' + formatFileSize(data.files[0].size) + '</i>');
      $('#upload ul').show();
      $('#knob').knob();

      tpl.find('span').click(function(){
        if(tpl.hasClass('working')){
          jqXHR.abort();
        }

        tpl.fadeOut(function(){
          tpl.remove();
        });
      });
      var jqXHR = data.submit();
    },

    progress: function(e, data){
      var progress = parseInt(data.loaded / data.total * 100, 10);
      $('#knob').val(progress).change();
      if(progress == 100){
        tpl.removeClass('working');
      }
    },
    
    done: function(e, data){
      tpl.find('p').text(data.files[0].name);
      $('#link').attr('value', 'http://'+host+'/'+data.result);
      
    },
    
    fail: function(e, data){
      tpl.addClass('error');
    }
  });


  $(document).on('drop dragover', function (e) {
    e.preventDefault();
  });

  function formatFileSize(bytes) {
    if (typeof bytes !== 'number') { return ''; }
    if (bytes >= 1000000000) { return (bytes / 1000000000).toFixed(2) + ' GB'; }
    if (bytes >= 1000000) { return (bytes / 1000000).toFixed(2) + ' MB'; }
    return (bytes / 1000).toFixed(2) + ' KB';
  }
  
  $('#copyButton').click(function(e){
    e.preventDefault();
  });

  var client = new ZeroClipboard($('#copyButton'));
  client.on('ready', function(readyEvent) {
    client.on('copy', function(event) {
      var clipboard = event.clipboardData;
      clipboard.setData('text/plain', $('#link').val());
    });
  });

});