def wav_normalize(data):
    value = data*(1/abs(data).max())
    return value
