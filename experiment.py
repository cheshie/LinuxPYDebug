from sys import argv

# 1
from elftools.elf.elffile import ELFFile


def load_maps(pid):
    handle = open('/proc/{}/maps'.format(pid), 'r')
    output = []
    for line in handle:
        line = line.strip()
        parts = line.split()
        (addr_start, addr_end) = map(lambda x: int(x, 16), parts[0].split('-'))
        permissions = parts[1]
        offset = int(parts[2], 16)
        device_id = parts[3]
        inode = parts[4]
        map_name = parts[5] if len(parts) > 5 else ''

        mapping = {
            'addr_start':  addr_start,
            'addr_end':    addr_end,
            'size':        addr_end - addr_start,
            'permissions': permissions,
            'offset':      offset,
            'device_id':   device_id,
            'inode':       inode,
            'map_name':    map_name
        }
        output.append(mapping)

    handle.close()
    return output


# maps = load_maps(argv[1])

# print(maps)

# 2
# process_libc = list(filter(
#     lambda x: '/libc-' in x['map_name'] and 'r-xp' == x['permissions'],
#     maps))
#
# if not process_libc:
#     print ("Couldn't locate libc shared object in this process.")
#     exit(1)

# # 3
# libc_base     = process_libc[0]['addr_start']
# libc_location = process_libc[0]['map_name']
# print(libc_location)
# exit()
# libc_elf = ELFFile(open("hello_loop", 'rb'))
#
# # 4
# print(libc_elf.get_section_by_name('.text').structs.Elf_addr)
# exit()
#
# __libc_dlopen_mode = list(filter(
#     lambda x: x.name == "printer",
#     libc_elf.get_section_by_name('.text').iter_symbols())
# )

from ctypes import CDLL
libc = CDLL('libc.so.6')
print(libc.dlopen())

# if not __libc_dlopen_mode:
#     print ("Couldn't find __libc_dlopen_mode in libc")
#     exit(1)
#
# print(__libc_dlopen_mode)
#
# # 5
# __libc_dlopen_mode = __libc_dlopen_mode[0].entry['st_value']
# print ("libc base @", hex(libc_base))
# print ("dlopen_mode offset @", hex(__libc_dlopen_mode))
# __libc_dlopen_mode = __libc_dlopen_mode + libc_base
# print ("function pointer @", __libc_dlopen_mode)