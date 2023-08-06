import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm


def plot_posterior(
    data, dt, R, pmean, pvar, cps, title=None, save=False, save_name=None
):
    T = len(data)
    fig, axes = plt.subplots(2, 1, figsize=(20, 8))
    _plot(data, fig, axes, dt, R, pmean, pvar, cps, title, T)
    if save:
        plt.savefig(save_name)


def plot_posterior_animation(data, fig, axes, dt, R, pmean, pvar, cps, title=None):
    T = len(data)
    _plot(data, fig, axes, dt, R, pmean, pvar, cps, title, T)


def _plot(data, fig, axes, dt, R, pmean, pvar, cps, title, T):
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = "20"
    fig.suptitle(title, fontsize=24)
    fig.autofmt_xdate()
    ax1, ax2 = axes
    ax1.cla()
    _ax1_plot(data, dt, pmean, pvar, ax1)

    ax2.cla()
    _ax2_plot(R, T, ax2)

    _extras(fig, cps, ax1, ax2)


def _extras(fig, cps, ax1, ax2):
    for cp in cps:
        ax1.axvline(cp, c="red", ls="dotted", label="Ground Truths")
        ax2.axvline(cp, c="red", ls="dotted")

    plt.tight_layout()
    handles, labels = [
        (a + b)
        for a, b in zip(
            ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels()
        )
    ]
    fig.legend(handles, labels)


def _ax2_plot(R, T, ax2):
    ax2.imshow(
        np.rot90(R), aspect="auto", cmap="gray_r", norm=LogNorm(vmin=0.0001, vmax=1)
    )
    maxes = R.argmax(axis=1)
    ax2.plot(len(R) - maxes, c="r", linewidth=3, label="Maxes")
    ax2.set_xlim([0, T])
    ax2.margins(0)


def _ax1_plot(data, dt, pmean, pvar, ax1):
    ax1.scatter(dt, data)
    ax1.plot(dt, data)
    ax1.set_xlim([dt[0], dt[-1]])
    ax1.margins(0)

    # Plot predictions.
    ax1.plot(dt, pmean, c="k", label="Mean Prediction")
    _2std = 2 * np.sqrt(pvar)
    ax1.plot(dt, pmean - _2std, c="k", ls="--", label="Mean Prediction +- 2std")
    ax1.plot(dt, pmean + _2std, c="k", ls="--")


def display(X, n, T, L, S, Ts, peaks=None, plot_peak_height=10, s_max=10):

    plt.cla()
    score_plot_ix = _rulsif_data_plot(X, n, T, L, peaks)
    plt.subplot(n, 1, score_plot_ix)
    plt.cla()
    _rulsif_score_plot(T, L, S, Ts, s_max)

    # display find peaks #todo refactoring
    _rulsif_peaks_plot(n, T, L, peaks, plot_peak_height, s_max)

    _rulsif_env_settings(T, s_max)


def _rulsif_env_settings(T, s_max):
    plt.ylim(-1, s_max)
    plt.xlim(0, T.max())
    plt.xticks(size=16)
    plt.yticks(np.arange(0, s_max + 1, 5), size=16)
    plt.xlabel("Time", size=16)
    plt.legend(fontsize=16)
    plt.tight_layout()


def _rulsif_peaks_plot(n, T, L, peaks, plot_peak_height, s_max):
    if peaks is not None:
        plt.subplot(n, 1, n)
        new_score_peaks = np.zeros(len(T))
        new_score_peaks[peaks] = plot_peak_height
        plt.plot(new_score_peaks, linewidth=3, label="Peaks", color="C4")
        for t in T[L == 1]:
            plt.plot([t] * 2, [-1, s_max], color="0", linestyle="--")


def _rulsif_score_plot(T, L, S, Ts, s_max):
    plt.plot(Ts, S, linewidth=3, label="Change-point score", color="C3")
    plt.xlim(0, T.max())
    for t in T[L == 1]:
        plt.plot([t] * 2, [-1, s_max], color="0", linestyle="--")


def _rulsif_data_plot(X, n, T, L, peaks):
    for i in range(X.shape[1]):
        plt.subplot(n, 1, i + 1)
        ax = X[:, i]
        plt.plot(T, ax, linewidth=2, label="Original signal", color="C0")
        for t in T[L == 1]:
            plt.plot([t] * 2, [ax.min(), ax.max()], color="0", linestyle="--")
        plt.ylim(ax.min(), ax.max())
        plt.xlim(0, T.max())
        plt.xticks(size=16)
        plt.yticks(size=16)

    score_plot_ix = n if peaks is None else n - 1
    return score_plot_ix
