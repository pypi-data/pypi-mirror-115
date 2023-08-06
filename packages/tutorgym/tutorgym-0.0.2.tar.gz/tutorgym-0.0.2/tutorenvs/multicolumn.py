from random import randint
from random import choice
from pprint import pprint
import logging

import cv2  # pytype:disable=import-error
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction import DictVectorizer
import numpy as np
from PIL import Image, ImageDraw

from tutorenvs.utils import OnlineDictVectorizer
from tutorenvs.utils import DataShopLogger
from tutorenvs.utils import StubLogger

pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


def custom_add(a, b):
    if a == '':
        a = '0'
    if b == '':
        b = '0'
    return str(int(a) + int(b))

class MultiColumnAdditionSymbolic:

    def __init__(self, logger=None):
        """
        Creates a state and sets a random problem.
        """
        if logger is None:
            # Note: To Produce log file comment out the stublogger and uncomment the data shop logger
            self.logger = DataShopLogger('MulticolumnAdditionTutor', extra_kcs=['field'])
            # self.logger = StubLogger()
        else:
            self.logger = logger
        self.logger.set_student()
        self.set_random_problem()

    def reset(self, upper, lower):
        """
        Sets the state to a new fraction arithmetic problem as specified by the
        provided arguments.
        """
        correct_answer = str(int(upper) + int(lower))
        self.correct_thousands = ""
        self.correct_hundreds = ""
        self.correct_tens = ""
        self.correct_ones = ""

        if len(correct_answer) == 4:
            self.correct_thousands = correct_answer[0]
            self.correct_hundreds = correct_answer[1]
            self.correct_tens = correct_answer[2]
            self.correct_ones = correct_answer[3]
        elif len(correct_answer) == 3:
            self.correct_hundreds = correct_answer[0]
            self.correct_tens = correct_answer[1]
            self.correct_ones = correct_answer[2]
        elif len(correct_answer) == 2:
            self.correct_tens = correct_answer[0]
            self.correct_ones = correct_answer[1]
        elif len(correct_answer) == 1:
            self.correct_ones = correct_answer[0]
        else:
            raise ValueError("Something is wrong, correct answer should have 1-4 digits")

        upper_hundreds = ''
        upper_tens = ''
        upper_ones = ''

        if len(upper) == 3:
            upper_hundreds = upper[0]
            upper_tens = upper[1]
            upper_ones = upper[2]
        if len(upper) == 2:
            upper_tens = upper[0]
            upper_ones = upper[1]
        if len(upper) == 1:
            upper_ones = upper[0]

        lower_hundreds = ''
        lower_tens = ''
        lower_ones = ''

        if len(lower) == 3:
            lower_hundreds = lower[0]
            lower_tens = lower[1]
            lower_ones = lower[2]
        if len(lower) == 2:
            lower_tens = lower[0]
            lower_ones = lower[1]
        if len(lower) == 1:
            lower_ones = lower[0]

        self.num_correct_steps = 0
        self.num_incorrect_steps = 0
        self.num_hints = 0

        self.state = {
            'thousands_carry': '',
            'hundreds_carry': '',
            'tens_carry': '',
            'upper_hundreds': upper_hundreds,
            'upper_tens': upper_tens,
            'upper_ones': upper_ones,
            'lower_hundreds': lower_hundreds,
            'lower_tens': lower_tens,
            'lower_ones': lower_ones,
            'operator': '+',
            'answer_thousands': '',
            'answer_hundreds': '',
            'answer_tens': '',
            'answer_ones': ''
        }

    def get_possible_selections(self):
        return ['thousands_carry',
                'hundreds_carry',
                'tens_carry',
                'answer_thousands',
                'answer_hundreds',
                'answer_tens',
                'answer_ones',
                'done']

    def get_possible_args(self):
        return [
            'thousands_carry',
            'hundreds_carry',
            'tens_carry',
            'upper_hundreds',
            'upper_tens',
            'upper_ones',
            'lower_hundreds',
            'lower_tens',
            'lower_ones',
            'answer_thousands',
            'answer_hundreds',
            'answer_tens',
            'answer_ones',
            ]

    def render(self, add_dot=None):
        img = self.get_image(add_counts=True, add_dot=add_dot)
        cv2.imshow('vecenv', np.array(img))
        cv2.waitKey(1)

    def get_image(self, add_counts=False, add_dot=None):
        state = {attr: " " if self.state[attr] == '' else
                self.state[attr] for attr in self.state}

        output = " %s%s%s \n  %s%s%s\n+ %s%s%s\n-----\n %s%s%s%s\n" % (
                state["thousands_carry"],
                state["hundreds_carry"],
                state["tens_carry"],
                state["upper_hundreds"],
                state["upper_tens"],
                state["upper_ones"],
                state["lower_hundreds"],
                state["lower_tens"],
                state["lower_ones"],
                state["answer_thousands"],
                state["answer_hundreds"],
                state["answer_tens"],
                state["answer_ones"],
                )

        img = Image.new('RGB', (50, 90), color="white")
        d = ImageDraw.Draw(img)
        d.text((10, 10), output, fill='black')

        # ones
        if state['answer_ones'] == " ":
            d.rectangle(((34, 71), (38, 79)), fill=None, outline='black')
        # tens
        if state['answer_tens'] == " ":
            d.rectangle(((28, 71), (32, 79)), fill=None, outline='black')
        # hundreds
        if state['answer_hundreds'] == " ":
            d.rectangle(((22, 71), (26, 79)), fill=None, outline='black')
        # thousands
        if state['answer_thousands'] == " ":
            d.rectangle(((16, 71), (20, 79)), fill=None, outline='black')

        # ones carry
        if state['tens_carry'] == " ":
            d.rectangle(((28, 11), (32, 19)), fill=None, outline='black')
        # tens carry
        if state['hundreds_carry'] == " ":
            d.rectangle(((22, 11), (26, 19)), fill=None, outline='black')
        # hundreds carry
        if state['thousands_carry'] == " ":
            d.rectangle(((16, 11), (20, 19)), fill=None, outline='black')

        # append correct/incorrect counts
        if add_counts:
            d.text((0, 0), "h:{}".format(self.num_hints), fill=(0,0,0))
            d.text((0, 80), "-:{}".format(self.num_incorrect_steps), fill=(0,0,0))
            d.text((20, 0), "+:{}".format(self.num_correct_steps), fill=(0,0,0))

        if add_dot:
            d.ellipse((add_dot[0]-3, add_dot[1]-3, add_dot[0]+3, add_dot[1]+3),
                    fill=None, outline='blue')

        return img

    def get_state(self):
        """
        Returns the current state as a dict.
        """
        state_output = {attr:
                        {'id': attr, 'value': self.state[attr],
                         'column': 'thousands' if 'thousands' in attr else
                         'hundreds' if 'hundreds' in attr else 'tens' if 'tens'
                         in attr else 'ones',
                         'row': 'answer' if 'answer' in attr else
                         'lower' if 'lower' in attr else 'upper' if 'upper'
                         in attr else 'carry',
                         'type': 'TextField',
                         'contentEditable': self.state[attr] == "",
                         'dom_class': 'CTATTable--cell',
                         'above': '',
                         'below': '',
                         'to_left': '',
                         'to_right': ''
                         }
                        for attr in self.state}
        state_output['done'] = {
            'id': 'done',
            'type': 'Component',
            'dom_class': 'CTATDoneButton',
            'above': '',
            'below': '',
            'to_left': '',
            'to_right': ''
        }

        return state_output

    def set_random_problem(self):
        upper = str(randint(1,999))
        lower = str(randint(1,999))
    
        self.reset(upper=upper, lower=lower)
        self.logger.set_problem("%s_%s" % (upper, lower))

    def apply_sai(self, selection, action, inputs):
        """
        Give a SAI, it applies it. This method returns feedback (i.e., -1 or 1).
        """
        reward = self.evaluate_sai(selection, action, inputs)
        
        if reward > 0:
            outcome = "CORRECT"
            self.num_correct_steps += 1
        else:
            outcome = "INCORRECT"
            self.num_incorrect_steps += 1

        self.logger.log_step(selection, action, inputs['value'], outcome, step_name=selection, kcs=[selection])

        if reward == -1.0:
            return reward

        if selection == "done":
            self.set_random_problem()

        else:
            self.state[selection] = inputs['value']

        return reward



    def evaluate_sai(self, selection, action, inputs):
        """
        Given a SAI, returns whether it is correct or incorrect.
        """
        if selection == "done":

            if action != "ButtonPressed":
                return -1.0

            if (self.state['answer_thousands'] == self.correct_thousands and
                    self.state['answer_hundreds'] == self.correct_hundreds and
                    self.state['answer_tens'] == self.correct_tens and
                    self.state['answer_ones'] == self.correct_ones):
                return 1.0
            else:
                return -1.0

        if self.state[selection] != "":
            return -1.0

        if inputs['value'] == "":
            return -1.0

        if (selection == "answer_ones" and
                inputs['value'] == self.correct_ones):
            return 1.0

        if (selection == "tens_carry" and
                len(custom_add(self.state['upper_ones'],
                    self.state['lower_ones'])) == 2 and
                inputs['value'] == custom_add(self.state['upper_ones'],
                    self.state['lower_ones'])[0]):
                return 1.0

        if (selection == "answer_tens" and self.state['answer_ones'] != "" and
                (self.state['tens_carry'] != "" or 
                    len(custom_add(self.state['upper_ones'],
                        self.state['lower_ones'])) == 1) and
                inputs['value'] == self.correct_tens):
                return 1.0

        if (selection == "hundreds_carry" and
                self.state['answer_ones'] != "" and
                (self.state['tens_carry'] != "" or 
                    len(custom_add(self.state['upper_ones'],
                        self.state['lower_ones'])) == 1)):

            if (self.state['tens_carry'] != ""):
                tens_sum = custom_add(custom_add(self.state['upper_tens'],
                        self.state['lower_tens']), self.state['tens_carry'])
            else:
                tens_sum = custom_add(self.state['upper_tens'],
                        self.state['lower_tens'])

            if len(tens_sum) == 2:
                if inputs['value'] == tens_sum[0]:
                    return 1.0

        if (selection == "answer_hundreds" and
            self.state['answer_tens'] != "" and
            (self.state['hundreds_carry'] != "" or 
               len(custom_add(self.state['upper_tens'],
                   self.state['lower_tens'])) == 1) and
               inputs['value'] == self.correct_hundreds):
            return 1.0

        if (selection == "thousands_carry" and
                self.state['answer_tens'] != "" and
                (self.state['hundreds_carry'] != "" or 
                    len(custom_add(self.state['upper_tens'],
                        self.state['lower_tens'])) == 1)):

            if (self.state['hundreds_carry'] != ""):
                hundreds_sum = custom_add(custom_add(
                    self.state['upper_hundreds'],
                    self.state['lower_hundreds']),
                    self.state['hundreds_carry'])
            else:
                hundreds_sum = custom_add(
                        self.state['upper_hundreds'],
                        self.state['lower_hundreds'])

            if len(hundreds_sum) == 2:
                if inputs['value'] == hundreds_sum[0]:
                    return 1.0

        if (selection == "answer_thousands" and
            self.state['answer_hundreds'] != "" and
            self.state['thousands_carry'] != "" and
            inputs['value'] == self.correct_thousands):
                return 1.0

        return -1.0

    def request_demo(self):
        demo = self.get_demo()
        feedback_text = "selection: %s, action: %s, input: %s" % (demo[0],
                demo[1], demo[2]['value'])
        self.logger.log_hint(feedback_text, step_name=demo[0], kcs=[demo[0]])
        self.num_hints += 1

        return demo

    def get_demo(self):
        """
        Returns a correct next-step SAI
        """

        if (self.state['answer_ones'] == self.correct_ones and
                self.state['answer_tens'] == self.correct_tens and
                self.state['answer_hundreds'] == self.correct_hundreds and
                self.state['answer_thousands'] == self.correct_thousands):
            return ('done', "ButtonPressed", {'value': -1})

        if self.state['answer_ones'] == '':
            return ('answer_ones', 'UpdateField', {'value': str(self.correct_ones)})

        if (self.state["tens_carry"] == '' and
                len(custom_add(self.state['upper_ones'],
                    self.state['lower_ones'])) == 2):
            return ('tens_carry', 'UpdateField',
                    {'value': custom_add(self.state['upper_ones'],
                                         self.state['lower_ones'])[0]})

        if self.state['answer_tens'] == '':
            return ('answer_tens', 'UpdateField', {'value': str(self.correct_tens)})

        if self.state["hundreds_carry"] == '':
            if (len(custom_add(custom_add(self.state['upper_tens'],
                self.state['lower_tens']), self.state['tens_carry'])) == 2):
                return ('hundreds_carry', 'UpdateField',
                        {'value':
                         custom_add(custom_add(self.state['upper_tens'],
                                               self.state['lower_tens']),
                                    self.state['tens_carry'])[0]})

        if self.state['answer_hundreds'] == '':
            return ('answer_hundreds', 'UpdateField', {'value': str(self.correct_hundreds)})

        if self.state["thousands_carry"] == '':
            if (len(custom_add(custom_add(self.state['upper_hundreds'],
                                          self.state['lower_hundreds']),
                               self.state['hundreds_carry'])) == 2):
                return ('thousands_carry', 'UpdateField',
                        {'value':
                         custom_add(custom_add(self.state['upper_hundreds'],
                                               self.state['lower_hundreds']),
                                    self.state['hundreds_carry'])[0]})

        if self.state['answer_thousands'] == '':
            return ('answer_thousands', 'UpdateField', {'value': str(self.correct_thousands)})

        raise Exception("request demo - logic missing")


class MultiColumnAdditionDigitsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.tutor = MultiColumnAdditionSymbolic()
        n_selections = len(self.tutor.get_possible_selections())
        n_features = 110
        self.dv = OnlineDictVectorizer(n_features)
        self.observation_space = spaces.Box(low=0.0,
                high=1.0, shape=(1, n_features), dtype=np.float32)
        self.action_space = spaces.MultiDiscrete([n_selections, 10])
        self.n_steps = 0
        self.max_steps = 5000

    def get_rl_state(self):
        return self.tutor.state

    def step(self, action):
        self.n_steps += 1

        s, a, i = self.decode(action)
        reward = self.tutor.apply_sai(s, a, i)
        state = self.tutor.state
        obs = self.dv.fit_transform([state])[0]
        done = (s == 'done' and reward == 1.0)

        if self.n_steps > self.max_steps:
            done = True

        info = {}

        return obs, reward, done, info

    def decode(self, action):
        s = self.tutor.get_possible_selections()[action[0]]

        if s == "done":
            a = "ButtonPressed"
        else:
            a = "UpdateField"
        
        if s == "done":
            v = -1
        if s == "check_convert":
            v = "x"
        else:
            v = action[1]

        i = {'value': str(v)}

        return s, a, i

    def reset(self):
        self.n_steps = 0
        self.tutor.set_random_problem()
        state = self.get_rl_state()
        obs = self.dv.fit_transform([state])[0]
        return obs

    def render(self, mode='human', close=False):
        self.tutor.render()


def int2_float_add_then_ones(x, y):
    z = float(x) + float(y)
    z = z % 10
    if z.is_integer():
        z = int(z)
    return str(z)


def int2_float_add_then_tens(x, y):
    z = float(x) + float(y)
    z = z // 10
    if z.is_integer():
        z = int(z)
    return str(z)


def int3_float_add_then_ones(x, y, w):
    z = float(x) + float(y) + float(w)
    z = z % 10
    if z.is_integer():
        z = int(z)
    return str(z)


def int3_float_add_then_tens(x, y, w):
    z = float(x) + float(y) + float(w)
    z = z // 10
    if z.is_integer():
        z = int(z)
    return str(z)


def add_tens(x, y, w):
    if w is None:
        return int2_float_add_then_tens(x, y)
    return int3_float_add_then_tens(x, y, w)


def add_ones(x, y, w):
    if w is None:
        return int2_float_add_then_ones(x, y)
    return int3_float_add_then_ones(x, y, w)


class MultiColumnAdditionOppEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.tutor = MultiColumnAdditionSymbolic()
        n_selections = len(self.tutor.get_possible_selections())
        n_features = 5000
        n_operators = len(self.get_rl_operators())
        n_args = len(self.tutor.get_possible_args())
        self.dv = OnlineDictVectorizer(n_features)
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(1, n_features), dtype=np.float32)
        self.action_space = spaces.MultiDiscrete([n_selections, n_operators,
                                                  n_args, n_args, n_args])
        self.n_steps = 0
        self.max_steps = 100000

    def get_rl_operators(self):
        return ['copy',
                'add2-tens',
                'add2-ones',
                'add3-tens',
                'add3-ones',
                ]

    def get_rl_state(self):
        state = self.tutor.state.copy()
        for attr in self.tutor.state:
            if attr == "operator" or state[attr] == "":
                continue
            for attr2 in self.tutor.state:
                if attr2 == "operator" or state[attr2] == "":
                    continue
                if attr >= attr2:
                    continue

                ones2 = int2_float_add_then_ones(state[attr], state[attr2])
                state['add2-ones(%s,%s)' % (attr, attr2)] = ones2
                tens2 = int2_float_add_then_tens(state[attr], state[attr2])
                state['add2-tens(%s,%s)' % (attr, attr2)] = tens2

                for attr3 in self.tutor.state:
                    if attr3 == "operator" or state[attr3] == "":
                        continue
                    if attr2 >= attr3:
                        continue

                    ones3 = int3_float_add_then_ones(state[attr], state[attr2],
                                                     state[attr3])
                    state['add3-ones(%s,%s,%s)' % (attr, attr2, attr3)] = ones3
                    tens3 = int3_float_add_then_tens(state[attr], state[attr2],
                                                     state[attr3])
                    state['add3-tens(%s,%s,%s)' % (attr, attr2, attr3)] = tens3

        return state

    def step(self, action):
        self.n_steps += 1

        try:
            s, a, i = self.decode(action)
            reward = self.tutor.apply_sai(s, a, i)
            done = (s == 'done' and reward == 1.0)
        except ValueError:
            reward = -1
            done = False

        state = self.get_rl_state()
        obs = self.dv.fit_transform([state])[0]
        info = {}

        if self.n_steps > self.max_steps:
            done = True

        return obs, reward, done, info

    def apply_rl_op(self, op, arg1, arg2, arg3):
        if op == "copy":
            return self.tutor.state[arg1]
        elif op == "add2-tens":
            return int2_float_add_then_tens(self.tutor.state[arg1],
                                            self.tutor.state[arg2])
        elif op == "add2-ones":
            return int2_float_add_then_ones(self.tutor.state[arg1],
                                            self.tutor.state[arg2])
        elif op == "add3-tens":
            return int3_float_add_then_tens(self.tutor.state[arg1],
                                            self.tutor.state[arg2],
                                            self.tutor.state[arg3])
        elif op == "add3-ones":
            return int3_float_add_then_ones(self.tutor.state[arg1],
                                            self.tutor.state[arg2],
                                            self.tutor.state[arg3])

    def decode(self, action):
        s = self.tutor.get_possible_selections()[action[0]]
        op = self.get_rl_operators()[action[1]]
        arg1 = self.tutor.get_possible_args()[action[2]]
        arg2 = self.tutor.get_possible_args()[action[3]]
        arg3 = self.tutor.get_possible_args()[action[3]]

        if s == "done":
            a = "ButtonPressed"
        else:
            a = "UpdateField"

        if s == "done":
            v = -1
        if s == "check_convert":
            v = "x"
        else:
            v = self.apply_rl_op(op, arg1, arg2, arg3)

        i = {'value': str(v)}

        return s, a, i

    def reset(self):
        self.n_steps = 0
        self.tutor.set_random_problem()
        state = self.get_rl_state()
        obs = self.dv.fit_transform([state])[0]
        return obs

    def render(self, mode='human', close=False):
        self.tutor.render()


class MultiColumnAdditionPixelEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def get_rl_state(self):
        img = self.tutor.get_image().convert('L')
        return np.expand_dims(np.array(img), axis=2)

    def __init__(self):
        self.tutor = MultiColumnAdditionSymbolic()
        n_selections = len(self.tutor.get_possible_selections())

        print('shape = ', self.get_rl_state().shape)

        self.observation_space = spaces.Box(low=0,
                high=255, shape=self.get_rl_state().shape, dtype=np.uint8)
        self.action_space = spaces.MultiDiscrete([n_selections, 10])

    def step(self, action):
        s, a, i = self.decode(action)
        reward = self.tutor.apply_sai(s, a, i)        
        obs = self.get_rl_state()
        done = (s == 'done' and reward == 1.0)
        info = {}

        return obs, reward, done, info

    def decode(self, action):
        s = self.tutor.get_possible_selections()[action[0]]

        if s == "done":
            a = "ButtonPressed"
        else:
            a = "UpdateField"
        
        if s == "done":
            v = -1
        if s == "check_convert":
            v = "x"
        else:
            v = action[1]

        i = {'value': str(v)}

        return s, a, i

    def reset(self):
        self.tutor.set_random_problem()
        obs = self.get_rl_state()
        return obs

    def render(self, mode='human', close=False):
        if mode == "rgb_array":
            return np.array(self.tutor.get_image(add_counts=True))

        elif mode == "human":
            self.tutor.render()

class MultiColumnAdditionPerceptEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.targets = ['answer_ones', 'tens_carry', 'answer_tens',
                'hundreds_carry', 'answer_hundreds', 'thousands_carry',
                'answer_thousands']
        self.target_xy = [
                (36, 75),
                (30, 15),
                (30, 75),
                (24, 15),
                (24, 75),
                (18, 15),
                (18, 75)
                ]

        self.current_target = 0

        self.set_xy()

        self.tutor = MultiColumnAdditionSymbolic()
        n_selections = len(self.tutor.get_possible_selections())

        print('shape = ', self.get_rl_state().shape)

        self.observation_space = spaces.Box(low=0,
                high=255, shape=self.get_rl_state().shape, dtype=np.uint8)
        self.action_space = spaces.Discrete(12)

    def set_xy(self):
        self.x, self.y = self.target_xy[self.current_target]

    def get_rl_state(self):
        img = self.tutor.get_image().convert('L')
        x_multiplier = 0.75 
        y_multiplier = 1.5
        x = round(self.x - (25 * x_multiplier))
        y = round(self.y - (45 * y_multiplier))

        translate = img.transform((round(img.size[0]*x_multiplier),
            round(img.size[1]*y_multiplier)), Image.AFFINE, (1, 0, x, 0, 1, y), fillcolor='white')

        cv2.imshow('translated', np.array(translate))
        cv2.waitKey(1)
        self.render()

        return np.expand_dims(np.array(translate), axis=2)

    def step(self, action):
        s = None
        reward = -1

        if action == 0:
            self.current_target = (self.current_target + 1) % len(self.targets)
            self.set_xy()

        elif action == 1:
            s = "done"
            a = "ButtonPressed"
            i = -1
        else:
            if self.x >= 34 and self.y >= 71 and self.x <= 38 and self.y <=79:
                s = "answer_ones"
            elif self.x >= 28 and self.y >= 71 and self.x <= 32 and self.y <=79:
                s = "answer_tens"
            elif self.x >= 22 and self.y >= 71 and self.x <= 26 and self.y <=79:
                s = "answer_hundreds"
            elif self.x >= 16 and self.y >= 71 and self.x <= 20 and self.y <=79:
                s = "answer_thousands"

            # carry fields
            elif self.x >= 28 and self.y >= 11 and self.x <= 32 and self.y <=19:
                s = "tens_carry"
            elif self.x >= 22 and self.y >= 11 and self.x <= 26 and self.y <=19:
                s = "hundreds_carry"
            elif self.x >= 16 and self.y >= 11 and self.x <= 20 and self.y <=19:
                s = "thousands_carry"

            a = 'UpdateField'
            i = {'value': str(action - 2)}

        if s != None:
            reward = self.tutor.apply_sai(s, a, i)

        self.x = min(max(self.x, 0), 50)
        self.y = min(max(self.y, 0), 90)

        obs = self.get_rl_state()
        done = (s == 'done' and reward == 1.0)
        info = {}

        return obs, reward, done, info

    def decode(self, action):
        s = self.tutor.get_possible_selections()[action[0]]

        if s == "done":
            a = "ButtonPressed"
        else:
            a = "UpdateField"
        
        if s == "done":
            v = -1
        if s == "check_convert":
            v = "x"
        else:
            v = action[1]

        i = {'value': str(v)}

        return s, a, i

    def reset(self):
        self.tutor.set_random_problem()
        obs = self.get_rl_state()
        return obs

    def render(self, mode='human', close=False):
        if mode == "rgb_array":
            return np.array(self.tutor.get_image(add_counts=True, add_dot=(self.x, self.y)))

        elif mode == "human":
            self.tutor.render(add_dot=(self.x, self.y))
