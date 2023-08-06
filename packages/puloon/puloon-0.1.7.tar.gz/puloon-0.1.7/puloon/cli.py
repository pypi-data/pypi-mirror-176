from pathlib import Path
from typing import Optional

import typer
from serial import Serial, SerialException

from puloon import __app_name__, __version__
from .lcdm4000 import PuloonException, PuloonLCDM4000

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


class PuloonExceptionHandler:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val: tuple, exc_tb):
        if exc_type and issubclass(exc_type, PuloonException):
            typer.echo(repr(exc_val))
            raise typer.Abort()
        if exc_type and issubclass(exc_type, (AssertionError, SerialException, PuloonException)):
            typer.echo(exc_val)
            raise typer.Abort()


PortArg = typer.Argument(
    ...,
    exists=True,
    dir_okay=False,
    help="Serial port path",
)


@app.command(name='reset')
def _reset(port: Path = PortArg) -> None:
    """
    The reset will cause the dispenser reset by software. Therefore, there is no response for this command.
    (Cf.) When RESET is transmitted, it would take 2 seconds for dispenser to initialize all status.
    Therefore, the next command would be sent after the initialization.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.reset())


@app.command(name='status')
def _status(port: Path = PortArg) -> None:
    """This command shows the current sensor status and the configuration of cassette in the top position."""
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.status())


@app.command(name='purge')
def _purge(port: Path = PortArg) -> None:
    """
    PURGE will cause the dispenser to purge the transport of all bills from four cassettes and
    to move the bills in the path to the reject tray. This command will not be required for normal operation.
    However, in case of abnormal termination such as sudden power-off by external cause,
    the command will be useful to remove the notes.
    A successful PURGE operation will move any bills in the transport to the reject tray but
    if the note would be left in the EXIT area, it may be dispensed.

    PURGE will perform the repetitive routine of FORWARD/BACKWARD FEED itself and cause the damage to notes.
    It will not recover errors completely by JAM or already terminated DISP (dispense) command.
    Therefore, it is recommended to use carefully.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.purge())


Qty1Option = typer.Option(
    0, "--qty1", "-q1", min=0, max=40, help="The number of bills to be dispensed from cassette type1"
)
Qty2Option = typer.Option(
    0, "--qty2", "-q2", min=0, max=40, help="The number of bills to be dispensed from cassette type2"
)
Qty3Option = typer.Option(
    0, "--qty3", "-q3", min=0, max=40, help="The number of bills to be dispensed from cassette type3"
)
Qty4Option = typer.Option(
    0, "--qty4", "-q4", min=0, max=40, help="The number of bills to be dispensed from cassette type4"
)
To1Option = typer.Option(
    False, "--to1", "-t1", help="If timeout value is used"
)
To2Option = typer.Option(
    0, "--to2", "-t2", min=0, max=9, help="If  timeout value used, the value is 0~9"
)


@app.command(name='dispense')
def _dispense(qty1: int = Qty1Option, qty2: int = Qty2Option, qty3: int = Qty3Option, qty4: int = Qty4Option,
              to1: bool = To1Option, to2: int = To2Option, port: Path = PortArg) -> None:
    """
    The command will cause to dispenser the requested number of notes from the requested cassette.
    It will check thickness and length of notes, which are individually referred to the specified OPACITY and LENGTH,
    and then decide whether the notes are dispensed or rejected. During the process,
    other parameters such as the required distance between notes and
    the skew of notes will give influence on dispensing and rejecting.

    The requested dispensing number of notes at maximum should not be over 100 sheets.
    """
    if sum((qty1, qty2, qty3, qty4)) == 0:
        raise typer.Exit()
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.dispense(qty1, qty2, qty3, qty4, to1, to2))


@app.command(name='test-dispense')
def _test_dispense(qty1: int = Qty1Option, qty2: int = Qty2Option, qty3: int = Qty3Option, qty4: int = Qty4Option,
                   to1: bool = To1Option, to2: int = To2Option, port: Path = PortArg) -> None:
    """
    The command will cause to reject the specified number of notes from the cassette to the reject tray.
    All the specified notes will move into the reject tray.

    The requested dispensing number of notes at maximum should not be over 100 sheets.
    """
    if sum((qty1, qty2, qty3, qty4)) == 0:
        raise typer.Exit()
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.test_dispense(qty1, qty2, qty3, qty4, to1, to2))


@app.command(name='last-status')
def _last_status(port: Path = PortArg) -> None:
    """
    The command will request to resend the results to the last operation commands
    such as PURGE, DISPENSE and TEST DISPENSE.
    Therefore, it is effective only when the prior operation was performed.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.last_status())


@app.command(name='sensor-diagnostics')
def _sensor_diagnostics(
        pos: int = typer.Option(
            0, "--pos", "-p", min=1, max=4, help="The Designated Cassette for Dispensing (1: Top, ... 4: Bottom)"
        ),
        port: Path = PortArg
) -> None:
    """
    The command will cause to dispense 5 notes from the designated cassette as if “TEST DISPENSE” will do.
    The notes are moved to reject tray and the measured OPACITY, LENGTH and SOLENOID TIME of the last note is returned.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.sensor_diagnostics(pos))


@app.command(name='set-bill-opacities')
def _set_bill_opacities(
        opac1_high: int = typer.Option(
            0, "--opac1-high", "-o1h", min=0, max=15, help="The opacity of bills in top cassette"
        ),
        opac1_low: int = typer.Option(
            0, "--opac1-low", "-o1l", min=0, max=15, help="The opacity of bills in top cassette"
        ),
        opac2_high: int = typer.Option(
            0, "--opac2-high", "-o2h", min=0, max=15, help="The opacity of bills in second top cassette"
        ),
        opac2_low: int = typer.Option(
            0, "--opac2-low", "-o2l", min=0, max=15, help="The opacity of bills in second top cassette"
        ),
        opac3_high: int = typer.Option(
            0, "--opac3-high", "-o3h", min=0, max=15, help="The opacity of bills in third top cassette"
        ),
        opac3_low: int = typer.Option(
            0, "--opac3-low", "-o3l", min=0, max=15, help="The opacity of bills in third top cassette"
        ),
        opac4_high: int = typer.Option(
            0, "--opac4-high", "-o4h", min=0, max=15, help="The opacity of bills in bottom cassette"
        ),
        opac4_low: int = typer.Option(
            0, "--opac4-low", "-o4l", min=0, max=15, help="The opacity of bills in bottom cassette"
        ),
        port: Path = PortArg
) -> None:
    """
    The command is used to save the reference value in order to detect double notes.
    Each opacity value can be saved from 0x00 to 0xFF. The value, 0x00 means to maintain current data.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used.
    However, when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved value of OPACITY when it is turned on.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.set_bill_opacities(
                opac1_high, opac1_low, opac2_high, opac2_low,
                opac3_high, opac3_low, opac4_high, opac4_low
            ))


@app.command(name='reset-bill-opacities', deprecated=True)
def _reset_bill_opacities(port: Path = PortArg) -> None:
    """
    The command is used to reset the reference value in order to detect double notes.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.set_bill_opacities())


@app.command(name='get-bill-opacities')
def _get_bill_opacities(port: Path = PortArg) -> None:
    """The command will get the OPACITY data from each cassette."""
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.get_bill_opacities())


@app.command(name='set-bill-dispense-order')
def _set_bill_dispense_order(
        order1: int = typer.Option(
            1, "--order1", "-o1", min=1, max=4, help="The cassette location (type) that is first to be picked up"
        ),
        order2: int = typer.Option(
            2, "--order2", "-o2", min=1, max=4, help="The cassette location (type) that is second to be picked up"
        ),
        order3: int = typer.Option(
            3, "--order3", "-o3", min=1, max=4, help="The cassette location (type) that is third to be picked up"
        ),
        order4: int = typer.Option(
            4, "--order4", "-o4", min=1, max=4, help="The cassette location (type) that is last to be picked up"
        ),
        port: Path = PortArg
) -> None:
    """
    The command will define the bill dispense order from multi-cassettes.
    The default order is to pick bills from top cassette first, then second cassette and so on.
    The invalid assignment of parameter will cause an error and not be saved.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used. However,
    when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved bill dispenser order when it is turned on.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.set_bill_dispense_order(order1, order2, order3, order4))


@app.command(name='get-bill-dispense-order')
def _get_bill_dispense_order(port: Path = PortArg) -> None:
    """The command will get the bill dispense order data."""
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.get_bill_dispense_order())


@app.command(name='set-bill-lengths')
def _set_bill_lengths(
        leng1_high: int = typer.Option(
            0, "--leng1-high", "-l1h", min=0, max=15, help="The length of bills in top cassette"
        ),
        leng1_low: int = typer.Option(
            0, "--leng1-low", "-l1l", min=0, max=15, help="The length of bills in top cassette"
        ),
        leng2_high: int = typer.Option(
            0, "--leng2-high", "-l2h", min=0, max=15, help="The length of bills in second top cassette"
        ),
        leng2_low: int = typer.Option(
            0, "--leng2-low", "-l2l", min=0, max=15, help="The length of bills in second top cassette"
        ),
        leng3_high: int = typer.Option(
            0, "--leng3-high", "-l3h", min=0, max=15, help="The length of bills in third top cassette"
        ),
        leng3_low: int = typer.Option(
            0, "--leng3-low", "-l3l", min=0, max=15, help="The length of bills in third top cassette"
        ),
        leng4_high: int = typer.Option(
            0, "--leng4-high", "-l4h", min=0, max=15, help="The length of bills in bottom cassette"
        ),
        leng4_low: int = typer.Option(
            0, "--leng4-low", "-l4l", min=0, max=15, help="The length of bills in bottom cassette"
        ),
        port: Path = PortArg
) -> None:
    """
    The command is used to save the reference value in order to detect double notes.
    Each length value can be saved from 0x00 to 0xFF. The value, 0x00 means to maintain current data.
    When the data is changed, it will be saved in the memory of EEPROM and then efficient for the next transaction.
    In case of power on/off, the value continues to be used. However,
    when the electricity trouble causes the saved data damaged (wrong check sum on EEPROM),
    the criterion is set to initial value again.
    Therefore, it is recommended for user to check the value of the saved value of LENGTH when it is turned on.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.set_bill_lengths(
                leng1_high, leng1_low, leng2_high, leng2_low,
                leng3_high, leng3_low, leng4_high, leng4_low
            ))


@app.command(name='reset-bill-lengths', deprecated=True)
def _reset_bill_lengths(port: Path = PortArg) -> None:
    """
    The command is used to reset the reference value in order to detect double notes.
    """
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.set_bill_lengths())


@app.command(name='get-bill-lengths')
def _get_bill_lengths(port: Path = PortArg) -> None:
    """The command will get to saved length data for each cassette."""
    with PuloonExceptionHandler():
        with Serial(str(port.resolve())) as serial:
            puloon = PuloonLCDM4000(serial)
            typer.echo(puloon.get_bill_lengths())
