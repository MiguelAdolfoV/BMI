from pylsl import StreamInlet, resolve_stream

print("looking for an EEG stream...")
brain_stream = resolve_stream("name", "AURA_Power_Power")

brain_inlet = StreamInlet(brain_stream[0])
brain_inlet.open_stream()
print("While entered")

global sample 
while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = brain_inlet.pull_sample()
    print(sample)