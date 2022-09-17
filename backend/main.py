from flask import Flask, request, render_template
from typing import List
import copy

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return render_template('index.html')

# VueからのPOSTリクエスト
@app.route('/api/resolve', methods=["POST"])
# Vueからリクエストされたときのメソッド
def resolve():
  # POSTで送られてきたjsonオブジェクトを受け取る
  get_request = request.get_json()
  # jsonオブジェクトの中の数独の配列を取得
  get_numbers = get_request['numbers']
  # 問題の初期状態を保存しておく
  initial_value = copy.deepcopy(get_numbers)
  # 計算結果をresultsにいれる
  results = get_result(get_numbers)
  # 別解存在フラグ
  has_another_solution = False
  # 解存在フラグ
  has_solution = results != None
  # 解があったら
  if has_solution:
    # 初期状態に戻す
    get_numbers = initial_value
    # 別解があるか確認する
    has_another_solution = checkAnotherSolution(get_numbers, results[0])
  # Vueに計算結果を返却する
  return { 'results': results, 'has_another_solution': has_another_solution, 'has_solution': has_solution }

def get_result(numbers: List[List[int]]):
  results = []
  initial_value = copy.deepcopy(numbers)
  # 回答が作れた時
  if solve(0, 0, numbers, range(1, 10)):
    results.append(numbers)
    return(results)
  else:
    return
  
def solve(x, y, numbers, current_range):
  if x == 0 and y == 9:
    return True
  
  if numbers[y][x] == 0:
    for i in current_range:
      numbers[y][x] = i
      if isValid(x, y, numbers):
        (nx, ny) = next(x, y)
        if solve(nx, ny, numbers, current_range):
          return True
    numbers[y][x] = 0
    return False
  else:
    (nx, ny) = next(x, y)
    if solve(nx, ny, numbers, current_range):
      return True
  
def next(x, y):
  if x == 8:
    x = 0
    y += 1
  else:
    x += 1
  return (x, y)

# 縦、横、ボックスに同じ数字がないか
def isValid(x, y, numbers):
  return isValidRow(x, y, numbers) and isValidColumn(x, y, numbers) and isValidBox(x, y, numbers)

# 横に同じ数字がないか
def isValidRow(x, y, numbers):
  for t in range(9):
    if x != t:
      if numbers[y][x] == numbers[y][t]:
        return False
  return True

# 縦に同じ数字がないか
def isValidColumn(x, y, numbers):
  for t in range(9):
    if y != t:
      if numbers[y][x] == numbers[t][x]:
        return False
  return True

# ボックスに同じ数字がないか
def isValidBox(x, y, numbers):
  start_x = (x // 3) * 3
  start_y = (y // 3) * 3
  box = [(m, n) for m in range(start_x, start_x + 3) for n in range(start_y, start_y + 3) if (m, n) != (x, y)]
  for (m, n) in box:
    if numbers[y][x] == numbers[n][m]:
      return False
  return True

def checkAnotherSolution(numbers, result):
  if solve(0, 0, numbers, range(9, 0, -1)):
    return result != numbers

## おまじない
if __name__ == "__main__":
    app.run()