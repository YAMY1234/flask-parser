addiu $sp,$zero,0x10018000
or $fp,$sp,$zero
jal  main
jal  end
add $7,$zero,1
add $v0,$zero,$7
jr $ra
add $8,$zero,1
add $a2,$zero,0
sgt $9,$8,$a2
bgt $9,$zero,l1
j l2
l1:
add $10,$zero,2
j l3
l2:
add $10,$zero,1
l3:
sub $sp,$sp,4
sw $ra,0($sp)
jal  f1
lw $ra,0($sp)
add $sp,$sp,4
add $11,$zero,$v0
add $v0,$zero,0
jr $ra
end: