import math
from enum import Enum


class Intensity(Enum):
    LIGHT = 75
    HEAVY = 90


class Exercise:
    def __init__(self, name, intensity):
        self.name = name
        self.intensity = intensity


class WorkoutDay:
    def __init__(self, number, exercises):
        self.number = number
        self.exercises = exercises


def printWorkoutDay(workoutDay):
    print("Workout #" + str(workoutDay.number))
    for exercise in workoutDay.exercises:
        print(exercise.name + " " + str(exercise.intensity.value))


def printWorkoutPlan(workoutPlan, limit=math.inf):
    print("Workoutplan\n")
    i = 0
    for workoutDay in workoutPlan:
        if i > limit:
            break
        printWorkoutDay(workoutDay)
        print("\n")
        i += 1


def compareWorkoutDays(workoutOne, workoutTwo):
    if len(workoutOne.exercises) != len(workoutTwo.exercises):
        return False
    for i in range(0, len(workoutOne.exercises)):
        if workoutOne.exercises[i].name != workoutTwo.exercises[i].name or workoutOne.exercises[i].intensity != \
                workoutTwo.exercises[i].intensity:
            return False
    return True


def constructWorkoutDay(dominantExercise, dayExercises):
    tempexarray = []
    dayExercises.append(dominantExercise)
    for exercise in dayExercises:
        intensity = Intensity.HEAVY if lightExerciseCounter[exercise] % 3 == 0 else Intensity.LIGHT
        tempexarray.append(Exercise(exercise, intensity))
        lightExerciseCounter[exercise] += 1
    return tempexarray


# We want to have 2* light then 1* heavy exercise

mainExercises = ["Squat", "Deadlift"]
dayOneExercises = ["Bench Press", "Row", "Triceps Extension"]
dayTwoExercises = ["Overhead Press", "Chin Ups",
                   "Curls"]
workoutNumber = 0
workoutPlan = []
lightExerciseCounter = {}
limit = math.inf

# Initiate light exercise counters (we start with light everywhere)
for exercise in mainExercises:
    lightExerciseCounter[exercise] = 1
for exercise in dayOneExercises:
    lightExerciseCounter[exercise] = 1
for exercise in dayTwoExercises:
    lightExerciseCounter[exercise] = 1

# Initiate dominant exercise counter (we start with Squats)
dominantExerciseCounter = 1

while workoutNumber != 100000:

    # Determine Dominant Exercise (1,2 -> Squat, 3 -> Deadlift)
    if dominantExerciseCounter % 3 == 0:
        dominantExercise = mainExercises[1]
    else:
        dominantExercise = mainExercises[0]
    dominantExerciseCounter += 1

    # Determine Exercise Intensities (1,2 -> Light, 3 -> Heavy)

    # We are day one
    if workoutNumber % 2 == 0:
        workoutPlan.append(WorkoutDay(workoutNumber, constructWorkoutDay(dominantExercise, dayOneExercises[:])))
    # We are day two
    else:
        workoutPlan.append(WorkoutDay(workoutNumber, constructWorkoutDay(dominantExercise, dayTwoExercises[:])))

    # Find successful cycle if most recent 20 workout days are identical to the first 20 workout days
    if workoutNumber > 20:
        success = True
        for i in range(0, 20):
            if not compareWorkoutDays(workoutPlan[i], workoutPlan[workoutNumber - 20 + i]):
                success = False
        if success:
            print("Found cycle of " + str(workoutNumber - 20) + " workouts.")
            limit = workoutNumber - 20 - 1
            break

    workoutNumber += 1

printWorkoutPlan(workoutPlan, limit)
