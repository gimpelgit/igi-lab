import matplotlib.pyplot as plt


def save_graph(path, x1, y1, x2, y2):
	plt.plot(x1, y1, label='math.exp', color="r")
	plt.plot(x2, y2, label='taylor_exp', color="g")
	plt.axis('equal')
	plt.legend()
	plt.savefig(path)