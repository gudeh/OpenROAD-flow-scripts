puts "\nRunning getFeatures.tcl"
puts "::env(RESULTS_DIR)-> $::env(RESULTS_DIR)"

yosys -import
read_liberty -lib {*}$::env(DONT_USE_LIBS)
read_verilog $::env(RESULTS_DIR)/1_1_yosys.v
hierarchy -auto-top
hello_world
puts "\nExit getFeatures.tcl"
exit
