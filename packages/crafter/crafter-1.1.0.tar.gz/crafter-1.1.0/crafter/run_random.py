import argparse
import pathlib
import time

import numpy as np

import crafter


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--seed', type=int, default=None)
  parser.add_argument('--area', nargs=2, type=int, default=(64, 64))
  parser.add_argument('--view', type=int, nargs=2, default=(9, 9))
  parser.add_argument('--size', type=int, nargs=2, default=(64, 64))
  parser.add_argument('--length', type=int, default=10000)
  parser.add_argument('--health', type=int, default=9)
  parser.add_argument('--record', type=pathlib.Path, default=None)
  args = parser.parse_args()

  random = np.random.RandomState(args.seed)
  crafter.constants.items['health']['max'] = args.health
  crafter.constants.items['health']['initial'] = args.health
  env = crafter.Env(args.area, args.view, args.size, args.length, args.seed)
  if args.record:
    recorder = crafter.Recorder()

  start = time.time()
  obs = env.reset()
  if args.record:
    recorder.reset(obs)
  print(f'Reset time: {1000*(time.time()-start):.2f}ms')
  print('Coal exist:    ', env._world.count('coal'))
  print('Iron exist:    ', env._world.count('iron'))
  print('Diamonds exist:', env._world.count('diamond'))

  start = time.time()
  done = False
  while not done:
    action = random.randint(0, env.action_space.n)
    obs, reward, done, info = env.step(action)
    if args.record:
      recorder.step(action, obs, reward, done, info)
  duration = time.time() - start
  step = env._step
  print(f'Step time: {1000*duration/step:.2f}ms ({int(step/duration)} FPS)')
  print('Episode length:', step)

  if args.record:
    recorder.save(args.record)


if __name__ == '__main__':
  main()
