import pytest

from main import cmds_first_step_check,get_cmds,get_sorted_files

@pytest.mark.parametrize(
        "text, result",
        [
            ("CMDS = ['echo 1']", True),
            ("TEST_VAR = ['echo 1']", False),         
        ]
)
def test_cmds_first_step_check(text,result,tmpdir):
    test_file = tmpdir.join("test_cmds.py")
    test_file.write(text)
    assert cmds_first_step_check(str(test_file)) == result


@pytest.mark.parametrize(
        "text, result",
        [
            ("CMDS = ['echo 1']", ["echo 1"]),
            ("CMDS = ['echo 1', 'echo 2']", ["echo 1", "echo 2"]),
            ("z = '5'\nCMDS = ['echo ' + z, 'echo 2']", ["echo 5", "echo 2"]),
            ("a = 1\nb = 2\nz = str(a+b)\nCMDS = ['echo ' + z, 'echo 2']", ["echo 3", "echo 2"]),
            ("TEST_VAR = ['echo 1']", []),         
        ]
)
def test_get_cmds(text, result, tmpdir):
    test_file = tmpdir.join("test_cmds.py")
    test_file.write(text)
    assert get_cmds(str(test_file)) == result



def test_get_sorted_files(tmpdir):
    paths = ['a.py','1/c.py','2/b.py','3.txt']
    for path in paths: 
        test_file = tmpdir.join(path)
        test_file.ensure()
    sorted_files = get_sorted_files(tmpdir)
    sorted_files = [x.replace(str(tmpdir),'') for x in sorted_files]
    assert sorted_files== ['/1/c.py','/2/b.py','/a.py']