from app import app
from model.FuzzingPlatform import FuzzingPlatform
from model.FuzzingArch import FuzzingArch
from model.FuzzingEngine import FuzzingEngine
from model.FuzzingJobState import FuzzingJobState
from model.FuzzingTarget import FuzzingTarget
from model.FuzzingScript import FuzzingScript
from model.FuzzingOptionType import FuzzingOptionType
from model.FuzzingOption import FuzzingOption

db = app.config['db']

#Fuzzing Job Status
db.session.add(FuzzingJobState('Queued'))           #DO NOT CHANGE
db.session.add(FuzzingJobState('Allocated'))        #DO NOT CHANGE
db.session.add(FuzzingJobState('Active'))           #DO NOT CHANGE
db.session.add(FuzzingJobState('Completed'))        #DO NOT CHANGE
db.session.add(FuzzingJobState('Paused'))           #DO NOT CHANGE
db.session.add(FuzzingJobState('Failed'))           #DO NOT CHANGE
#db.session.add(FuzzingJobState('Reserved'))         #DO NOT CHANGE

#Fuzzing Option
field_type = FuzzingOptionType("FIELD")             #DO NOT CHANGE
file_type = FuzzingOptionType("FILE")               #DO NOT CHANGE
list_type = FuzzingOptionType("LIST")               #DO NOT CHANGE
checkbox_type = FuzzingOptionType("CHECKBOX")       #DO NOT CHANGE
db.session.add(field_type)
db.session.add(file_type)
db.session.add(list_type)
db.session.add(checkbox_type)


#Platforms
unknown_plat = FuzzingPlatform('Unknown')
db.session.add(unknown_plat)

#Architectures
unknown_arch = FuzzingArch('Unknown')
db.session.add(unknown_arch)

#Options
afl_in_dir = FuzzingOption('afl_in_dir', field_type)
afl_out_dir = FuzzingOption('afl_out_dir', field_type)
afl_timeout = FuzzingOption('afl_timeout', field_type)
db.session.add(afl_in_dir)
db.session.add(afl_out_dir)
db.session.add(afl_timeout)


#Fuzzing Engines
db.session.add(
    FuzzingEngine("afl", "/usr/local/bin/afl-fuzz", unknown_plat, unknown_arch, [afl_out_dir, afl_timeout, afl_in_dir ])
)

#Fuzzing Targets
db.session.add(FuzzingTarget('libpng-1.5.27', "/home/vagrant/libpng-1.5.27/pngtest", unknown_plat, unknown_arch))
db.session.add(FuzzingTarget('tiff-4.0.6-fake-vulnerable', "/home/vagrant/tiff-4.0.6/tools/tiff2pdf", unknown_plat, unknown_arch))


#Fuzzing Script
db.session.add(FuzzingScript('test-script',
'''<?xml version="1.0"?>
<test>
    <something>go</something>
</test>
'''))


