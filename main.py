from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    A = 2.0
    L = 2.8

    @staticmethod
    def f_left(x):
        """Left branch: wiggly, ends at f_left(A) = 2.0."""
        return x + 0.35 * np.sin(3 * np.pi * x)

    @staticmethod
    def f_right(x):
        """Right branch: wiggly, approaches L=2.8 as x→2⁺."""
        return -0.5 * x + 3.8 + 0.3 * np.sin(3 * np.pi * x)

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_FUNC  = "#1A6FC4"  # blue   – graph
        C_LIMIT = "#B03A2E"  # red    – limit / L guide
        C_POINT = "#CA6F1E"  # orange – moving tracker dot
        C_TEXT  = "#1A1A1A"
        C_AXES  = "#555555"
        # fmt: on

        #
        # AXES
        #
        axes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[0, 3.5, 1],
            x_length=5.6,
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
        # GRAPH: two branches
        #
        left_branch = axes.plot(
            self.f_left,
            x_range=[0.1, 2.0, 0.005],
            color=C_FUNC,
            stroke_width=3,
        )
        right_branch = axes.plot(
            self.f_right,
            x_range=[2.0, 3.3, 0.005],
            color=C_FUNC,
            stroke_width=3,
        )

        hole = Circle(radius=0.10, color=C_FUNC, stroke_width=2.5)
        hole.set_fill(WHITE, opacity=1)
        hole.move_to(axes.c2p(self.A, self.L))

        left_endpoint = Dot(
            axes.c2p(self.A, self.f_left(self.A)),
            color=C_FUNC,
            radius=0.10,
            z_index=5,
        )

        self.play(Create(left_branch), run_time=1.0)
        self.play(Create(right_branch), run_time=0.8)
        self.play(FadeIn(hole), FadeIn(left_endpoint))
        self.wait(0.4)

        #
        # STATIC GUIDE LINES: a and L
        #
        lbl_a = MathTex("a", color=C_TEXT, font_size=30).next_to(
            axes.c2p(self.A, 0), DOWN, buff=0.22
        )
        lbl_L = MathTex("L", color=C_LIMIT, font_size=30).next_to(
            axes.c2p(0, self.L), LEFT, buff=0.22
        )

        L_guide = DashedLine(
            axes.c2p(0, self.L),
            axes.c2p(self.A, self.L),
            color=C_LIMIT,
            stroke_width=1.8,
            dash_length=0.12,
        )
        a_guide = DashedLine(
            axes.c2p(self.A, 0),
            axes.c2p(self.A, self.L),
            color=C_TEXT,
            stroke_width=1.5,
            dash_length=0.12,
        )

        self.play(
            Create(L_guide),
            Create(a_guide),
            Write(lbl_a),
            Write(lbl_L),
            run_time=1.0,
        )
        self.wait(0.5)

        #
        # MOVING DOT: right-hand approach x → A⁺
        #
        x_t = ValueTracker(3.3)

        moving_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_t.get_value(), self.f_right(x_t.get_value())),
                color=C_POINT,
                radius=0.09,
                z_index=6,
            )
        )

        h_trace = always_redraw(
            lambda: DashedLine(
                axes.c2p(0, self.f_right(x_t.get_value())),
                axes.c2p(x_t.get_value(), self.f_right(x_t.get_value())),
                color=C_POINT,
                stroke_width=1.4,
                dash_length=0.09,
            )
        )

        v_trace = always_redraw(
            lambda: DashedLine(
                axes.c2p(x_t.get_value(), 0),
                axes.c2p(x_t.get_value(), self.f_right(x_t.get_value())),
                color=C_POINT,
                stroke_width=1.4,
                dash_length=0.09,
            )
        )

        y_dot = always_redraw(
            lambda: Dot(
                axes.c2p(0, self.f_right(x_t.get_value())),
                color=C_POINT,
                radius=0.07,
                z_index=6,
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

        self.play(
            FadeIn(moving_dot),
            FadeIn(h_trace),
            FadeIn(v_trace),
            FadeIn(y_dot),
            FadeIn(x_dot),
        )

        pt = axes.c2p(self.A, self.L)
        self.play(
            x_t.animate.set_value(2.001),
            self.camera.frame.animate.scale(0.35).move_to(pt),
            run_time=5.0,
            rate_func=smooth,
        )
        self.wait(2.5)

        self.play(Restore(self.camera.frame), run_time=2.0, rate_func=smooth)
        self.wait(1.5)
