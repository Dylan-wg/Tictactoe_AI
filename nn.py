from keras.models import Sequential
from keras.layers import Dense

def p_nn():
    ''' Policy Network '''

    p_nn = Sequential()
    p_nn.add(Dense(64, input_dim=9, activation="relu"))
    p_nn.add(Dense(64, activation="sigmoid"))
    p_nn.add(Dense(9, activation="linear"))
    p_nn.add(Dense(9, activation="sigmoid"))
    p_nn.compile(optimizer="adam", loss="mean_squared_error")

    return p_nn

def v_nn():
    ''' Value Network '''

    v_nn = Sequential()
    v_nn.add(Dense(64, input_dim=9, activation="relu"))
    v_nn.add(Dense(64, activation="sigmoid"))
    v_nn.add(Dense(9, activation="linear"))
    v_nn.add(Dense(1, activation="sigmoid"))
    v_nn.compile(optimizer="adam", loss="mean_squared_error")

    return v_nn
