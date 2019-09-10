import arcpy
import shutil
import os

# Commands for the ArcGIS Python interpreter, to (1) get into the right directory, and (2) execute this script
# import os; os.chdir("U:\\FY2020\\Transportation\\SidewalkWalksheds\\Delphine_Sidewalks\\Python"); execfile(r'prep_network.py')

# Global settings
REMOVE_INTERMEDIARY_LAYERS_OPTION = "yes"  # or "no"

# Set up global variables
base_path = "U:\\FY2020\\Transportation\\SidewalkWalksheds\\Delphine_Sidewalks"
gdb_path = base_path + "\\Data\\Network_data\\dvrpc_ped_assets_dk_newer_MM.gdb"
dataset_path = gdb_path + "\\utm18n"

log_path = base_path + "\\Error_log"

# Set up ArcGIS env variables
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# Optionally remove intermediary layers generated during the analysis
def remove_intermediary_layers(layers_to_remove):
    if REMOVE_INTERMEDIARY_LAYERS_OPTION == "yes":
        mxd=arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if lyr.name in layers_to_remove:
                arcpy.mapping.RemoveLayer(df, lyr)

# Prepare the line features classes (sidewalk, crosswalk)
def prep_lines():
    # Load the original vector file
    arcpy.MakeFeatureLayer_management("utm18n\\PED_LINE", "PED_LINE")

    # Select the sidewalk features for the line features
    arcpy.SelectLayerByAttribute_management("PED_LINE", "NEW_SELECTION", "line_type = 1")

    # Save to a new feature class and do some clean up
    arcpy.CopyFeatures_management("PED_LINE", "utm18n\\sidewalks")
    arcpy.SelectLayerByAttribute_management("PED_LINE", "CLEAR_SELECTION")

    # Select the crosswalk features
    arcpy.SelectLayerByAttribute_management("PED_LINE", "NEW_SELECTION", "line_type = 2")

    # Save to a new feature class and do some clean up
    arcpy.CopyFeatures_management("PED_LINE", "utm18n\\crosswalks")
    arcpy.SelectLayerByAttribute_management("PED_LINE", "CLEAR_SELECTION")

    # Clean up
    remove_intermediary_layers(["PED_LINE"])

def prep_points():
    # Load the original vector file for the ramps
    arcpy.MakeFeatureLayer_management("utm18n\\RAMP_PT", "RAMP_PT")

    # Select the "existing" ramps
    arcpy.SelectLayerByAttribute_management("RAMP_PT", "NEW_SELECTION", "status = 'EXISTING'")

    # Save to a new feature class and do some clean up
    arcpy.CopyFeatures_management("RAMP_PT", "utm18n\\ramps_existing")
    arcpy.SelectLayerByAttribute_management("RAMP_PT", "CLEAR_SELECTION")

    # Select the other types of ramps
    arcpy.SelectLayerByAttribute_management("RAMP_PT", "NEW_SELECTION", "status = 'EXISTING'")

    # Save to a new feature class and do some clean up
    arcpy.CopyFeatures_management("RAMP_PT", "utm18n\\ramps_other")
    arcpy.SelectLayerByAttribute_management("RAMP_PT", "CLEAR_SELECTION")

    remove_intermediary_layers(["RAMP_PT"])

def cleanup():
    remove_intermediary_layers(["PED_LINE"])
    remove_intermediary_layers(["RAMP_PT"])

# In progress:
def build_network():
    #Check out the Network Analyst extension license
    #arcpy.CheckOutExtension("Network")

    temp_dir = os.environ.get("TEMP")
    # That's C:\Users\dkhanna\AppData\Local\Temp\arc81A4

    if temp_dir:
        shutil.copy2(temp_dir + "test.txt", log_path)
        #shutil.copy2(os.path.join(temp_dir, "BuildErrors.txt"), log_path)



# ***************************************
# Begin Main
#prep_lines()
#prep_points()
#cleanup()
 build_network()
