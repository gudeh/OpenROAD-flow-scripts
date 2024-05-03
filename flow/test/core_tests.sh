test/test_helper.sh gcd nangate45 &
test/test_helper.sh aes nangate45 &
test/test_helper.sh tinyRocket nangate45 &
test/test_helper.sh dynamic_node nangate45 &
test/test_helper.sh jpeg nangate45 &
test/test_helper.sh ibex nangate45 &
wait

test/test_helper.sh gcd sky130hs &
test/test_helper.sh ibex sky130hs &
test/test_helper.sh jpeg sky130hs &
test/test_helper.sh riscv32i sky130hs &
test/test_helper.sh coyote_tc sky130hs &
test/test_helper.sh aes sky130hs &
wait

test/test_helper.sh gcd sky130hd &
test/test_helper.sh ibex sky130hd &
test/test_helper.sh jpeg sky130hd &
test/test_helper.sh riscv32i sky130hd &
test/test_helper.sh coyote_tc sky130hd &
test/test_helper.sh aes sky130hd &
wait

test/test_helper .sh aes gf180 &
test/test_helper.sh aes-hybrid gf180 &
test/test_helper.sh ibex gf180 &
test/test_helper.sh jpeg gf180
test/test_helper.sh riscv32i gf180 &
test/test_helper.sh uart-blocks gf180 &
wait

test/test_helper.sh gcd ihp-sg13g2 &
test/test_helper.sh aes ihp-sg13g2 &
test/test_helper.sh ibex ihp-sg13g2 &
test/test_helper.sh jpeg ihp-sg13g2 &
test/test_helper.sh riscv32i ihp-sg13g2 &
test/test_helper.sh spi ihp-sg13g2 &
wait

test/test_helper.sh gcd asap7 &
test/test_helper.sh aes asap7 &
test/test_helper.sh ethmac asap7 &
test/test_helper.sh ibex asap7 &
test/test_helper.sh jpeg asap7 &
test/test_helper.sh uart asap7 &
test/test_helper.sh riscv32i asap7 &
wait

test/test_helper.sh black_parrot nangate45 &
test/test_helper.sh bp_fe_top nangate45 & 
test/test_helper.sh bp_multi_top nangate45 &
wait

test/test_helper.sh swerv nangate45 &
test/test_helper.sh ariane133 nangate45 &
