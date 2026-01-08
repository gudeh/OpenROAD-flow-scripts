source $::env(SCRIPTS_DIR)/load.tcl
erase_non_stage_variables place
load_design 2_floorplan.odb 2_floorplan.sdc

if { [env_var_exists_and_non_empty FLOORPLAN_DEF] } {
  puts "FLOORPLAN_DEF is set. Skipping global placement without IOs"
} elseif { [all_pins_placed] } {
  puts "All pins are placed. Skipping global placement without IOs"
} else {
 # global_placement_debug -generate_images -pause 5000 -update 5000
  # set_debug_level GPL init 1
 # set_debug_level GPL debugPlots 1

  log_cmd global_placement -skip_io \
    -pad_left $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    -pad_right $::env(CELL_PAD_IN_SITES_GLOBAL_PLACEMENT) \
    {*}[env_var_or_empty GLOBAL_PLACEMENT_ARGS]
}

write_db $::env(RESULTS_DIR)/3_1_place_gp_skip_io.odb
