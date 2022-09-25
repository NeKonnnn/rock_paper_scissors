
import numpy as np
import collections
def Jonson_agent(observation, configuration):
    k = 2
    global table, action_seq
    if observation.step % 25 == 0: # обновляем таблицу каждые 25 шагов. 
        action_seq, table = [], collections.defaultdict(lambda: [1, 1, 1])    
    if len(action_seq) <= 2 * k + 1:
        action = int(np.random.randint(3))
        if observation.step > 0:
            action_seq.extend([observation.lastOpponentAction, action])
        else:
            action_seq.append(action)
        return action
    # вносим изменения
    key = ''.join([str(a) for a in action_seq[:-1]])
    table[key][observation.lastOpponentAction] += 1
    # вносим изменения последовательности действий
    action_seq[:-2] = action_seq[2:]
    action_seq[-2] = observation.lastOpponentAction
    # предсказание следующего хода опонента
    key = ''.join([str(a) for a in action_seq[:-1]])
    if observation.step < 50:
        next_opponent_action_pred = np.argmax(table[key])
    else:
        scores = np.array(table[key])
        next_opponent_action_pred = np.random.choice(3, p=scores/scores.sum())
    # совершаем действия
    action = (next_opponent_action_pred + 1) % 3
    # меняем стратегию, если высок шанс проигрыша
    if observation.step > 90:
        action = next_opponent_action_pred
    action_seq[-1] = action
    return int(action)
