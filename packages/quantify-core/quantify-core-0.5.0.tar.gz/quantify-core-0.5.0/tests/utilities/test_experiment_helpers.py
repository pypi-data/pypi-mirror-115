import numpy as np
from qcodes.instrument import Instrument, ManualParameter
import pytest
from quantify_core.utilities.experiment_helpers import (
    create_plotmon_from_historical,
    load_settings_onto_instrument,
)
from quantify_core.data.handling import set_datadir


def test_load_settings_onto_instrument(tmp_test_data_dir):
    """
    Test that we can successfully load the settings of a dummy instrument
    """
    # Always set datadir before instruments
    set_datadir(tmp_test_data_dir)

    def get_func():
        return 20

    tuid = "20210319-094728-327-69b211"

    instr = Instrument("DummyInstrument")

    # A parameter that is both settable and gettable
    instr.add_parameter(
        "settable_param", initial_value=10, parameter_class=ManualParameter
    )
    # A parameter that is only gettable
    instr.add_parameter("gettable_param", set_cmd=False, get_cmd=get_func)
    # A boolean parameter that is True by defualt
    instr.add_parameter(
        "boolean_param", initial_value=True, parameter_class=ManualParameter
    )
    # A parameter which our function will try to set to None
    instr.add_parameter("none_param", initial_value=1, parameter_class=ManualParameter)
    # The snapshot also contains an 'obsolete_param', that is not included here.
    # This represents a parameter which is no longer in the qcodes driver.

    with pytest.warns(
        UserWarning,
        match="DummyInstrument does not possess a parameter obsolete_param. Could not "
        "set parameter.",
    ):
        load_settings_onto_instrument(instr, tuid)

    assert instr.get("IDN") == {
        "vendor": None,
        "model": "DummyInstrument",
        "serial": None,
        "firmware": None,
    }
    assert instr.get("settable_param") == 5
    assert instr.get("gettable_param") == 20
    assert instr.get("none_param") is None
    assert not instr.get("boolean_param")

    instr.close()


def test_create_plotmon_from_historical(tmp_test_data_dir):
    """
    Test for creating a plotmon based on a provided tuid
    """
    set_datadir(tmp_test_data_dir)

    tuid = "20200504-191556-002-4209ee"
    plotmon = create_plotmon_from_historical(tuid)

    curves_dict = plotmon._get_curves_config()
    x = curves_dict[tuid]["x0y0"]["config"]["x"]
    y = curves_dict[tuid]["x0y0"]["config"]["y"]

    x_exp = np.linspace(0, 5, 50)
    y_exp = np.cos(np.pi * x_exp) * -1
    np.testing.assert_allclose(x[:50], x_exp)
    np.testing.assert_allclose(y[:50], y_exp)

    cfg = plotmon._get_traces_config(which="secondary_QtPlot")[0]["config"]
    assert np.shape(cfg["z"]) == (11, 50)
    assert cfg["xlabel"] == "Time"
    assert cfg["xunit"] == "s"
    assert cfg["ylabel"] == "Amplitude"
    assert cfg["yunit"] == "V"
    assert cfg["zlabel"] == "Signal level"
    assert cfg["zunit"] == "V"

    plotmon.close()
