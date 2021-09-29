import filecmp
import tempfile

from assembler.assembler import main


def test_max_assembler():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        main(["tests/data/Max.asm", "--output", temp.name])
        assert filecmp.cmp("tests/data/Max.hack", temp.name, shallow=False)


def test_add_assembler():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        main(["tests/data/Add.asm", "--output", temp.name])
        assert filecmp.cmp("tests/data/Add.hack", temp.name, shallow=False)


def test_rect_assembler():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        main(["tests/data/Rect.asm", "--output", temp.name])
        assert filecmp.cmp("tests/data/Rect.hack", temp.name, shallow=False)


def test_pong_assembler():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        main(["tests/data/Pong.asm", "--output", temp.name])
        with open("tests/data/Pong.hack") as f:
            ln = 0
            for l1, l2 in zip(temp, f):
                if l1 != l2:
                    print(f"LINE NUM: {ln}")
                    print(f"{l1} - {l2}")
                ln += 1
        assert filecmp.cmp("tests/data/Pong.hack", temp.name, shallow=False)
