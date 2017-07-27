import Verilog_VCD
import pprint

file_name = "ex2.vcd"
wave_forms = Verilog_VCD.parse_vcd(file_name)
names = []
waves = []
i = 0
for wave_form_symbol in wave_forms:
    wave_form = wave_forms[wave_form_symbol]
    #get the name of the waveform
    nets = wave_form['nets'][0]
    name[i] = nets['name']

    #get the values of the waveform
    time_values = wave_form['tv']
    #generate wavedrom wave
    last_point = 0
    wave = ""
    for time_value in time_values:
        diff = time_value-last_value
        for j in range(diff):
            x = x+"3"

    

