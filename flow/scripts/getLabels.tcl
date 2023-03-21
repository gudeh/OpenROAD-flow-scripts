puts "\nRunning getLabels.tcl"
# Read liberty files
source $::env(SCRIPTS_DIR)/read_liberty.tcl

# Read def
if {[info exist ::env(DEF_FILE)]} {
    # Read lef
    read_lef $::env(TECH_LEF)
    read_lef $::env(SC_LEF)
    if {[info exist ::env(ADDITIONAL_LEFS)]} {
      foreach lef $::env(ADDITIONAL_LEFS) {
        read_lef $lef
      }
    }
    set input_file $::env(DEF_FILE)
    read_def $input_file
} else {
    set input_file $::env(ODB_FILE)
    read_db $input_file
}

if {![info exist ::env(GUI_NO_TIMING)]} {
  # Determine design stage (1 ... 6)
  set design_stage [lindex [split [file tail $input_file] "_"] 0]
  
  # Read SDC, first try to find the most recent SDC file for the stage
  set sdc_file ""
  for {set s $design_stage} {$s > 0} {incr s -1} {
    set sdc_file [glob -nocomplain -directory $::env(RESULTS_DIR) -types f "${s}_\[A-Za-z\]*\.sdc"]
    if {$sdc_file != ""} {
      break
    }
  }
  if {$sdc_file == ""} {
    set sdc_file $::env(SDC_FILE)
  }
  read_sdc $sdc_file
  if [file exists $::env(PLATFORM_DIR)/derate.tcl] {
    source $::env(PLATFORM_DIR)/derate.tcl
  }
  
  source $::env(PLATFORM_DIR)/setRC.tcl
  if {$design_stage >= 4} {
    # CTS has run, so propagate clocks
    set_propagated_clock [all_clocks]
  }
  
  if {$design_stage >= 6 && [file exist $::env(RESULTS_DIR)/6_final.spef]} {
    puts "Loading spef!"
    read_spef $::env(RESULTS_DIR)/6_final.spef
  } elseif {$design_stage >= 3} {
    puts "Estimating parasitics"
    estimate_parasitics -placement
  }
  
# Cleanup temporary variables
  unset sdc_file s design_stage
}

################################################################
################# My additions from gui.tcl #####################
################################################################
set designPath congestionPrediction/dataSet/${::env(DESIGN_NAME)}
file mkdir $designPath

#for printScreens of layouts
set printsPath congestionPrediction/layoutPrints
file mkdir $printsPath

#moving yosys outpupt files (it doesnt have access to design names)
file rename -force congestionPrediction/DGLedges.csv congestionPrediction/dataSet/${::env(DESIGN_NAME)}/DGLedges.csv
file rename -force congestionPrediction/DGLcells.csv congestionPrediction/dataSet/${::env(DESIGN_NAME)}/DGLcells.csv

################## GATES POSITIONS #################
set dut gatesPosition_
set fileName ${designPath}/${dut}${::env(DESIGN_NAME)}.csv
set outFile [open $fileName w]
puts $outFile "Name,xMin,yMin,xMax,yMax"
set block [ord::get_db_block]
foreach inst [$block getInsts] { 
  set box [$inst getBBox] 
  puts $outFile "[$inst getName], [ord::dbu_to_microns [$box xMin]], [ord::dbu_to_microns [$box yMin]], [ord::dbu_to_microns [$box xMax]], [ord::dbu_to_microns [$box yMax]]" 
}
close $outFile

################## PLACEMENT #################
set dut placementHeat_
set fileName ${designPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Placement $fileName

#layout printscreen placement
gui::set_display_controls "Heat Maps/Placement Density" visible true
set psName ${printsPath}/${dut}${::env(DESIGN_NAME)}.png
save_image $psName
puts "Placement done!\n"

################## POWER #################
set dut powerHeat_
set fileName ${designPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Power $fileName
puts "Power done!\n"

################## ROUTING #################
#read_guides $::env(RESULTS_DIR)/route.guide
set dut routingHeat_
set fileName ${designPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Routing $fileName

#layout printscreen Routing
gui::set_display_controls "Heat Maps/Routing Congestion" visible true
set psName ${printsPath}/${dut}${::env(DESIGN_NAME)}.png
save_image $psName
puts "Routing done!\n"

################## IR DROP #################
analyze_power_grid -net VDD
set dut irdropHeat_
set fileName ${designPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap IRDrop $fileName
puts "IR Drop done!\n"


puts "\nExit getLabels.tcl"
exit
