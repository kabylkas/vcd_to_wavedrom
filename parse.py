import Verilog_VCD
import pprint

file_name = "ex2.vcd"
wave_forms = Verilog_VCD.parse_vcd(file_name)
names = []
sizes = []
waves = []
values = []
max_time = 0
for wave_form_symbol in wave_forms:
    wave_form = wave_forms[wave_form_symbol]
    #get the name of the waveform
    nets = wave_form['nets'][0]
    name = nets['name']
    size = nets['size']
    names.append(name)
    sizes.append(size)

    #get the values of the waveform
    time_values = wave_form['tv']
    #generate wavedrom wave
    last_time = 0
    temp_values = []
    for time_value in time_values:
        #get the time and value
        time = time_value[0]
        value = time_value[1]
        temp_values.append(value)
        #save the maximum time for further processing
        if max_time<time:
            max_time = time
        diff = time-last_time
        last_time = time
        #determine the value and data type for wavedrom
        wave_continue = '3'
        if size == '1':
            wave_continue = '0'
            if value == '1':
                wave_continue = '1'

        #put/append to the wave
        if diff == 0:
            wave = wave_continue
        else:
            for j in range(diff-1):
                wave += '.'
            wave += wave_continue

    #save the wave
    waves.append(wave)
    values.append(temp_values)

#extend the waves to make them equal
waves_extended = []
max_time+=10
print max_time
for wave in waves:
    diff = max_time-len(wave)
    for j in range(diff):
        wave+='.'
    waves_extended.append(wave)

#construct WavedromJSON
i=0
wavedrom_json = '{signal: ['
for wave in waves_extended:
    if i>0:
       wavedrom_json += ', '
    #construct values
    str_values = ""
    not_first = False
    temp_values = values.pop(0)
    size = sizes.pop(0)
    name = names.pop(0)
    if not size == '1':
        for value in temp_values:
            if not_first:
                str_values += ", "
            str_values += "'"+value+"'"
            not_first = True
    if not size == '1':
        wavedrom_json += "{name: '"+name+"', wave: '"+wave+"', data: ["+str_values+"]}"
    else:
        wavedrom_json += "{name: '"+name+"', wave: '"+wave+"'}"
    i+=1

wavedrom_json += ']}'

print(wavedrom_json)
   
