x, y = zip(*lazorPath)
n, s = zip(*list(NS.keys()))
e, w = zip(*list(EW.keys()))
xo, yo = zip(*listOfOrigins)

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='r')
plt.scatter(n, s, color='k')
plt.scatter(e, w, color='k')
plt.scatter(xo, yo, color='c')

for n in range(len(x)):
    line.set_data(x[:n], y[:n])
    fig.canvas.draw()
    fig.savefig('Frame%03d.png' %n)
