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

#define ORTHANC_PLUGIN_NAME  "report"
#define TEMPLATES_DIR "/usr/share/orthanc/templates"
#define REPORT_DIR "/var/tmp"

static OrthancPluginContext* context = NULL;

static void fetch_templates(OrthancPluginRestOutput* output, const char* url, const OrthancPluginHttpRequest* request) {
  OrthancPluginContext* context = OrthancPlugins::GetGlobalContext();
  
  if (request->method != OrthancPluginHttpMethod_Get) {
    OrthancPluginSendMethodNotAllowed(context, output, "GET");
  } else {
    char buffer[1024] = { 0 };
    DIR *dir = opendir(TEMPLATES_DIR);
    if (dir) {
      struct dirent *ent;
      while ((ent = readdir(dir)) != NULL) {
        char *suffix = strstr(ent->d_name, ".odt");
        if (suffix && strlen(suffix) == 4) {
          if (buffer[0]) {
            strcat(buffer, ", ");
            strcat(buffer, ent->d_name);
          } else {
            strcpy(buffer, ent->d_name);
          }
        }
      }
      closedir(dir);
    }
    if (buffer[0] == '\0') {
      snprintf(buffer, sizeof (buffer), "no templates found");
    }
    OrthancPluginAnswerBuffer(context, output, buffer, strlen(buffer), "text/plain");
  }
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
    char *mrn = strtok_r(rqb, colon, &sptr);
    char *session = strtok_r(NULL, colon, &sptr);
    char *odt_template = strtok_r(NULL, colon, &sptr);
    char *uuid = strtok_r(NULL, colon, &sptr);
    bool failure = false;
    if (mrn == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible mrn passed");
    } else if (session == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible session passed");
    } else if (odt_template == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible template type passed");
    } else if (uuid == NULL) {
      failure = true;
      OrthancPluginLogWarning(context, "No discernible uuid passed");
    }
    if (failure) {
      OrthancPluginSendHttpStatusCode(context, output, 400);
      return;
    }
    char wfile[256];
    size_t snr = snprintf(wfile, sizeof (wfile), "%s/study_%s_%s.odt", REPORT_DIR, mrn, session);
    char tfile[256];
    size_t snt =  snprintf(tfile, sizeof (tfile), "%s/%s", TEMPLATES_DIR, odt_template);

    if (snr < 0 || snr >= sizeof (wfile) || snt < 0 || snt >= sizeof (tfile)) {
      strcpy(buffer, "one of the filenames too long or unparseable");
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 500, buffer, strlen(buffer));
      return;
    }

    if (access(wfile, F_OK) == 0) {
      strcpy(buffer, "report file for this study already exists");
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 500, buffer, strlen(buffer));
      return;
    }
    if (access(tfile, R_OK) != 0) {
      snprintf(buffer, sizeof (buffer), "template file %s does not exist in %s", odt_template, TEMPLATES_DIR);
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 500, buffer, strlen(buffer));
      return;
    }
    int statusCode = 200;

    failure = false;
    char emsg[1024];
    sprintf(emsg, "exception in copying from template");
    try {
      do {
        std::ifstream source(tfile, std::ifstream::binary);
        if (!source) {
          sprintf(emsg, "failed to open %s", odt_template);
          failure = true;
          break;
        }

        std::ofstream dest(wfile, std::ofstream::binary);
        if (!dest) {
          sprintf(emsg, "failed to create study_%s_%s.odt", mrn, session);
          failure = true;
          break;
        }

        sprintf(emsg, "reading source file");
        dest << source.rdbuf();

        sprintf(emsg, "closing source file");
        source.close();

        sprintf(emsg, "closing destination file");
        dest.close();

      } while (false);
    } catch (...) {
      failure = true;
    }

    if (failure) {
      snprintf(buffer, sizeof (buffer), "%s", emsg);
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, 500, buffer, strlen(buffer));
    } else {
      OrthancPluginSetHttpHeader(context, output, "Content-Type", "text/plain");
      OrthancPluginSendHttpStatus(context, output, statusCode, NULL, 0);
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
    OrthancPlugins::RegisterRestCallback<fetch_templates>("/kp-report/templates", true /* thread safe */);
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
