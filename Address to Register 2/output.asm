
firmware.elf:     file format elf32-avr


Disassembly of section .text:

00000000 <__vectors>:
   0:	0c 94 34 00 	jmp	0x68	; 0x68 <__ctors_end>
   4:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
   8:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
   c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  10:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  14:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  18:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  1c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  20:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  24:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  28:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  2c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  30:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  34:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  38:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  3c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  40:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  44:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  48:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  4c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  50:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  54:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  58:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  5c:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  60:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>
  64:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__bad_interrupt>

00000068 <__ctors_end>:
  68:	11 24       	eor	r1, r1
  6a:	1f be       	out	0x3f, r1	; 63
  6c:	cf ef       	ldi	r28, 0xFF	; 255
  6e:	d8 e0       	ldi	r29, 0x08	; 8
  70:	de bf       	out	0x3e, r29	; 62
  72:	cd bf       	out	0x3d, r28	; 61
  74:	0e 94 40 00 	call	0x80	; 0x80 <main>
  78:	0c 94 64 00 	jmp	0xc8	; 0xc8 <_exit>

0000007c <__bad_interrupt>:
  7c:	0c 94 00 00 	jmp	0	; 0x0 <__vectors>

00000080 <main>:
  80:	cf 93       	push	r28
  82:	df 93       	push	r29
  84:	00 d0       	rcall	.+0      	; 0x86 <main+0x6>
  86:	00 d0       	rcall	.+0      	; 0x88 <main+0x8>
  88:	cd b7       	in	r28, 0x3d	; 61
  8a:	de b7       	in	r29, 0x3e	; 62
  8c:	20 9a       	sbi	0x04, 0	; 4
  8e:	21 e0       	ldi	r18, 0x01	; 1
  90:	85 b1       	in	r24, 0x05	; 5
  92:	82 27       	eor	r24, r18
  94:	85 b9       	out	0x05, r24	; 5
  96:	19 82       	std	Y+1, r1	; 0x01
  98:	1a 82       	std	Y+2, r1	; 0x02
  9a:	1b 82       	std	Y+3, r1	; 0x03
  9c:	1c 82       	std	Y+4, r1	; 0x04
  9e:	89 81       	ldd	r24, Y+1	; 0x01
  a0:	9a 81       	ldd	r25, Y+2	; 0x02
  a2:	ab 81       	ldd	r26, Y+3	; 0x03
  a4:	bc 81       	ldd	r27, Y+4	; 0x04
  a6:	80 3a       	cpi	r24, 0xA0	; 160
  a8:	96 48       	sbci	r25, 0x86	; 134
  aa:	a1 40       	sbci	r26, 0x01	; 1
  ac:	b1 05       	cpc	r27, r1
  ae:	80 f7       	brcc	.-32     	; 0x90 <main+0x10>
  b0:	89 81       	ldd	r24, Y+1	; 0x01
  b2:	9a 81       	ldd	r25, Y+2	; 0x02
  b4:	ab 81       	ldd	r26, Y+3	; 0x03
  b6:	bc 81       	ldd	r27, Y+4	; 0x04
  b8:	01 96       	adiw	r24, 0x01	; 1
  ba:	a1 1d       	adc	r26, r1
  bc:	b1 1d       	adc	r27, r1
  be:	89 83       	std	Y+1, r24	; 0x01
  c0:	9a 83       	std	Y+2, r25	; 0x02
  c2:	ab 83       	std	Y+3, r26	; 0x03
  c4:	bc 83       	std	Y+4, r27	; 0x04
  c6:	eb cf       	rjmp	.-42     	; 0x9e <main+0x1e>

000000c8 <_exit>:
  c8:	f8 94       	cli

000000ca <__stop_program>:
  ca:	ff cf       	rjmp	.-2      	; 0xca <__stop_program>
