from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    # ── tuneable parameters ───────────────────────────────────────────
    A = 2.5  # location of the vertical asymptote

    @staticmethod
    def f(x):
        """Wiggly function with vertical asymptote at A: → +∞ as x → A⁻."""
        return 1.0 / (2.5 - x) + 0.22 * np.sin(4 * np.pi * x)

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_FUNC  = "#1A6FC4"  # blue   - graph
        C_ASYMP = "#B03A2E"  # red    - vertical asymptote
        C_POINT = "#CA6F1E"  # orange - moving tracker dot
        C_TEXT  = "#1A1A1A"
        C_AXES  = "#555555"
        # fmt: on

        #
        # AXES
        #
        axes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[0, 7, 1],
            x_length=5.0,
            y_length=5.6,
            axis_config={
                "color": C_AXES,
                "include_tip": True,
                "tip_length": 0.20,
                "stroke_width": 2,
            },
            x_axis_config={},
            y_axis_config={},
        ).shift(DOWN * 0.3)

        ax_x = MathTex("x", color=C_TEXT, font_size=26).next_to(
            axes.get_x_axis(), RIGHT, buff=0.12
        )
        ax_y = MathTex("y", color=C_TEXT, font_size=26).next_to(
            axes.get_y_axis(), UP, buff=0.12
        )

        self.play(Create(axes), Write(ax_x), Write(ax_y), run_time=1.2)

        #
        # GRAPH
        #
        X_PLOT_END = self.A - 1.0 / 6.5
        X_GRAPH_END = self.A - 0.03

        graph = axes.plot(
            self.f,
            x_range=[0.3, X_GRAPH_END, 0.005],
            color=C_FUNC,
            stroke_width=3,
        )

        self.play(Create(graph), run_time=1.4)
        self.wait(0.3)

        #
        # VERTICAL ASYMPTOTE at x = A
        #
        asymptote = DashedLine(
            axes.c2p(self.A, 0),
            axes.c2p(self.A, 7),
            color=C_ASYMP,
            stroke_width=2.0,
            dash_length=0.15,
        )
        lbl_a = MathTex("a", color=C_ASYMP, font_size=30).next_to(
            axes.c2p(self.A, 0), DOWN, buff=0.22
        )

        self.play(Create(asymptote), Write(lbl_a), run_time=0.9)
        self.wait(0.5)

        #
        # MOVING DOT: left-hand approach x → A⁻
        #
        x_t = ValueTracker(0.4)

        moving_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_t.get_value(), self.f(x_t.get_value())),
                color=C_POINT,
                radius=0.09,
                z_index=6,
            )
        )

        v_trace = always_redraw(
            lambda: DashedLine(
                axes.c2p(x_t.get_value(), 0),
                axes.c2p(x_t.get_value(), self.f(x_t.get_value())),
                color=C_POINT,
                stroke_width=1.4,
                dash_length=0.09,
            )
        )

        x_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_t.get_value(), 0),
                color=C_POINT,
                radius=0.07,
                z_index=6,
            )
        )

        self.play(FadeIn(moving_dot), FadeIn(v_trace), FadeIn(x_dot))

        self.play(
            x_t.animate.set_value(X_PLOT_END),
            run_time=4.0,
            rate_func=linear,
        )

        self.play(
            x_t.animate.set_value(X_GRAPH_END),
            self.camera.frame.animate.scale(2.0),
            run_time=3.5,
            rate_func=linear,
        )
        self.wait(1.5)
