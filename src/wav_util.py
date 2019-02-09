def wav_normalize(data):
    value = data*(1/abs(data).max())
    return value

def wav_mono(data):
    value = data.sum(axis=1)/2
    return value

