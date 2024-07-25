import nn

p_nn = nn.p_nn()
p_nn.load_weights("o_p_nn.h5")

data = [
    [0, 1, -1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, -1, 0],
    [-1, 0, 1, 1, 1, 0, -1, 0, -1],
    [0, 0, 0, 0, 1, -1, 0, 0, 1]
]

labels = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0]
]

p_nn.fit(x=data, y=labels, epochs=15, batch_size=4)
p_nn.save_weights("p_nn.h5")
