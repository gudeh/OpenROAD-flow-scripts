puts "\nRunning getFeatures.tcl"
puts "::env(RESULTS_DIR)-> $::env(RESULTS_DIR)"
puts "::env(DONT_USE_LIBS)-> $::env(DONT_USE_LIBS)"

#The tcl command 'yosys -import' can be used to import all yosys commands directly as tcl commands to the tcl shell.
yosys -import
read_liberty -lib {*}$::env(DONT_USE_LIBS)
#read_verilog $::env(RESULTS_DIR)/1_1_yosys.v
#read_verilog $::env(RESULTS_DIR)/1_synth.v
read_verilog $::env(RESULTS_DIR)/6_final.v
hierarchy -auto-top
hello_world
#show
puts "\nExit getFeatures.tcl"
exit
