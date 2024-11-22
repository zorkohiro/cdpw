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
function ChooseTemplate(callback)
{
  var clickedTemplate = '';
  var clickedPeer = '';
  var templates = ["first", "second", "third", "fourth"];
  var items = $('<ul>')
    .attr('data-divider-theme', 'd')
    .attr('data-role', 'listview');

  items.append('<li data-role="list-divider">Report Templates</li>');
  for (var i = 0, len = templates.length; i < len; i++) {
    var name = templates[i];
    var item = $('<li>')
      .html('<a href="#" rel="close">' + name + '</a>')
      .attr('name', name)
      .click(function() { 
        clickedTemplate = $(this).attr('name');
      });
    items.append(item);
    console.log('template['+i+'] is '+name);
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
          callback(clickedTemplate, clickedPeer);
        }
      }
      timer = setInterval(WaitForDialogToClose, 100);
    }
  });
}

function CreateReport(resourceId)
{
  console.log('In CreateReport: ' + resourceId);
  var b = $('<a>')
    .attr('id', 'kp-report')
    .attr('data-role', 'button')
    .attr('href', '#')
    .attr('data-theme', 'b') // blue
    .attr('data-icon', 'forward')
    .text('Create Study Report')
    .button();

  b.insertBefore($('#study-delete').parent().parent());
  b.click(function() {
    var session = "none";
    var mrn = "none";
    $.ajax({
      url: '../studies/' + resourceId + '?full',
      dataType: 'json',
      async: false,
      cache: false,
      success: function(study) {
        var ACCESSION_NUMBER = '0008,0050';
        var PATIENT_ID = '0010,0020';
        for (var i in study.MainDicomTags) {
          if (i == ACCESSION_NUMBER) {
            session = study.MainDicomTags[i].Value;
            break;
          }
        }
        for (var i in study.PatientMainDicomTags) {
          if (i == PATIENT_ID) {
            mrn = study.PatientMainDicomTags[i].Value;
            break;
          }
        }
        console.log(study);
        if (session != "none" && mrn != "none") {
          console.log("Study " + resourceId + ' has ACESSION_NUMBER ' + session + ' and PATIENT_ID ' + mrn);
        } else if (session == "none" && mrn == "none") {
          alert("Study has no ACCESSION_NUMBER or PATIENT_ID defined");
        } else if (session == "none") {
          alert("Study has no ACCESSION_NUMBER defined");
        } else if (mrn == "none") {
          alert("Study has no PATIENT_ID defined");
        }
      }
    }).done(function(){
      console.log("session is " + session + "; mrn is " + mrn);
      if (session != "none" && mrn != "none") {
        console.log("Calling ChooseTemplate");
        ChooseTemplate(function(server) {
            if (server != '') {
              console.log("back from ChooseTemplate: " + server);
            } else {
              console.log("back from ChooseTemplate with no cboice");
            }
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
