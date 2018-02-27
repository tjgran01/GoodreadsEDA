import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("seaborn-white")

scores = [5, 4, 3, 2, 1]
amts = [2986, 2618, 1240, 621, 371]
all_scores = []

for i, amt in enumerate(amts):
    for x in range(0, amt):
        if i == 0:
            all_scores.append(5)
        elif i == 1:
            all_scores.append(4)
        elif i == 2:
            all_scores.append(3)
        elif i == 3:
            all_scores.append(2)
        elif i == 4:
            all_scores.append(1)
        else:
            print("Something must have happened.")


plt.bar(scores, amts, color="#adcaea", edgecolor="#96afd9", linewidth="3")
plt.title("Distribution of Review Scores")
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")
sns.despine()
plt.show()
