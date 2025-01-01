# micropython
# MIT license
# Copyright (c) 2022 Roman Shevchik goctaprog@gmail.com
"""service class for I/O bus operation"""

from machine import I2C

class BusAdapter:
    """Proxy between I/O bus and device I/O class"""
    def __init__(self, bus):
        self.bus = bus

    def read_register(self, device_addr: int, reg_addr: int, bytes_count: int) -> bytes:
        """reads a value from the sensor register.
        device_addr - the address of the sensor on the bus.
        reg_addr - the address of the register in the sensor address space.
        bytes_count - the size of the value in bytes.
        reads value from sensor register.
        device_addr - address of the sensor on the bus.
        reg_addr - register address in the address space of the sensor"""
        raise NotImplementedError

    def write_register(self, device_addr: int, reg_addr: int, value: [int, bytes, bytearray],
                       bytes_count: int, byte_order: str):
        """writes the data value to the sensor, at the address reg_addr.
        bytes_count - the number of bytes written from value.
        byte_order - the order of the bytes in the value being written.
        writes value data to the sensor, at reg_addr.
        bytes_count - number of bytes written from value.
        byte_order - the order of bytes in the value being written.
        """
        raise NotImplementedError

    def read(self, device_addr, n_bytes: int) -> bytes:
        raise NotImplementedError

    def write(self, device_addr, buf: bytes):
        raise NotImplementedError

class I2cAdapter(BusAdapter):
    def __init__(self, bus: I2C):
        super().__init__(bus)

    def write_register(self, device_addr: int, reg_addr: int, value: [int, bytes, bytearray],
                       bytes_count: int, byte_order: str):
        """writes the data value to the sensor, at the address reg_addr.
        bytes_count - amount of data written
        value - must be of types int, bytes, bytearray"""
        buf = None
        if isinstance(value, int):
            buf = value.to_bytes(bytes_count, byte_order)
        if isinstance(value, (bytes, bytearray)):
            buf = value

        return self.bus.writeto_mem(device_addr, reg_addr, buf)

    def read_register(self, device_addr: int, reg_addr: int, bytes_count: int) -> bytes:
        """reads a value from the sensor register.
        bytes_count - the size of the value in bytes"""
        return self.bus.readfrom_mem(device_addr, reg_addr, bytes_count)

    def read(self, device_addr, n_bytes: int) -> bytes:
        return self.bus.readfrom(device_addr, n_bytes)
    
    def read_buf_from_mem(self, device_addr, mem_addr, buf):
        """Reads from the device with address device_addr into the buffer buf, starting at the address in the device mem_addr.
        The number of bytes read is determined by the length of the buffer buf.
        Reads from device address device_addr into buf, starting at the address in device mem_addr.
        The number of bytes read is determined by the length of the buffer buf"""
        return self.bus.readfrom_mem_into(device_addr, mem_addr, buf)

    def write(self, device_addr, buf: bytes):
        return self.bus.writeto(device_addr, buf)

    def write_buf_to_mem(self, device_addr, mem_addr, buf):
        """Writes all bytes from the buffer buf to the device with the address device_addr.
        The entry starts from the address in the device: mem_addr.
        Writes to device address device_addr all the bytes in buf.
        The entry starts at an address in the device: mem_addr."""
        return self.bus.writeto_mem(device_addr, mem_addr, buf)
