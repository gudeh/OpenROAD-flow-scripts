source scripts/open.tcl

gui::dump_heatmap RUDY "$::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(my_design_name)-stg$::env(STAGE)-rudy.csv"
gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
set psName $::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(my_design_name)-stg$::env(STAGE)-rudy.png
save_image -width 3000 $psName

# gui::dump_heatmap Routing "$::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(my_design_name)-stg$::env(STAGE)-grt.csv"
# gui::set_display_controls "Heat Maps/Routing Congestion" visible true
# set psName $::env(REPORTS_DIR)/$::env(PLATFORM)-$::env(my_design_name)-stg$::env(STAGE)-grt.png
# save_image -width 3000 $psName

exit

