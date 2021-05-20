import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

#create fig
fig,((ax1,ax2))=plt.subplots(2,1,sharex=True)
fig.suptitle("Sampling of Distributions\n\n(Parametrize and then run)", fontsize="x-large")

#sliders axis
ax2=plt.subplot(2, 1, 2)             
ax2.axis('off')
ax2.set_title('\nParametrize Normal Distribution')
axis_color = 'lightgoldenrodyellow'
E0_slider_ax = fig.add_axes([0.13, .22, 0.3, 0.02], axisbg=axis_color)
E1_slider_ax = fig.add_axes([0.13, .17, 0.3, .02], axisbg = axis_color)
E0_slider = Slider(E0_slider_ax, r'Normal $\mu$', valmin = -5, valmax = 5, valinit = -2.5)
E0_slider.label.set_size(15)
E1_slider = Slider(E1_slider_ax, r'Normal $\sigma$', 0, 5, valinit = 1)
E1_slider.label.set_size(15)

#animation function
def update(curr, x1):
    plt.subplot(2, 1, 1)
    plt.cla()


    plt.axis([np.round(np.percentile(x1,.05)),np.round(np.percentile(x1,99.5)),0,1])   #plot 99% cuantile
    plt.hist(x1[:curr*100+100], normed=True, bins=20, alpha=0.5)
    plt.gca().set_title('\n\nNormal n={}'.format(curr*100+100))

#create animation start button
def animate_button(self):
    x1 = np.random.normal(E0_slider.val, E1_slider.val, 5000)
    a = animation.FuncAnimation(fig, update, , fargs=(x1, ), frames=100,interval=500, repeat=False)
    fig.canvas.draw()

#animation button
axnext = fig.add_axes([0.785, 0.02,0.1, 0.075], axisbg = axis_color)
bnext = Button(axnext, 'Run Simulations!')
bnext.on_clicked(animate_button)

plt.show()