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
  $('#' + 'Reports').remove();

  var b = $('<a>')
      .attr('id', 'Reports')
      .attr('data-role', 'button')
      .attr('href', '#')
      .attr('data-icon', 'forward')
      .attr('data-theme', 'e')
      .text('Create Radiology Report');
      .button();

  b.insertBefore($('#series-delete').parent().parent());

  b.click(function() {
    if ($.mobile.pageData) {
      alert('here I am');
    }
  });
}

$('#study').live('pagebeforeshow', function() {
  CreateReport($.mobile.pageData.uuid);
});
