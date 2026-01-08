test/test_helper.sh tinyRocket nangate45 &
test/test_helper.sh microwatt sky130hd &
test/test_helper.sh swerv_wrapper nangate45 &
test/test_helper.sh aes-block asap7 &
wait
test/test_helper.sh bp_fe_top nangate45 &
test/test_helper.sh bp_quad nangate45 &
test/test_helper.sh bp_be_top nangate45 &
wait
test/test_helper.sh black_parrot nangate45 &
test/test_helper.sh mempool_group nangate45 &
test/test_helper.sh mock-array asap7 &
wait
test/test_helper.sh ariane133 nangate45 &
test/test_helper.sh ariane136 nangate45 &
test/test_helper.sh uart-blocks gf180 &
wait
test/test_helper.sh riscv32i asap7 &
test/test_helper.sh chameleon_hier sky130hd &
test/test_helper.sh bp_multi_top nangate45 &