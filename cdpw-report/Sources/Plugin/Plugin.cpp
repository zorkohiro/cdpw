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
#define TEMPLATES_DIR       "/usr/lib/kp-report/Templates"
#define EDITOR              "/usr/bin/spawn_editor"

/*#sizeof (emsstatic OrthancPluginContext* context = NULL;*/
static OrthancPluginContext* context = NULL;

static void fetch_templates(OrthancPluginRestOutput* output, const char* url, const OrthancPluginHttpRequest* request) {
  OrthancPluginContext* context = OrthancPlugins::GetGlobalContext();

  if (request->method != OrthancPluginHttpMethod_Get) {
    OrthancPluginSendMethodNotAllowed(context, output, "GET");
  } else {
    Json::Value result;
    char prtbuf[1024] = { 0 };
    int nent = 0;
    char modality[8] = { 0 };
    DIR *dir = opendir(TEMPLATES_DIR);

    snprintf(prtbuf, sizeof (prtbuf), "%s: URL %s", __func__, url);
    OrthancPluginLogWarning(context, prtbuf);

    const char *resourceId = strrchr(url, '/');
    if (resourceId) {
        resourceId++;
        snprintf(prtbuf, sizeof (prtbuf), "%s: URL called with resourceId %s", __func__, resourceId);
        OrthancPluginLogWarning(context, prtbuf);
    }

    if (resourceId) {
        FILE *pp;
        snprintf(prtbuf, sizeof (prtbuf), "GetModality -r %s", resourceId);
        OrthancPluginLogWarning(context, prtbuf);
        pp = popen(prtbuf, "r");
        if (pp != NULL) {
            char lbuf[24];
            if (fgets(lbuf, sizeof (lbuf), pp) != NULL) {
                char *ridx = strrchr(lbuf, '\n');
                if (ridx) {
                    *ridx = '\0';
                    snprintf(prtbuf, sizeof (prtbuf), "GetModality of %s returns %s", resourceId, lbuf);
                    OrthancPluginLogWarning(context, prtbuf);
                    // Convert to lower case as we copy to modality
                    for (size_t index = 0; lbuf[index] && index < sizeof (modality) - 1; index++) {
                        modality[index] = lbuf[index];
                        if (isupper(lbuf[index]))
                           modality[index] += ' ';
                    }
                    snprintf(prtbuf, sizeof (prtbuf), "Modality is now %s", modality);
                    OrthancPluginLogWarning(context, prtbuf);
                }
            }
            pclose(pp);
        }
    }
    if (dir) {
      snprintf(prtbuf, sizeof (prtbuf) - 1, "Opened TEMPLATES_DIR %s", TEMPLATES_DIR);
      OrthancPluginLogWarning(context, prtbuf);
      struct dirent *ent;
      while ((ent = readdir(dir)) != NULL) {
        char *suffix = strstr(ent->d_name, ".json");
        if (suffix && strlen(suffix) == 5) {
          if (modality[0]) {
              if (strncmp(ent->d_name, modality, strlen(modality)) != 0) {
                  snprintf(prtbuf, sizeof (prtbuf) - 1, "skipping %s because front of name does not match modality %s", ent->d_name, modality);
                  OrthancPluginLogWarning(context, prtbuf);
                  continue;
              }
          }
          snprintf(prtbuf, sizeof (prtbuf) - 1, "Appending %s", ent->d_name);
          OrthancPluginLogWarning(context, prtbuf);
          /*
           * We already know we have the suffix .json.
           * We own the data that a pointer was returned
           * for and we aren't using it after this, so
           * we can muck with it.
           */
          *suffix = '\0';
          // Convert all '_' to ' ' for pretty print in a menu
          for (char *ptr = ent->d_name; *ptr; ptr++) {
            if (*ptr == '_')
              *ptr = ' ';
          }
          result.append(ent->d_name);
          nent++;
        } else {
          snprintf(prtbuf, sizeof (prtbuf) - 1, "Did not append %s", ent->d_name);
          OrthancPluginLogWarning(context, prtbuf);
        }
      }
      closedir(dir);
    } else {
      snprintf(prtbuf, sizeof (prtbuf) - 1,  "failed to open TEMPLATES_DIR %s", TEMPLATES_DIR);
      OrthancPluginLogWarning(context, prtbuf);
    }
    /*
     * If we have a modality but no entries, we have a modality for which we have no template.
     * Use the generic template instead.
     */
    char buffer[64];
    if (nent == 0 && modality[0]) {
      snprintf(buffer, sizeof (buffer), "no templates found for modality %s", modality);
      OrthancPluginLogWarning(context, buffer);
      result.append("generic");
      nent++;
    } else if (nent == 0) {
      snprintf(buffer, sizeof (buffer), "no templates found");
      OrthancPluginLogWarning(context, buffer);
      OrthancPluginAnswerBuffer(context, output, buffer, strlen(buffer), "text/plain");
      return;
    }
    snprintf(prtbuf, sizeof (prtbuf) - 1, "sending back json list of %d entries", nent);
    OrthancPluginLogWarning(context, prtbuf);
    std::string answer = result.toStyledString();
    OrthancPluginAnswerBuffer(context, output, answer.c_str(), answer.size(), "application/json");
  }
}

static int spawn_editor(OrthancPluginContext* context, char *tmplt, char *uuid, char *emsgbuf) {
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
    int rslt = execl(EDITOR, hdr, tmplt, uuid, NULL);
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
    char buffer[1024], localb[1024], *sptr = NULL, *rqb = localb;
    strcpy(rqb, (char *) request->body);
    snprintf(buffer, sizeof (buffer), "Post on URL [%s] with body [%s]", url, rqb);
    OrthancPluginLogWarning(context, buffer);
    const char *colon = ":";
    char *uuid = strtok_r(rqb, colon, &sptr);
    char *json_tmplt = strtok_r(NULL, colon, &sptr);
    bool failure = false;

    if (uuid == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible uuid passed");
    } else if (json_tmplt == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible template name passed");
    }
    if (failure) {
      OrthancPluginSendHttpStatusCode(context, output, 400);
      return;
    }

    // Convert ' ' in json_tmplt to '_' which is how it is stored in reality
    char jsonfile[128] = { 0 };
    int i = 0;
    for (char *ptr = json_tmplt; *ptr; ptr++, i++) {
      if (*ptr == ' ')
        jsonfile[i] = '_';
      else
        jsonfile[i] = *ptr;
    }
    // spawn_editor is responsible for tacking on any suffix to the template
    // that will identify which entry program to use
    if (spawn_editor(context, jsonfile, uuid, buffer) < 0) {
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
    OrthancPlugins::RegisterRestCallback<fetch_templates>("/kp-report/templates/([^/]*)", true /* thread safe */);
    OrthancPlugins::RegisterRestCallback<create_report>("/kp-report/create", true /* thread safe */);

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
