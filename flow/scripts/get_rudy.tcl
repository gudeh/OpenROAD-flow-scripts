source scripts/gui.tcl
gui::dump_heatmap Routing "$::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-grt.csv"
gui::set_display_controls "Heat Maps/Routing Congestion" visible true
set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-grt.png
save_image -width 3000 $psName

gui::dump_heatmap RUDY    "$::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-rudy.csv"
gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
set psName $::env(REPORTS_DIR)/$::env(DESIGN_NAME)-$::env(PLATFORM)-rudy.png
save_image -width 3000 $psName
exit
