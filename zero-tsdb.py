#!/usr/bin/env python3
import sys, argparse
def show_hex_dump(data, offset, length):
    chunk = data[offset:offset+length]
    print(f"\033[1;36m[Hex Dump] Offset 0x{offset:08x}:\033[0m")
    for i in range(0, len(chunk), 16):
        sub = chunk[i:i+16]
        hex_str = ' '.join(f"{b:02x}" for b in sub)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in sub)
        print(f"\033[33m0x{offset+i:08x}\033[0m  {hex_str:<48}  |{ascii_str}|")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arena-size', type=int, default=1048576, help='Size of memory arena in bytes (default 1MB)')
    args = parser.parse_args()
    
    print("\033[1;34m=== V3 SYSTEMS & KERNEL MEMORY ENGINE ===\033[0m")
    arena = bytearray(args.arena_size)
    print(f"\033[1;32m[Kernel] Allocated {args.arena_size} bytes in user-space.\033[0m\n")
    
    while True:
        try:
            cmd = input("\033[1;32msys> \033[0m").strip().split()
            if not cmd: continue
            if cmd[0] in ('exit', 'quit'): break
            
            if cmd[0] == 'write' and len(cmd) >= 3:
                offset = int(cmd[1])
                data = ' '.join(cmd[2:]).encode('utf-8')
                arena[offset:offset+len(data)] = data
                print(f"\033[1;32m[Success] Wrote {len(data)} bytes to offset {offset}.\033[0m")
            elif cmd[0] == 'read' and len(cmd) == 3:
                show_hex_dump(arena, int(cmd[1]), int(cmd[2]))
            else:
                print("Commands: write <offset> <string>, read <offset> <length>, exit")
        except Exception as e:
            print(f"\033[1;31m[Error]: {e}\033[0m")
if __name__ == '__main__': main()
