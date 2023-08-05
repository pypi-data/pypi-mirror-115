from frdate import frdate
import datetime

d1='14 juillet 1789'
d2=datetime.date(1789,7,14)
echantillon=[
  '14071789',
  '14/07/1789',
  '17890714',
  '14 07 1789',
  '14 juillet 1789',
  '1789-07-14',
  'quatorze juillet 1789'
   ]

def test_fr_conv():
  assert frdate.conv('2000-01-01',litteral=True) == 'premier janvier deux mille'
  assert frdate.conv('2000-01-01',True) == datetime.date(2000,1,1)
  assert frdate.conv('2000-01-01') == '1er janvier 2000'
  assert frdate.conv('10101212') == '10 octobre 1212'
  for t in echantillon:
    assert frdate.conv(t) == d1
    assert frdate.conv(t,True) == d2
  assert frdate.conv(echantillon) == [d1 for i in range(len(echantillon))]
