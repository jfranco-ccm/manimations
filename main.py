from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    # ── tuneable parameters ───────────────────────────────────────────
    A = 0.0  # squeeze point:  g(x) ≤ f(x) ≤ h(x) and g(A)=h(A)=L
    L = 0.0

    @staticmethod
    def f(x):
        """Squeezed function: x² · sin(5x), stays between ±x²."""
        return x**2 * np.sin(5 * x)

    @staticmethod
    def g(x):
        """Lower bound: -x²."""
        return -(x**2)

    @staticmethod
    def h(x):
        """Upper bound: +x²."""
        return x**2

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_F     = "#1A6FC4"  # blue   – squeezed function f
        C_BOUND = "#1D6A39"  # green  – bounding functions g and h
        C_POINT = "#CA6F1E"  # orange – squeeze point
        C_FILL  = "#1D6A39"  # green  – shaded squeeze region
        C_TEXT  = "#1A1A1A"
        C_AXES  = "#555555"
        # fmt: on

        #
        # AXES
        #
        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=6.0,
            y_length=6.0,
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
        self.wait(0.2)

        #
        # BOUNDING CURVES  g(x) = -x²  and  h(x) = x²
        #
        curve_h = axes.plot(self.h, x_range=[-2.1, 2.1, 0.01], color=C_BOUND, stroke_width=2.5)
        curve_g = axes.plot(self.g, x_range=[-2.1, 2.1, 0.01], color=C_BOUND, stroke_width=2.5)

        lbl_h = MathTex(r"h(x)=x^2", color=C_BOUND, font_size=26).next_to(
            axes.c2p(1.5, self.h(1.5)), UR, buff=0.12
        )
        lbl_g = MathTex(r"g(x)=-x^2", color=C_BOUND, font_size=26).next_to(
            axes.c2p(1.5, self.g(1.5)), DR, buff=0.12
        )

        self.play(Create(curve_h), Create(curve_g), run_time=1.2)
        self.play(Write(lbl_h), Write(lbl_g), run_time=0.7)
        self.wait(0.4)

        #
        # SHADED REGION between g and h (the squeeze band)
        #
        region = axes.get_area(
            curve_h,
            x_range=[-2.1, 2.1],
            bounded_graph=curve_g,
            color=C_FILL,
            opacity=0.12,
        )

        self.play(FadeIn(region), run_time=0.8)
        self.wait(0.3)

        #
        # SQUEEZED FUNCTION  f(x) = x² sin(5x)
        #
        curve_f = axes.plot(self.f, x_range=[-2.1, 2.1, 0.008], color=C_F, stroke_width=2.8)

        lbl_f = MathTex(r"f(x)=x^2\sin(5x)", color=C_F, font_size=24).next_to(
            axes.c2p(-2.0, self.f(-2.0)), UL, buff=0.12
        )

        self.play(Create(curve_f), run_time=1.6)
        self.play(Write(lbl_f), run_time=0.6)
        self.wait(0.5)

        #
        # SQUEEZE POINT  (0, 0)
        # radius scales with camera frame so the dot stays small on screen during zoom
        #
        _base_w = self.camera.frame.width
        squeeze_dot = always_redraw(
            lambda: Dot(
                axes.c2p(self.A, self.L),
                color=C_POINT,
                radius=0.10 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )

        lbl_L = MathTex("L=0", color=C_POINT, font_size=28).next_to(
            axes.c2p(self.A, self.L), UR, buff=0.18
        )

        self.play(FadeIn(squeeze_dot), Write(lbl_L), run_time=0.8)
        self.wait(0.5)

        #
        # ZOOM IN to the squeeze point to show all three curves converging
        #
        pt = axes.c2p(self.A, self.L)

        self.play(
            FadeOut(lbl_L),
            self.camera.frame.animate.scale(0.18).move_to(pt),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(2.5)

        self.play(Restore(self.camera.frame), run_time=2.0, rate_func=smooth)
        self.wait(1.5)

