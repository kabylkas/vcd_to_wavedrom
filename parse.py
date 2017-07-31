import Verilog_VCD

read_file_name = "ex4.vcd"
print("Reading {0} file...".format(read_file_name))
wave_forms = Verilog_VCD.parse_vcd(read_file_name)
print("Parsing {0} file...".format(read_file_name))
names = []
sizes = []
waves = []
values = []
max_time = 0
i=0;
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

print("Successfully parsed .vcd file")

#extend the waves to make them equal
waves_extended = []
waves_shortened = []
max_time+=10
max_length = 50
for wave in waves:
    diff = max_time-len(wave)
    for j in range(diff):
        wave+='.'
    waves_extended.append(wave)
    if max_length<len(wave):
        waves_shortened.append(wave[0:max_length])

#construct WavedromJSON
#waves_to_process = waves_extended
waves_to_process = waves_shortened

i=0
wavedrom_json = '{signal: ['
for wave in waves_to_process:
    if i>0:
       wavedrom_json += ',\n'
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

print("Successfully generated wavedrom...")

# writing html file
path_to_wavedrom = "../wavedrom/test/"
write_file_name = "vcd_to_wavedrom.html"
f = open(path_to_wavedrom+write_file_name, 'w')

to_write = """<html>
<head>
  <meta charset="UTF-8">
  <title>testsuit</title>
  <script type="text/javascript" src="../skins/default.js"></script>
  <script type="text/javascript" src="../skins/narrow.js"></script>
  <script type="text/javascript" src="../wavedrom.min.js"></script>
</head>

<body>

<div class="content">

<script type="WaveDrom">"""+wavedrom_json+"""</script>
<script>(function(){ window.addEventListener("load", WaveDrom.ProcessAll, false); })();</script>
</body>
</html>"""

f.write(to_write)
f.close()
print("Generated file: {0}".format(path_to_wavedrom+write_file_name))
print("Done!")
