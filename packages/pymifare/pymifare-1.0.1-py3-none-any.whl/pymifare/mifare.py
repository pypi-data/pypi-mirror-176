import os,sys,platform

#print(__name__)
#if __name__ == "mifare":
#    #import checkpathmodule
#    import mifaredef
#else:
#    # pymifare.mifare is expected
#    #from . import checkpathmodule
#    from . import mifaredef

try:
    import mifaredef
except:
    from . import mifaredef


modulepath = os.path.dirname(mifaredef.__file__)
sys.path.insert(0, modulepath)
#print("addded path",modulepath)


from pyspv1.serialcommspv1 import SerialCommSpv1
from pyspv1.spsc import EnumLogFilter
from globalvar import spv1handler
from mifareasynchandler import MifareAsyncHandler


def create_mifare_serial_comm(DefaultSerialTimeOut = 0.5,AsyncReceive=True,async_card_read_callback = None,vertical_log = False,log_filter = EnumLogFilter.ALL,external_dll_path=None, instance_id=1):
    """ Create and returns SerialSpv1 object and initialize system including dll """
    """ Example platform.platform() outputs:

    Windows 10:
    Windows-10-10.0.14393-SP0

    Raspberry Pi:
    Linux-4.4.38-v7+-armv71-with-debian-8.0

    Debian 64 bit ( Virtual Box)
    Linux-3.16.0-4-amd64-x86_64-with-debian-8.3

    Ubuntu 16.04 
    Linux-4.4.0-66-generic-i686-with-Ubuntu-16.04-xenial
    """

    # Check armv first; as Raspberry and Debian both have Debian string.
    if external_dll_path == None:
        _platform_string = platform.platform().lower()
        _architecture_string = platform.architecture()[0]
        # !!! Attention comparision msut be lower case!!
        if "win".lower() in _platform_string:
            # Tested on 64 bit windows 10,(python installed version is 32 bit)
            # Windows-10-10.0.14393-SP0
            spv1handler.initialize(path=modulepath + "//spv1mifare_win.dll",log_filter=log_filter,vertical_log=vertical_log)
        elif "armv7".lower() in _platform_string:
            # Tested with Raspberry Pi 3
            # Linux-4.4.38-v7+-armv71-with-debian-8.0
            # Beaglebone may work too as well. Not tested
            spv1handler.initialize(path=modulepath + "//spv1mifare_armv7l.so",log_filter=log_filter,vertical_log=vertical_log)
        elif "Linux".lower() in _platform_string:
            if "x86_64" in _platform_string:
                spv1handler.initialize(path=modulepath + "//spv1mifare_linux_x86_64.so",log_filter=log_filter,vertical_log=vertical_log)
            else:
                # This dll is not available.
                print("Required dll for your platform is available upon request.")
        else:
            spv1handler.initialize(path=external_dll_path,log_filter=log_filter,vertical_log=vertical_log)
    else:
        spv1handler.initialize(path=external_dll_path, log_filter=log_filter, vertical_log=vertical_log)

    mifare_async_handler = MifareAsyncHandler(spv1handler, async_card_read_callback=async_card_read_callback)
    mifare_serial_comm = SerialCommSpv1(spv1handler, mifare_async_handler, DefaultSerialTimeOut, AsyncReceive, instance_id=instance_id)
    return mifare_serial_comm


