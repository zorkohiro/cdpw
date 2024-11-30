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
// static content for now
const template_files = [ "US_RUQ.odt", "ct_abd_pelvis_with_contrast.odt", "ct_chest_without_contrast.odt", "xray_chest.odt" ];
const template_title = [ "ULTRASOUND RIGHT UPPER QUADRANT ABDOMEN", "CT ABDOMEN PELVIS WITH CONTRAST", "CT CHEST WITHOUT CONTRAST", "XRAY CHEST" ];

function ChooseTemplate(callback)
{
  var clickedTemplate = '';
  var items = $('<ul>')
    .attr('data-divider-theme', 'd')
    .attr('data-role', 'listview');

  items.append('<li data-role="list-divider">Report Templates</li>');
  $.ajax({
    url: '../kp-report/templates',
    type: 'GET',
    dataType: 'text',
    async: false,
    cache: false,
    success: function(templates) {
      console.log('GET callback returned: ' + templates);
      for (let i = 0, len = template_title.length; i < len; i++) {
        let name = template_title[i];
        let item = $('<li>')
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
    var session, mrn, studyid;
    $.ajax({
      url: '../studies/' + resourceId + '?full',
      dataType: 'json',
      async: false,
      cache: false,
      success: function(study) {
        var ACCESSION_NUMBER = '0008,0050';
        var PATIENT_ID = '0010,0020';
        for (let i in study.MainDicomTags) {
          if (i == ACCESSION_NUMBER) {
            session = study.MainDicomTags[i].Value;
            break;
          }
        }
        for (let i in study.PatientMainDicomTags) {
          if (i == PATIENT_ID) {
            mrn = study.PatientMainDicomTags[i].Value;
            break;
          }
        }
        console.log(study);
        if (session && mrn) {
          studyid = study.ID;
          console.log("Study " + resourceId + ' has ACESSION_NUMBER ' + session + ' and PATIENT_ID ' + mrn);
        } else if (!session && !mrn) {
          alert("Study has no ACCESSION_NUMBER or PATIENT_ID defined");
        } else if (!session) {
          alert("Study has no ACCESSION_NUMBER defined");
        } else if (!mrn) {
          alert("Study has no PATIENT_ID defined");
        }
      }
    }).done(function(){
      if (session  && mrn) {
        ChooseTemplate(function(template_choice) {
            var templfil;
            if (template_choice == '') {
              console.log("back from ChooseTemplate with no cboice");
              return;
            }
            var found = false;
            for (let i = 0; i < template_title.length; i++) {
              if (template_choice == template_title[i]) {
                templfil = template_files[i];
                found = true;
                break;
              }
            }
            if (!found) {
              console.log("Did not find a choice!");
              return;
            }
            var pdata = mrn + ":" + session + ":" + templfil + ":" + resourceId;
            $.ajax({
              url: '../kp-report/create',
              type: 'POST',
              dataType: 'text',
              data: pdata,
              async: false,
              success: function(job) {
              },
              error: function(xhr, status, error) {
                alert("failed to run POST, status: " + xhr.status);
                if (xhr.status == 500) {
                  alert(xhr.responseText);
                }
              }
            });
            // alert("This functionality is not yet enabled");
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
