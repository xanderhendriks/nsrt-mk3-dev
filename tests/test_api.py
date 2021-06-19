import nsrt_mk3_dev
import time
import pytest


def test_leq(nsrt):
    leq = nsrt.read_leq()

    print(f'leq: {leq}')

    assert 30 < leq < 70


def test_temperature(nsrt):
    temperature = nsrt.read_temperature()

    print(f'temperature: {temperature}')

    assert 15 < temperature < 30


@pytest.mark.parametrize('weighting', [nsrt_mk3_dev.NsrtMk3Dev.Weighting.DB_C, nsrt_mk3_dev.NsrtMk3Dev.Weighting.DB_A, nsrt_mk3_dev.NsrtMk3Dev.Weighting.DB_Z])
def test_weighting(nsrt, weighting):
    nsrt.write_weighting(weighting)
    time.sleep(2)

    level = nsrt.read_level()
    print(f'level: {level}')

    assert 30 < level < 70
    assert nsrt.read_weighting() == weighting


@pytest.mark.parametrize('frequency', [32000, 48000])
def test_frequency(nsrt, frequency):
    nsrt.write_fs(frequency)
    assert nsrt.read_fs() == frequency


def test_frequency_exception(nsrt):
    frequency = 25000
    with pytest.raises(ValueError) as exception_info:
        nsrt.write_fs(frequency)

    assert str(exception_info.value) == f'{frequency} not supported. Value can only be 32000 or 48000'


@pytest.mark.parametrize('tau', [1, 0.5, 0.125])
def test_tau(nsrt, tau):
    nsrt.write_tau(tau)
    assert nsrt.read_tau() == tau


def test_model(nsrt):
    assert nsrt.read_model() == 'NSRT_mk3_Dev_Audio'


def test_device_parameters(nsrt):
    serial_number = nsrt.read_sn()
    firmware_revision = nsrt.read_fw_rev()
    date_of_birth = nsrt.read_dob()
    date_of_calibration = nsrt.read_doc()

    print(f'serial number: {serial_number}, firmware revision number: {firmware_revision}\n'
          f'manufactured on: {date_of_birth}, calibrated on: {date_of_calibration}')

    assert serial_number == 'Anv8jF06W%0XCpFS60J5ND'
    assert firmware_revision == '1.0'
    assert date_of_birth == '2021-06-02 06:53:53'
    assert date_of_calibration == '2021-06-09 04:48:50'


@pytest.mark.parametrize('user_id', ['NX Solutions', 'Convergence'])
def test_user_id(nsrt, user_id):
    nsrt.write_user_id(user_id)

    assert nsrt.read_user_id() == user_id


def test_user_id_exception(nsrt):
    user_id = 32 * 'c'
    with pytest.raises(ValueError) as exception_info:
        nsrt.write_user_id(user_id)

    assert str(exception_info.value) == 'Maximum length for the user id is 31 characters'
