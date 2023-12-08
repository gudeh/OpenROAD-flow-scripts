source scripts/gui.tcl
gui::dump_heatmap Routing "reports/evaluateRUDY/$::env(DESIGN_NAME)-$::env(PLATFORM)-grt.csv"
gui::set_display_controls "Heat Maps/Routing Congestion" visible true
set psName reports/evaluateRUDY/$::env(DESIGN_NAME)-$::env(PLATFORM)-grt.png
save_image $psName

gui::dump_heatmap RUDY    "reports/evaluateRUDY/$::env(DESIGN_NAME)-$::env(PLATFORM)-rudy.csv"
gui::set_display_controls "Heat Maps/Estimated Congestion (RUDY)" visible true
set psName reports/evaluateRUDY/$::env(DESIGN_NAME)-$::env(PLATFORM)-rudy.png
save_image $psName
exit
