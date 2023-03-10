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
  
## Cleanup temporary variables
#  unset sdc_file s design_stage


################################################################
################# My additions from gui.tcl #####################
################################################################
set dirPath congestionPrediction/${::env(DESIGN_NAME)}
file mkdir $dirPath

#for printScreens of layouts
set dirPath2 congestionPrediction/layoutPrints
file mkdir $dirPath2

#moving yosys outpupt files (it doesnt have access to design names)
file rename -force congestionPrediction/DGLedges.csv congestionPrediction/${::env(DESIGN_NAME)}/DGLedges.csv
file rename -force congestionPrediction/DGLcells.csv congestionPrediction/${::env(DESIGN_NAME)}/DGLcells.csv

#Write the position of each node
set dut gatesPosition_
set myname ${dirPath}/${dut}${::env(DESIGN_NAME)}.csv
set myout [open $myname w]
puts $myout "Name,xMin,yMin,xMax,yMax"
set block [ord::get_db_block]
foreach inst [$block getInsts] { 
  set box [$inst getBBox] 
  puts $myout "[$inst getName], [ord::dbu_to_microns [$box xMin]], [ord::dbu_to_microns [$box yMin]], [ord::dbu_to_microns [$box xMax]], [ord::dbu_to_microns [$box yMax]]" 
}
close $myout

#Write a CSV for each heat value
set dut placementHeat_
set myname ${dirPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Placement $myname

#layout printscreen
set psname ${dirPath2}/${dut}${::env(DESIGN_NAME)}
save_image psname

set dut powerHeat_
set myname ${dirPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Power $myname

read_guides $::env(RESULTS_DIR)/route.guide
set dut routingHeat_
set myname ${dirPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Routing $myname

analyze_power_grid -net VDD
set dut irdropHeat_
set myname ${dirPath}/${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap IRDrop $myname

# Cleanup temporary variables
unset sdc_file s design_stage

puts "\nExit getLabels.tcl"
exit

}
