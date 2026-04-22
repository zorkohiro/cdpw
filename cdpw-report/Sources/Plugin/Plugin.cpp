/**
 * Kaiser Permanente Report Plugin
 * Copyright (C) 2024 Kaiser Permanente
 *
 * Gratefully derived in part from Neuroimaging plugin
 * Copyright (C) 2012-2024 Sebastien Jodogne, Medical Physics
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
#include <EmbeddedResources.h>

#include <Logging.h>
#include <SystemToolbox.h>

#include "../../Resources/Orthanc/Plugins/OrthancPluginCppWrapper.h"
#include <iostream>
#include <fstream>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <syslog.h>
#include <ctype.h>

#define ORTHANC_PLUGIN_NAME "report"
#define TEMPLATES_DIR       "/usr/lib/cdpw/Templates"
#define EDITOR              "/usr/bin/spawn_editor"

/*#sizeof (emsstatic OrthancPluginContext* context = NULL;*/
static OrthancPluginContext* context = NULL;

static int spawn_editor(OrthancPluginContext* context, char *uuid, char *emsgbuf) {
  pid_t pid = fork();
  if (pid < 0) {
    sprintf(emsgbuf, "fork failed: %s", strerror(errno));
    return -1;
  } else if (pid == 0) {
    // close
    for (int i = 0; i < 100; i++) {
      close(i);
    }
    setsid();
    open("/dev/null", O_RDONLY); // open standard input
    int fdo = open("/tmp/editor.log", O_RDWR|O_APPEND|O_CREAT, 0644); // standard output
    int fds = dup(fdo); // standard error
    const char *hdr = strrchr(EDITOR, '/'); // Get last component in path for argv[0] setting
    if (hdr == NULL)
      hdr = "spawn_editor";
    int rslt = execl(EDITOR, hdr, uuid, NULL);
    if (rslt < 0) {
      char buffer[1024];
      sprintf(buffer, "exec failed: %s\n", strerror(errno));
      if (write(fdo, buffer, strlen(buffer)) != (ssize_t) strlen(buffer)) {
        buffer[strlen(buffer) - 1] = '\0';
        syslog(LOG_USER|LOG_WARNING, "%s", buffer);
      }
      if (fds >= 0) { // quiesce compiler
        close(fds);
      }
      _exit(0);
    }
  }
  return 0;
}

static void create_report(OrthancPluginRestOutput* output, const char* url, const OrthancPluginHttpRequest* request) {

  OrthancPluginContext* context = OrthancPlugins::GetGlobalContext();
  
  if (request->method != OrthancPluginHttpMethod_Post) {
    OrthancPluginSendMethodNotAllowed(context, output, "POST");
  } else {
    char buffer[1024], localb[1024], *uuid = localb;
    strcpy(uuid, (char *) request->body);
    snprintf(buffer, sizeof (buffer), "Post on URL [%s] with body [%s]", url, uuid);
    OrthancPluginLogWarning(context, buffer);
    bool failure = false;

    if (strlen(uuid) == 0) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible uuid passed");
    }
    if (failure) {
      OrthancPluginSendHttpStatusCode(context, output, 400);
      return;
    }

    // spawn_editor is responsible for tacking on any suffix to the template
    // that will identify which entry program to use
    if (spawn_editor(context, uuid, buffer) < 0) {
      OrthancPluginLogWarning(context, buffer);
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 500, buffer, strlen(buffer));
    } else {
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 200, NULL, 0);
    }
  }
}

extern "C"
{
  ORTHANC_PLUGINS_API int32_t OrthancPluginInitialize(OrthancPluginContext* context)
  {
    OrthancPluginLogWarning(context, "Report plugin is initializing");
    OrthancPlugins::SetGlobalContext(context);
    Orthanc::Logging::InitializePluginContext(context);
    Orthanc::Logging::EnableInfoLevel(true);

    /* Check the version of the Orthanc core */
    if (OrthancPluginCheckVersion(context) == 0) {
      OrthancPlugins::ReportMinimalOrthancVersion(ORTHANC_PLUGINS_MINIMAL_MAJOR_NUMBER,
                                                  ORTHANC_PLUGINS_MINIMAL_MINOR_NUMBER,
                                                  ORTHANC_PLUGINS_MINIMAL_REVISION_NUMBER);
      return -1;
    }

    OrthancPlugins::SetDescription(ORTHANC_PLUGIN_NAME, "Add support for Study Report Writing in Orthanc.");
    OrthancPlugins::RegisterRestCallback<create_report>("/cdpw/create", true /* thread safe */);

    {
      std::string explorer;
      Orthanc::EmbeddedResources::GetFileResource(
        explorer, Orthanc::EmbeddedResources::ORTHANC_EXPLORER_JS);
      OrthancPlugins::ExtendOrthancExplorer(ORTHANC_PLUGIN_NAME, explorer);
    }
    return 0;
  }

  ORTHANC_PLUGINS_API void OrthancPluginFinalize()
  {
      OrthancPluginLogWarning(context, "Report plugin is finalizing");
  }


  ORTHANC_PLUGINS_API const char* OrthancPluginGetName()
  {
    return ORTHANC_PLUGIN_NAME;
  }


  ORTHANC_PLUGINS_API const char* OrthancPluginGetVersion()
  {
    return ORTHANC_PLUGIN_VERSION;
  }
}
