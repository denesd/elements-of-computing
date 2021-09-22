import filecmp
import tempfile

from assembler.assembler import main


def test_max_assembler():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        main(["tests/data/Max.asm", temp.name])
        assert filecmp.cmp("tests/data/Max.hack", temp.name, shallow=False)
