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
var resourceId;

function CreateReport(rid)
{
  resourceId = rid;
  console.log('In CreateReport: ' + resourceId);

//  var b = $('<a>')
//      .attr('id', 'kp-report')
//      .attr('data-role', 'button')
//      .attr('href', '#')
//      .attr('data-theme', 'e') // yellow
//      .attr('data-icon', 'forward')
//      .text('Create Radiology Report')
//      .button();

  var b = $('<a>')
      .attr('id', 'kp-report')
      .attr('data-role', 'button')
      .attr('href', '#')
      .attr('data-theme', 'b') // blue
      .attr('data-icon', 'forward')
      .text('Create Radiology Report')
      .button();

  b.insertBefore($('#study-delete').parent().parent());
  b.click(function() {
      $.ajax({
          url: '../studies/' + resourceId + '?full',
          dataType: 'json',
          async: false,
          cache: false,
          success: function(study) {
              console.log('In Ajax success: ' + resourceId);
              console.log(study);
              var ACCESSION_NUMBER = '0008,0050';
              var PATIENT_ID = '0010,0020';
              for (var i in study.MainDicomTags) {
                  if (i == ACCESSION_NUMBER) {
                      var val = study.MainDicomTags[i].Value;
                      alert('Found ACCESSION_NUMBER: ' + val);
                  }
              }
              for (var i in study.PatientMainDicomTags) {
                  if (i == PATIENT_ID) {
                      var val = study.PatientMainDicomTags[i].Value;
                      alert('Found PATIENT_ID: ' + val);
                  }
              }
          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
              console.log('In Ajax error: ' + resourceId);
              console.log("Status: " + textStatus);
              console.log("Error: " + errorThrown);
          }
      });
  });
}

$('#study').live('pagebeforeshow', function() {
    if ($.mobile.pageData) {
        CreateReport($.mobile.pageData.uuid);
    }
});
$('#patient').live('pagebeforeshow', function() {
    if ($.mobile.pageData) {
        console.log('In Patient for ' + $.mobile.pageData.uuid);
        $('#' + 'kp-report').remove();
    }
});
$('#series').live('pagebeforeshow', function() {
    if ($.mobile.pageData) {
        console.log('In Series for ' + $.mobile.pageData.uuid);
        $('#' + 'kp-report').remove();
    }
});
$('#instance').live('pagebeforeshow', function() {
    if ($.mobile.pageData) {
        console.log('In Instance for ' + $.mobile.pageData.uuid);
        $('#' + 'kp-report').remove();
    }
});
$('#lookup').live('pagebeforeshow', function() {
    if ($.mobile.pageData) {
        console.log('In Lookup for ' + $.mobile.pageData.uuid);
        $('#' + 'kp-report').remove();
    }
});
