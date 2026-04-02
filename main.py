from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    # ── tuneable parameters ───────────────────────────────────────────
    T_START = 0.0
    T_END = 2 * PI

    @staticmethod
    def f1(t):
        """First component: f₁(t) = cos(t)."""
        return np.cos(t)

    @staticmethod
    def f2(t):
        """Second component: f₂(t) = sin(t)."""
        return np.sin(t)

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_CURVE  = "#1A6FC4"  # blue   – parametric curve / f
        C_F1     = "#B03A2E"  # red    – first component f₁
        C_F2     = "#1D6A39"  # green  – second component f₂
        C_DOT    = "#CA6F1E"  # orange – moving point
        C_TEXT   = "#1A1A1A"
        C_AXES   = "#555555"
        # fmt: on

        #
        # LAYOUT: three axis groups
        # [f₁ graph] | [ℝ² parametric plane] | [f₂ graph]
        #

        # central plane: the ℝ² output space
        plane = Axes(
            x_range=[-1.6, 1.6, 1],
            y_range=[-1.6, 1.6, 1],
            x_length=3.4,
            y_length=3.4,
            axis_config={
                "color": C_AXES,
                "include_tip": True,
                "tip_length": 0.15,
                "stroke_width": 1.8,
            },
            x_axis_config={},
            y_axis_config={},
        ).move_to(ORIGIN)

        # left axes: f₁(t) = cos(t)
        ax1 = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[-1.4, 1.4, 1],
            x_length=3.2,
            y_length=3.4,
            axis_config={
                "color": C_AXES,
                "include_tip": True,
                "tip_length": 0.15,
                "stroke_width": 1.8,
            },
            x_axis_config={},
            y_axis_config={},
        ).next_to(plane, LEFT, buff=0.55)

        # right axes: f₂(t) = sin(t)
        ax2 = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[-1.4, 1.4, 1],
            x_length=3.2,
            y_length=3.4,
            axis_config={
                "color": C_AXES,
                "include_tip": True,
                "tip_length": 0.15,
                "stroke_width": 1.8,
            },
            x_axis_config={},
            y_axis_config={},
        ).next_to(plane, RIGHT, buff=0.55)

        # axis labels
        lbl_x = MathTex("f_1", color=C_F1, font_size=22).next_to(
            plane.get_x_axis(), RIGHT, buff=0.10
        )
        lbl_y = MathTex("f_2", color=C_F2, font_size=22).next_to(
            plane.get_y_axis(), UP, buff=0.10
        )
        lbl_t1 = MathTex("t", color=C_TEXT, font_size=22).next_to(
            ax1.get_x_axis(), RIGHT, buff=0.10
        )
        lbl_t2 = MathTex("t", color=C_TEXT, font_size=22).next_to(
            ax2.get_x_axis(), RIGHT, buff=0.10
        )
        lbl_c1 = MathTex("f_1", color=C_F1, font_size=22).next_to(
            ax1.get_y_axis(), UP, buff=0.10
        )
        lbl_c2 = MathTex("f_2", color=C_F2, font_size=22).next_to(
            ax2.get_y_axis(), UP, buff=0.10
        )

        # panel headers — placed to upper-right of each graph to avoid y-axis label overlap
        hdr_plane = MathTex(r"\mathbb{R}^2", color=C_TEXT, font_size=26).next_to(
            lbl_y, UR, buff=0.08
        )
        hdr_f1 = MathTex(r"f_1(t)=\cos t", color=C_F1, font_size=22).next_to(
            lbl_c1, UR, buff=0.08
        )
        hdr_f2 = MathTex(r"f_2(t)=\sin t", color=C_F2, font_size=22).next_to(
            lbl_c2, UR, buff=0.08
        )

        self.play(
            Create(plane),
            Create(ax1),
            Create(ax2),
            Write(lbl_x),
            Write(lbl_y),
            Write(lbl_t1),
            Write(lbl_t2),
            Write(lbl_c1),
            Write(lbl_c2),
            run_time=1.4,
        )
        self.play(Write(hdr_plane), Write(hdr_f1), Write(hdr_f2), run_time=0.8)
        self.wait(0.3)

        #
        # STATIC CURVES
        #

        # parametric circle in the ℝ² plane
        circle = ParametricFunction(
            lambda t: plane.c2p(self.f1(t), self.f2(t)),
            t_range=[0, 2 * PI, 0.02],
            color=C_CURVE,
            stroke_width=2.8,
        )

        # f₁(t) = cos(t) on left axes
        curve_f1 = ax1.plot(
            self.f1, x_range=[0, 2 * PI, 0.02], color=C_F1, stroke_width=2.8
        )

        # f₂(t) = sin(t) on right axes
        curve_f2 = ax2.plot(
            self.f2, x_range=[0, 2 * PI, 0.02], color=C_F2, stroke_width=2.8
        )

        self.play(Create(circle), run_time=1.6)
        self.wait(0.3)
        self.play(Create(curve_f1), Create(curve_f2), run_time=1.4)
        self.wait(0.5)

        #
        # FORMULAS
        #
        formula_f = MathTex(
            r"f(t) = (f_1(t),\, f_2(t))",
            color=C_TEXT,
            font_size=24,
        ).to_edge(DOWN, buff=0.45)

        formula_proj = MathTex(
            r"f_i = \pi_i \circ f",
            color=C_TEXT,
            font_size=24,
        ).next_to(formula_f, RIGHT, buff=0.55)

        self.play(Write(formula_f), run_time=0.9)
        self.wait(0.3)

        #
        # MOVING DOT: traces f(t) in all three panels simultaneously
        #
        t_tracker = ValueTracker(self.T_START)

        _base_w = self.camera.frame.width

        # dot on the parametric circle
        dot_plane = always_redraw(
            lambda: Dot(
                plane.c2p(
                    self.f1(t_tracker.get_value()), self.f2(t_tracker.get_value())
                ),
                color=C_DOT,
                radius=0.09 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )

        # dot tracing f₁ on left axes
        dot_f1 = always_redraw(
            lambda: Dot(
                ax1.c2p(t_tracker.get_value(), self.f1(t_tracker.get_value())),
                color=C_F1,
                radius=0.08 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )

        # dot tracing f₂ on right axes
        dot_f2 = always_redraw(
            lambda: Dot(
                ax2.c2p(t_tracker.get_value(), self.f2(t_tracker.get_value())),
                color=C_F2,
                radius=0.08 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )

        # π₁ projection: vertical dashed line from plane dot to x-axis
        proj1 = always_redraw(
            lambda: DashedLine(
                plane.c2p(
                    self.f1(t_tracker.get_value()), self.f2(t_tracker.get_value())
                ),
                plane.c2p(self.f1(t_tracker.get_value()), 0),
                color=C_F1,
                stroke_width=1.4,
                dash_length=0.09,
            )
        )

        # π₂ projection: horizontal dashed line from plane dot to y-axis
        proj2 = always_redraw(
            lambda: DashedLine(
                plane.c2p(
                    self.f1(t_tracker.get_value()), self.f2(t_tracker.get_value())
                ),
                plane.c2p(0, self.f2(t_tracker.get_value())),
                color=C_F2,
                stroke_width=1.4,
                dash_length=0.09,
            )
        )

        # shadow dots on the plane axes
        shadow_x = always_redraw(
            lambda: Dot(
                plane.c2p(self.f1(t_tracker.get_value()), 0),
                color=C_F1,
                radius=0.07,
                z_index=5,
            )
        )
        shadow_y = always_redraw(
            lambda: Dot(
                plane.c2p(0, self.f2(t_tracker.get_value())),
                color=C_F2,
                radius=0.07,
                z_index=5,
            )
        )

        # π₁ and π₂ labels — offset from the midpoint of each projection line
        lbl_pi1 = always_redraw(
            lambda: MathTex(r"\pi_1", color=C_F1, font_size=18).next_to(
                plane.c2p(
                    self.f1(t_tracker.get_value()), self.f2(t_tracker.get_value()) * 0.5
                ),
                LEFT,
                buff=0.10,
            )
        )
        lbl_pi2 = always_redraw(
            lambda: MathTex(r"\pi_2", color=C_F2, font_size=18).next_to(
                plane.c2p(
                    self.f1(t_tracker.get_value()) * 0.5, self.f2(t_tracker.get_value())
                ),
                UP,
                buff=0.10,
            )
        )

        self.play(
            FadeIn(dot_plane),
            FadeIn(dot_f1),
            FadeIn(dot_f2),
            FadeIn(proj1),
            FadeIn(proj2),
            FadeIn(shadow_x),
            FadeIn(shadow_y),
            FadeIn(lbl_pi1),
            FadeIn(lbl_pi2),
            run_time=0.9,
        )
        self.play(Write(formula_proj), run_time=0.8)
        self.wait(0.4)

        #
        # ANIMATE: dot travels the full circle, all three panels in sync
        #
        self.play(
            t_tracker.animate.set_value(self.T_END),
            run_time=7.0,
            rate_func=linear,
        )
        self.wait(1.5)
