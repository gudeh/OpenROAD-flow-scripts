source scripts/my_gui.tcl
# $design_stage defined at gui.tcl

gui::load_drc $::env(REPORTS_DIR)/5_route_drc.rpt-5.rpt
set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-DRC.png
save_image -width 3000 $psName

gui::dump_heatmap Routing "$::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-grt.csv"
gui::set_display_controls "Heat Maps/Routing Congestion" visible true
set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-grt.png
save_image -width 3000 $psName

gui::dump_heatmap RUDY    "$::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-rudy.csv"
gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-rudy.png
save_image -width 3000 $psName

unset sdc_file s design_stage
exit
