L0:
   j Lmain

L1:
   sw ra,(sp)

L2:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L3:
    lw t1,something   sw t1,something

L4:
   lw t1, something
   lw t2, something
   blt t1,t2,L4
L5:
   j L10

L6:
   lw t1, something
   lw t2, something
   blt t1,t2,L6
L7:
   j L10

L8:
    lw t1,something   sw t1,something

L9:
   j L16

L10:
   lw t1, something
   lw t2, something
   blt t1,t2,L10
L11:
   j L15

L12:
   lw t1, something
   lw t2, something
   blt t1,t2,L12
L13:
   j L15

L14:
    lw t1,something   sw t1,something

L15:
    lw t1,something   sw t1,something

L16:
   lw t1,something
    lw t0,something    sw t1,(t0))L17:
   lw ra,(sp)
   jr ra

L18:
   sw ra,(sp)

L19:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L20:
    lw t1,something   sw t1,something

L21:
   lw t1, something
   lw t2, something
   bgt t1,t2,L21
L22:
   j L25

L23:
   li t1,1
    lw t0,something    sw t1,(t0))L24:
   j L41

L25:
   lw t1, something
   lw t2, something
   bne t1,t2,L25
L26:
   j L30

L27:
   lw t1, something
   lw t2, something
   bne t1,t2,L27
L28:
   j L30

L29:
   li t1,1
    lw t0,something    sw t1,(t0))L30:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L31:
L32:
L33:
L34:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L35:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L36:
L37:
L38:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L39:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L40:
   lw t1,something
    lw t0,something    sw t1,(t0))L41:
   lw ra,(sp)
   jr ra

L42:
   sw ra,(sp)

L43:
   sw ra,(sp)

L44:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L45:
    lw t1,something   sw t1,something

L46:
   lw t1, something
   lw t2, something
   div t3,t1,t2
   sw t3, something

L47:
   lw t1, something
   lw t2, something
   mul t3,t1,t2
   sw t3, something

L48:
   lw t1, something
   lw t2, something
   bne t1,t2,L48
L49:
   j L52

L50:
   li t1,1
    lw t0,something    sw t1,(t0))L51:
   j L53

L52:
   li t1,0
    lw t0,something    sw t1,(t0))L53:
   lw ra,(sp)
   jr ra

L54:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L55:
    lw t1,something   sw t1,something

L56:
   li t1,2
   sw t1,something

L57:
   lw t1, something
   lw t2, something
   bgt t1,t2,L57
L58:
   j L70

L59:
L60:
L61:
L62:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L63:
   lw t1, something
   lw t2, something
   bne t1,t2,L63
L64:
   j L67

L65:
   li t1,0
    lw t0,something    sw t1,(t0))L66:
   j L67

L67:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L68:
    lw t1,something   sw t1,something

L69:
   j L57

L70:
   li t1,1
    lw t0,something    sw t1,(t0))L71:
   lw ra,(sp)
   jr ra

L72:
   sw ra,(sp)

L73:
   sw ra,(sp)

L74:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L75:
    lw t1,something   sw t1,something

L76:
   lw t1, something
   lw t2, something
   mul t3,t1,t2
   sw t3, something

L77:
   lw t1,something
    lw t0,something    sw t1,(t0))L78:
   lw ra,(sp)
   jr ra

L79:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L80:
    lw t1,something   sw t1,something

L81:
L82:
L83:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L84:
L85:
L86:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L87:
   lw t1, something
   lw t2, something
   mul t3,t1,t2
   sw t3, something

L88:
    lw t1,something   sw t1,something

L89:
   lw t1,something
    lw t0,something    sw t1,(t0))L90:
   lw ra,(sp)
   jr ra

L91:
   sw ra,(sp)

L92:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L93:
    lw t1,something   sw t1,something

L94:
   lw t1, something
   lw t2, something
   mul t3,t1,t2
   sw t3, something

L95:
   lw t1, something
   lw t2, something
   bne t1,t2,L95
L96:
   j L99

L97:
   li t1,0
    lw t0,something    sw t1,(t0))L98:
   j L99

L99:
L100:
   lw t1, something
   lw t2, something
   bne t1,t2,L100
L101:
   j L110

L102:
L103:
   lw t1, something
   lw t2, something
   beq t1,t2,L103
L104:
   j L105

L105:
L106:
   lw t1, something
   lw t2, something
   bne t1,t2,L106
L107:
   j L110

L108:
   li t1,1
    lw t0,something    sw t1,(t0))L109:
   j L111

L110:
   lw t1,something
    lw t0,something    sw t1,(t0))L111:
   lw ra,(sp)
   jr ra

Lmain:
   addi sp,sp,framelength
   mv gp,sp

L113:
   li t1,0
   sw t1,something

L114:
L115:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L116:
    lw t1,something   sw t1,something

L117:
   li t1,1600
   sw t1,something

L118:
   lw t1, something
   lw t2, something
   bgt t1,t2,L118
L119:
   j L126

L120:
L121:
L122:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L123:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L124:
    lw t1,something   sw t1,something

L125:
   j L118

L126:
L127:
L128:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L129:
L130:
L131:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L132:
L133:
L134:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L135:
L136:
L137:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L138:
   li t1,1
   sw t1,something

L139:
   lw t1, something
   lw t2, something
   bgt t1,t2,L139
L140:
   j L147

L141:
L142:
L143:
    sw sp, something
    addi sp,sp,framelength
    jal on_a_label
    addi sp,sp, -framelength
L144:
   lw t1, something
   lw t2, something
   addi t3,t1,t2
   sw t3, something

L145:
    lw t1,something   sw t1,something

L146:
   j L139

L147:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L148:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L149:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L150:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L151:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L152:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L153:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L154:
   lw t1, something
   lw t2, something
   sub t3,t1,t2
   sw t3, something

L155:
    lw t1,something   sw t1,something

