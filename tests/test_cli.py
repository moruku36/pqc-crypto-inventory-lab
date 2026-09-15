import pytest

from pqc_inventory.cli import main


def test_default_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "PQC Crypto Inventory Lab" in capsys.readouterr().out


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as result:
        main(["--version"])
    assert result.value.code == 0
    assert "pqc-scan 0.1.0" in capsys.readouterr().out


def test_unknown_option() -> None:
    with pytest.raises(SystemExit) as result:
        main(["--not-a-valid-option"])
    assert result.value.code == 2
