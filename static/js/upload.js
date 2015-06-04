(function(){
  var tpl = $('.working');
  
  $('#drop div').click(function(){
    $(this).parent().find('input').click();
  });
  $('#copyButton').click( function(e){
    e.preventDefault();
  });
  $(document).on('drop dragover', function (e) {
    e.preventDefault();
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
      $('#link').attr('value', host+'/'+data.result);
      
    },
    
    fail: function(e, data){
      tpl.addClass('error');
    }
  });
  
  var clipboardClient = new ZeroClipboard($('#copyButton'));
  clipboardClient.on('ready', function(readyEvent) {
    clipboardClient.on('copy', function(event) {
      var clipboard = event.clipboardData;
      clipboard.setData('text/plain', $('#link').val());
    });
  });
  
  function formatFileSize(bytes) {
    if (typeof bytes !== 'number') { return ''; }
    if (bytes >= 1000000000) { return (bytes / 1000000000).toFixed(2) + ' GB'; }
    if (bytes >= 1000000) { return (bytes / 1000000).toFixed(2) + ' MB'; }
    return (bytes / 1000).toFixed(2) + ' KB';
  }  
  
})();