$(document).ready(function() { 
  $("#rundb-loading").hide();
    var options = { 
        //target:        '#rundb-maintable',   // target element(s) to be updated with server response 
        beforeSubmit:  rundb_frmSearch_onBeforeSubmit,  // pre-submit callback 
        success:       rundb_frmSearch_onSuccess,  // post-submit callback 
        error: function() { alert('boo'); }
        // other available options: 
        //url:       url         // override for form's 'action' attribute 
        //type:      type        // 'get' or 'post', override for form's 'method' attribute 
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
        //clearForm: true        // clear all form fields after successful submit 
        //resetForm: true        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        //timeout:   3000 
    }; 
 
    // bind form using 'ajaxForm' 
    $('#frmSearch').ajaxForm(options);

    $('#rundb-formControl').toggle(
      function(){
        $('#frmSearch').slideUp();        
        $('#rundb-formControl-show').show();        
        $('#rundb-formControl-hide').hide();        
      },
      function(){
        $('#frmSearch').slideDown();        
        $('#rundb-formControl-show').hide();        
        $('#rundb-formControl-hide').show();        
      }
    );
}); 

function rundb_frmSearch_onBeforeSubmit()
{
  $("#rundb-loading").show();
  $("#rundb-tblMain").hide();
}

function rundb_frmSearch_onSuccess(response){
  $("#rundb-loading").hide();
  $("#rundb-tblMain").show();
  $("#rundb-tblMain").html(response);

  $('#rundb-formControl').click();
}

function rundb_showfiles(runid,page)
{
  var run_files_row = $('#run-files-row-'+runid);
  if (!((run_files_row.length>0) && (page==1))){
	  $.ajax({
		    url: '/rundb/files?runid='+runid+'&p='+page,
		    cache: false,
		    success: function(data) {
            if (page==1){
                $('#run-'+runid).after(data);
             }else{
                $('.rundb-files-next-'+runid).replaceWith(data);
             }
		    }});
  }else{
    run_files_row.toggle();
  }
  return false;
}

function rundb_file_pin(fileid)
{
  $.ajax({
    url: '/rundb/file-pin?fileid='+fileid,
    cache: false,
    success: function(data) {
        var pin_span = $('#rundb-file-pin-'+fileid+' span');
        switch(data['refcount'])
        {
          case 0:
            pin_span.removeClass("ss_tag_blue_delete").addClass('ss_tag_blue_add');
            break;
          case 1:
            pin_span.removeClass("ss_tag_blue_add").addClass('ss_tag_blue_delete');
            break;
          default:
            alert("reference count = "+data['refcount']);
            break;
        }
        $("#rundb-file-log-"+fileid).show();
    },
    error: function(request, textStatus, errorThrown){
      alert(textStatus);
    }
  });
	return false;
}

function rundb_files_pin(runid)
{
  $(".rundb-file-row-"+runid).find(".ss_tag_blue_add").parent().click();
  return false;
}

function rundb_files_unpin(runid)
{
  $(".rundb-file-row-"+runid).find(".ss_tag_blue_delete").parent().click();
  return false;
}

function rundb_file_log(fileid)
{
  $("#rundb-file-log-"+fileid).fancybox();
  return false;
}

