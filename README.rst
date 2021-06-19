nsrt-mk3-dev
============

Introduction
------------
The NSRT_mk3_Dev is a new variant of the NSRT_mk3 series that introduces an open virtual Com port
communication protocol. That means that the instrument can be used on any platform that has a generic
driver to support the CDC (Communication) USB class. Nowadays most platforms support that class,
including Windows, Mac and Linux.
That instrument is targeted at developers. Because its communication protocol is open, developers can
design their own application supporting the instrument.
In addition to the Com port, the NSRT_mk3_Dev can have an optional USB Audio interface to stream
the actual Audio signal captured by the microphone.

Usage
-----
1. Connect the NSRT mk3 dev to the computer

2. Check the virtual Com port under which it was enumerated:

    a. Windows: WIN + type: Device Manager

       Look for the extra device::

           USB Serial Device (COM20)

       Indicating the device can be found on COM20

    b. Linux: type:: 

            dmesg | grep -i usb
        
       and look for::

           [22339.508035] usb 1-1.2: Product: NSRT_mk3_Dev
           [22339.508044] usb 1-1.2: Manufacturer: Convergence Instruments
           [22339.520711] cdc_acm 1-1.2:1.1: ttyACM0: USB ACM device

       Indicating that the device can be found on /dev/ttyACM0

3. Install the package::

       pip install nsrt-mk3-dev

4. Create a script to access the device::

       import nsrt_mk3_dev

       nsrt = nsrt_mk3_dev.NsrtMk3Dev('COM20')
       model = nsrt.read_model()

       serial_number  = nsrt.read_sn()
       firmware_revision = nsrt.read_fw_rev()
       date_of_birth = nsrt.read_dob()
       date_of_calibration = nsrt.read_doc()
       print(f'Sound level meter model: {model}\n'
             f'serial number: {serial_number}, firmware revision number: {firmware_revision}\n'
             f'manufactured on: {date_of_birth}, calibrated on: {date_of_calibration}')

       leq_level = nsrt.read_leq()
       weighting = nsrt.read_weighting()
       weighted_level = nsrt.read_level()
       print(f'current leq level: {leq_level:0.2f} dB, {weighting} value: {weighted_level:0.2f}')

Test
----
The GIT repo contains a pytest which tests all the API functions. The test_device_parameters testcase will need to be 
updated to the device under test as it reads out device specific data. To execute the test run the following command 
in the GIT repo's root directory::

    pytest tests