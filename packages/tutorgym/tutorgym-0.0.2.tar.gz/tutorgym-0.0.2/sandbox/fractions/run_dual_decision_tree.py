from tutorenvs.fractions import FractionArithSymbolic

from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer

from tutorenvs.utils import DataShopLogger


def train_tree(n=10, logger=None):
    X = []
    y_sel = []
    y_inp = []
    dv = DictVectorizer()
    selections = []
    selection_mapping = {}
    rev_selection_mapping = {}
    selection_tree = DecisionTreeClassifier()

    inputs = []
    input_mapping = {}
    rev_input_mapping = {}
    input_tree = DecisionTreeClassifier()

    env = FractionArithSymbolic(logger)

    p = 0
    hints = 0

    while p < n:
        state = {a: env.state[a] for a in env.state}
        env.render()

        if rev_selection_mapping == {}:
            sai = None
        else:
            vstate = dv.transform([state])
            sel = rev_selection_mapping[selection_tree.predict(vstate)[0]]
            if sel == 'done':
                act = 'ButtonPressed'
            else:
                act = "UpdateField"
            inp = rev_input_mapping[input_tree.predict(vstate)[0]]
            sai = (sel, act, inp)

        if sai is None:
            hints += 1
            sai = env.request_demo()
            sai = (sai[0], sai[1], sai[2]['value'])

        reward = env.apply_sai(sai[0], sai[1], {'value': sai[2]})

        if reward < 0:
            hints += 1
            sai = env.request_demo()
            sai = (sai[0], sai[1], sai[2]['value'])
            reward = env.apply_sai(sai[0], sai[1], {'value': sai[2]})

        X.append(state)
        y_sel.append(sai[0])
        y_inp.append(sai[2])

        Xv = dv.fit_transform(X)

        selections = list(set(y_sel))
        selection_mapping = {l: i for i, l in enumerate(selections)}
        rev_selection_mapping = {i: l for i, l in enumerate(selections)}

        inputs = list(set(y_inp))
        input_mapping = {l: i for i, l in enumerate(inputs)}
        rev_input_mapping = {i: l for i, l in enumerate(inputs)}

        yv_sel = [selection_mapping[i] for i in y_sel]
        yv_inp = [input_mapping[i] for i in y_inp]

        selection_tree.fit(Xv, yv_sel)
        input_tree.fit(Xv, yv_inp)

        if sai[0] == "done" and reward == 1.0:
            print("Problem %s of %s" % (p, n))
            print("# of hints = {}".format(hints))
            hints = 0
            p += 1

    return selection_tree, input_tree


if __name__ == "__main__":

    logger = DataShopLogger('FractionsTutor', extra_kcs=['field'])
    for _ in range(1):
        tree = train_tree(800, logger)
