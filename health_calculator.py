BMI_MAX = 24.0
BMI_MIN = 18.5
EXERCISE_FACTOR = {'1': 1.2, '2': 1.375, '3': 1.55, '4': 1.725, '5': 1.9}


def BMI_calculator(weight: float, height: float) -> float:
    # BMI = weight(kg) / (height(m) ** 2
    return round(weight / (height**2), 1)


def BMI_ideal_weight(weight: float, height: float) -> float:
    bmi = BMI_calculator(weight, height)
    print(f"你的BMI:               {bmi:2.1f}")
    if BMI_MIN <= bmi < BMI_MAX:
        ideal_w = 0
    elif bmi < BMI_MIN:
        ideal_w = round(BMI_MIN*(height**2), 1)
        print(
            f"BMI太低了喔! 理想應該要在 {BMI_MIN} ~ {BMI_MAX} 之間，你的體重應該要上升至 {ideal_w} kg")
    else:
        ideal_w = round(BMI_MAX*(height**2), 1)
        print(
            f"BMI太高了喔! 理想應該要在 {BMI_MIN} ~ {BMI_MAX} 之間，你的體重應該要下降至 {ideal_w} kg")

    return ideal_w


def BMR_calculator(sex: int, weight: float, height: float, age: int) -> float:
    # Mifflin-St Jeor formula
    # 9.99 × 體重 + 6.25 × 身高 - 4.92 × 年齡 +(166 × 性別 (男 1、女 0) - 161)
    BMR1 = 9.99 * weight + 6.25*100*height - 4.92 * age + (166*sex-161)

    # Harris-Benedict Equation
    # male  : 66 ＋( 13.7*體重kg＋5  *身高cm－6.8*年齡)
    # female:655 ＋( 9.6 *體重kg＋1.8*身高cm－4.7*年齡)
    if sex:
        BMR2 = 66.5 + (13.75*weight + 5.003*100*height-6.755*age)
    else:
        BMR2 = 655 + (9.563*weight + 1.85*100*height-4.676*age)
    return round((BMR1 + BMR2) / 2, 1)


def TDEE_calculator(sex: int, weight: float, height: float, age: int, exercise: str) -> float:
    BMR = BMR_calculator(sex, weight, height, age)

    TDEE = round(EXERCISE_FACTOR[exercise] * BMR, 1)
    print(f'基礎代謝率      (BMR): {BMR} kcal')
    print(f'每日總熱量消耗 (TDEE): {TDEE} kcal')
    return TDEE


sex = int(input("請輸入你的性別(0:女，男:1): ").strip())
age = int(input("請輸入你的年紀: ").strip())
height = float(input("請輸入你的身高(cm): ").strip())/100
weight = float(input("請輸入你的體重(kg): ").strip())
print("選擇你每天的活動程度:")
print('----------------------------------')
print("1. 無活動  (臥床)")
print("2. 輕度活動(久坐)     每週運動1-3天")
print("3. 中度活動(站走稍多) 每週運動3-5天")
print("4. 高度活動(站走為主) 每週運動6-7天")
print("5. 非常高度活動       每週運動7+ 天")
exercise = input().strip()
print('----------------------------------')

b = BMI_ideal_weight(weight, height)
d = TDEE_calculator(sex, weight, height, age, exercise)
