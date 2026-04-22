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

function CreateReport(resourceId)
{
  var b = $('<a>')
    .attr('id', 'cdpw')
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
        $.ajax({
          url: '../cdpw/create',
          type: 'POST',
          dataType: 'text',
          data: studyid,
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
    $('#' + 'cdpw').remove();
  }
});
$('#series').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'cdpw').remove();
  }
});
$('#instance').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'cdpw').remove();
  }
});
$('#lookup').live('pagebeforeshow', function() {
  if ($.mobile.pageData) {
    $('#' + 'cdpw').remove();
  }
});
