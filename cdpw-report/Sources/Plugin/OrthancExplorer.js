/**
 * Kaiser Permanente report writer plugin for Orthanc
 * Copyright (C) 2024 Kaiser Permanente
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 **/

function ChooseTemplate(callback, id)
{
  var clickedTemplate = '';
  var items = $('<ul>')
    .attr('data-divider-theme', 'd')
    .attr('data-role', 'listview');

  items.append('<li data-role="list-divider">Report Templates</li>');
  $.ajax({
    url: '../kp-report/templates/' + $.mobile.pageData.uuid,
    type: 'GET',
    dataType: 'json',
    async: false,
    cache: false,
    success: function(templates) {
      console.log('GET callback returned: ' + templates);
      var name, item;
      if (templates.length > 0) {
        for (var i = 0; i < templates.length; i++) {
          name = templates[i];
          let item = $('<li>')
            .html('<a href="#" rel="close">' + name + '</a>')
            .attr('name', name)
            .click(function() { 
              clickedTemplate = $(this).attr('name');
            });
          items.append(item);
          console.log("adding attr " + name);
        }
      }
      // Launch the dialog
      $(document).simpledialog2({
        mode: 'blank',
        animate: false,
        headerText: 'Choose Report Template',
        headerClose: true,
        forceInput: false,
        width: '100%',
        blankContent: items,
        callbackClose: function() {
          var timer;
          function WaitForDialogToClose() {
            if (!$('#dialog').is(':visible')) {
              clearInterval(timer);
              callback(clickedTemplate);
            }
          }
          timer = setInterval(WaitForDialogToClose, 100);
        }
      });
    },
    error: function(xhr, status, error) {
      console.log("failed to run GET, status: " + status + " error: " + error);
    }
  });
}

function CreateReport(resourceId)
{
  var b = $('<a>')
    .attr('id', 'kp-report')
    .attr('data-role', 'button')
    .attr('href', '#')
    .attr('data-theme', 'b') // blue
    .attr('data-icon', 'forward')
    .text('Create Study Report')
    .button();

  console.log("resource ID is " + resourceId);
  b.insertBefore($('#study-delete').parent().parent());
  b.click(function() {
    var studyid;
    $.ajax({
      url: '../studies/' + resourceId + '?full',
      dataType: 'json',
      async: false,
      cache: false,
      success: function(study) {
        studyid = study.ID;
        console.log("Study " + resourceId);
      }
    }).done(function(){
      if (studyid) {
        ChooseTemplate(function(template_choice) {
            if (template_choice == '') {
              console.log("back from ChooseTemplate with no choice");
              return;
            }
            var pdata = studyid + ":" + template_choice;
            $.ajax({
              url: '../kp-report/create',
              type: 'POST',
              dataType: 'text',
              data: pdata,
              async: false,
              success: function(job) {
              },
              error: function(xhr, status, error) {
                if (xhr.status == 500) {
                  alert(xhr.responseText);
                } else {
                  alert("failed to run POST, status: " + xhr.status);
                }
              }
            });
        });
      }
    });
  });
}

$('#study').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    if ($.mobile.pageData.uuid) {
        CreateReport($.mobile.pageData.uuid);
    }
  }
});
$('#patient').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'kp-report').remove();
  }
});
$('#series').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'kp-report').remove();
  }
});
$('#instance').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'kp-report').remove();
  }
});
$('#lookup').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'kp-report').remove();
  }
});
