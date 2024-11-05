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

#define ORTHANC_PLUGIN_NAME  "report"

static OrthancPluginContext* context = NULL;

extern "C"
{
  ORTHANC_PLUGINS_API int32_t OrthancPluginInitialize(OrthancPluginContext* context)
  {
    OrthancPluginLogWarning(context, "Report plugin is initializing");
    OrthancPlugins::SetGlobalContext(context);
    Orthanc::Logging::InitializePluginContext(context);
    Orthanc::Logging::EnableInfoLevel(true);

    /* Check the version of the Orthanc core */
    if (OrthancPluginCheckVersion(context) == 0)
    {
      OrthancPlugins::ReportMinimalOrthancVersion(ORTHANC_PLUGINS_MINIMAL_MAJOR_NUMBER,
                                                  ORTHANC_PLUGINS_MINIMAL_MINOR_NUMBER,
                                                  ORTHANC_PLUGINS_MINIMAL_REVISION_NUMBER);
      return -1;
    }

    OrthancPlugins::SetDescription(ORTHANC_PLUGIN_NAME, "Add support for Study Report Writing in Orthanc.");

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
