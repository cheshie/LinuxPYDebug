def set_hw(address, length, condition):
    # This code MUST be ported to x64

    # length value must be on of: (1,2,4)
    # condition must be in HW_ACCESS, HW_EXECUTE, HW_WRITE
    # checking available slots - only 4 breakpoints at the time

    # enable appropriate flag in the DR7
    # register to set the bp
    regs.dr7 |= 1 << (available * 2)

    # save address of the breakpoint in the free register
    regs.dr0 (...) dr3 = address

    # set bp condition
    context.dr7 |= condition << ((available * 4) + 16)

    # set the length
    context.dr7 |= length << ((available * 4) + 18)
""
    # set process registers here
    # page 61 ghpy