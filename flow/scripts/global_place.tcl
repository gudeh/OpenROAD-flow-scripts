utl::set_metrics_stage "globalplace__{}"
source $::env(SCRIPTS_DIR)/load.tcl
erase_non_stage_variables place
load_design 3_2_place_iop.odb 2_floorplan.sdc

set_dont_use $::env(DONT_USE_CELLS)

if { $::env(GPL_TIMING_DRIVEN) } {
  remove_buffers
}

# Do not buffer chip-level designs
# by default, IO ports will be buffered
# to not buffer IO ports, set environment variable
# DONT_BUFFER_PORT = 1
if { ![env_var_exists_and_non_empty FOOTPRINT] } {
  if { !$::env(DONT_BUFFER_PORTS) } {
    puts "Perform port buffering..."
    buffer_ports
  }
}

set global_placement_args {}

# Parameters for routability mode in global placement
# append_env_var global_placement_args GPL_ROUTABILITY_DRIVEN -routability_driven 0
# lappend global_placement_args -routability_max_inflation_ratio 4
lappend global_placement_args -enable_routing_congestion


# Parameters for timing driven mode in global placement
if { $::env(GPL_TIMING_DRIVEN) } {
  lappend global_placement_args {-timing_driven}
  if { [info exists ::env(GPL_KEEP_OVERFLOW)] } {
    lappend global_placement_args -keep_resize_below_overflow $::env(GPL_KEEP_OVERFLOW)
  }
}

proc do_placement { global_placement_args } {
  set all_args [concat [list -density [place_density_with_lb_addon] \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT)] \
    $global_placement_args]

  lappend all_args {*}[env_var_or_empty GLOBAL_PLACEMENT_ARGS]

  log_cmd global_placement {*}$all_args
}

set result [catch { do_placement $global_placement_args } errMsg]
if { $result != 0 } {
  write_db $::env(RESULTS_DIR)/3_3_place_gp-failed.odb
  error $errMsg
}

estimate_parasitics -placement

if { $::env(CLUSTER_FLOPS) } {
  cluster_flops
  estimate_parasitics -placement
}

report_metrics 3 "global place" false false

write_db $::env(RESULTS_DIR)/3_3_place_gp.odb


# from save_images.tcl
source $::env(SCRIPTS_DIR)/util.tcl
gui::save_display_controls
set height [[[ord::get_db_block] getBBox] getDY]
set height [ord::dbu_to_microns $height]
set resolution [expr $height / 1000]
set markerdb [[ord::get_db_block] findMarkerCategory DRC]
if { $markerdb != "NULL" && [$markerdb getMarkerCount] > 0 } {
  gui::select_marker_category $markerdb
}
gui::clear_highlights -1
gui::clear_selections
gui::fit
# Setup initial visibility to avoid any previous settings
gui::set_display_controls "*" visible false
gui::set_display_controls "Layers/*" visible true
gui::set_display_controls "Nets/*" visible true
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Shape Types/*" visible true
gui::set_display_controls "Misc/Instances/*" visible false
gui::set_display_controls "Misc/Instances/Pins" visible true
gui::set_display_controls "Misc/Instances/Blockages" visible true
gui::set_display_controls "Misc/Scale bar" visible true
gui::set_display_controls "Misc/Highlight selected" visible true
gui::set_display_controls "Misc/Detailed view" visible true
gui::clear_highlights -1
gui::clear_selections

# The routing congestion view
gui::set_display_controls "Instances/*" visible true
gui::set_display_controls "Instances/Physical/*" visible false
gui::set_display_controls "Nets/*" visible false
gui::set_display_controls "Heat Maps/Routing Congestion" visible true

save_image -resolution $resolution $::env(REPORTS_DIR)/3_3_routing_congestion.webp

gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
save_image -resolution $resolution $::env(REPORTS_DIR)/3_3_rudy.webp

gui::restore_display_controls