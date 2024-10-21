source scripts/my_open.tcl
# $design_stage defined at gui.tcl

#gui::load_drc $::env(REPORTS_DIR)/5_route_drc.rpt-5.rpt
#set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-DRC.png
#save_image -width 3000 $psName

gui::dump_heatmap Placement "$::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(DESIGN_NAME)-stg$::env(STAGE)-Pdensity.csv"
gui::set_display_controls "Heat Maps/Placement Density" visible true
set psName $::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(DESIGN_NAME)-stg$::env(STAGE)-Pdensity.png
save_image -width 3000 $psName

# gui::dump_heatmap RUDY    "$::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-rudy.csv"
# gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
# set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-stg$design_stage-rudy.png
# save_image -width 3000 $psName

unset my_design_stage
exit
