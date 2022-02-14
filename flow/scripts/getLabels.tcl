# Read lef
read_lef $::env(TECH_LEF)
read_lef $::env(SC_LEF)
if {[info exist ::env(ADDITIONAL_LEFS)]} {
  foreach lef $::env(ADDITIONAL_LEFS) {
    read_lef $lef
  }
}

# Read liberty files
source $::env(SCRIPTS_DIR)/read_liberty.tcl

# Determine design stage (1 ... 6)
set design_stage [lindex [split [file tail $::env(DEF_FILE)] "_"] 0]

# Read def
read_def $::env(DEF_FILE)

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
  puts "Loading spef"
  read_spef $::env(RESULTS_DIR)/6_final.spef
} elseif {$design_stage >= 3} {
  puts "Estimating parasitics"
  estimate_parasitics -placement
}

set dut gatesPosition_
set myname ${dut}${::env(DESIGN_NAME)}.csv
set myout [open $myname w]
puts $myout "Name,xMin,yMin,xMax,yMax"
set block [ord::get_db_block]
foreach inst [$block getInsts] { 
  set box [$inst getBBox] 
  puts $myout "[$inst getName], [ord::dbu_to_microns [$box xMin]], [ord::dbu_to_microns [$box yMin]], [ord::dbu_to_microns [$box xMax]], [ord::dbu_to_microns [$box yMax]]" 
}
close $myout

# Cleanup temporary variables
unset sdc_file s design_stage

set dut placementHeat_
set myname ${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Placement $myname

set dut powerHeat_
set myname ${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Power $myname

set dut routingHeat_
set myname ${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap Routing $myname

set dut irdropHeat_
set myname ${dut}${::env(DESIGN_NAME)}.csv
gui::dump_heatmap IRDrop $myname
