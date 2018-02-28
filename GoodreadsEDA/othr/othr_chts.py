import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("seaborn-white")

scores = [5, 4, 3, 2, 1]
amts = [2986, 2618, 1240, 621, 371]

mean_diffs = [-0.18268497330282196, -0.08435934144595558, -0.04966431623099199,
              0.06767546411187286]
mean_x = ["a. 3mo", "b. 6mo", "c. 1yr", "d. All"]

all_scores = []

# plt.bar(scores, amts, color="#adcaea", edgecolor="#96afd9", linewidth="3")
# plt.title("Distribution of Review Scores")
# plt.xlabel("Review Score")
# plt.ylabel("Number of Reviews")
# sns.despine()
# plt.show()

plt.plot(mean_x, mean_diffs, marker="o", color="#adcaea")
plt.title("Changes in Mean Review Scores \nBefore and After Movie Release \n(Scale of 1-5)")
plt.ylabel("Change in Mean Review Score")
plt.xlabel("Timeframe")
plt.grid(True)
sns.despine()
plt.show()
