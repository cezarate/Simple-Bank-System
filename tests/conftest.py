from pytest import MonkeyPatch

mp = MonkeyPatch()
mp.setenv(name="DB_NAME", value="test")