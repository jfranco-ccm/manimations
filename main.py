from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    A = 1.2  # base point x = a
    H0 = 1.0  # initial h (large offset)
    H1 = 0.02  # final h (tangent approximation)

    @staticmethod
    def f(x):
        """Smooth curve: f(x) = x²."""
        return x**2

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_FUNC   = "#1A6FC4"  # blue   – curve
        C_SECANT = "#B03A2E"  # red    – secant / tangent line
        C_OFFSET = "#1D6A39"  # green  – Δx and Δy offset markers
        C_POINT  = "#CA6F1E"  # orange – points on the curve
        C_TEXT   = "#1A1A1A"
        C_AXES   = "#555555"
        # fmt: on

        _base_w = self.camera.frame.width

        #
        # AXES
        #
        axes = Axes(
            x_range=[0, 3.0, 1],
            y_range=[0, 6.0, 1],
            x_length=5.2,
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
        # CURVE
        #
        graph = axes.plot(
            self.f, x_range=[0.05, 2.45, 0.01], color=C_FUNC, stroke_width=3
        )
        self.play(Create(graph), run_time=1.4)
        self.wait(0.3)

        #
        # BASE POINT  a  — radius scales with camera frame during zoom
        #
        pt_A = always_redraw(
            lambda: Dot(
                axes.c2p(self.A, self.f(self.A)),
                color=C_POINT,
                radius=0.09 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )
        lbl_a = MathTex("a", color=C_POINT, font_size=28).next_to(
            axes.c2p(self.A, 0), DOWN, buff=0.22
        )

        self.play(FadeIn(pt_A), Write(lbl_a), run_time=0.8)
        self.wait(0.3)

        #
        # OFFSET MARKERS  Δx and Δy
        #
        h_t = ValueTracker(self.H0)

        pt_B = always_redraw(
            lambda: Dot(
                axes.c2p(self.A + h_t.get_value(), self.f(self.A + h_t.get_value())),
                color=C_POINT,
                radius=0.09 * self.camera.frame.width / _base_w,
                z_index=6,
            )
        )

        lbl_ah = always_redraw(
            lambda: MathTex(r"a+h", color=C_POINT, font_size=24).next_to(
                axes.c2p(self.A + h_t.get_value(), 0), DOWN, buff=0.22
            )
        )

        fa_guide = DashedLine(
            axes.c2p(0, self.f(self.A)),
            axes.c2p(self.A, self.f(self.A)),
            color=C_POINT,
            stroke_width=1.2,
            dash_length=0.10,
        )
        lbl_fa = MathTex(r"f(a)", color=C_POINT, font_size=22).next_to(
            axes.c2p(0, self.f(self.A)), LEFT, buff=0.12
        )

        fah_guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(0, self.f(self.A + h_t.get_value())),
                axes.c2p(self.A + h_t.get_value(), self.f(self.A + h_t.get_value())),
                color=C_POINT,
                stroke_width=1.2,
                dash_length=0.10,
            )
        )
        lbl_fah = always_redraw(
            lambda: MathTex(r"f(a{+}h)", color=C_POINT, font_size=22).next_to(
                axes.c2p(0, self.f(self.A + h_t.get_value())), LEFT, buff=0.12
            )
        )

        dx_line = always_redraw(
            lambda: Line(
                axes.c2p(self.A, self.f(self.A)),
                axes.c2p(self.A + h_t.get_value(), self.f(self.A)),
                color=C_OFFSET,
                stroke_width=2.5,
            )
        )
        lbl_dx = always_redraw(
            lambda: MathTex(r"\Delta x", color=C_OFFSET, font_size=22).next_to(
                axes.c2p(self.A + h_t.get_value() / 2, self.f(self.A)),
                DOWN,
                buff=0.15,
            )
        )

        dy_line = always_redraw(
            lambda: Line(
                axes.c2p(self.A + h_t.get_value(), self.f(self.A)),
                axes.c2p(self.A + h_t.get_value(), self.f(self.A + h_t.get_value())),
                color=C_OFFSET,
                stroke_width=2.5,
            )
        )
        lbl_dy = always_redraw(
            lambda: MathTex(r"\Delta y", color=C_OFFSET, font_size=22).next_to(
                axes.c2p(
                    self.A + h_t.get_value(),
                    (self.f(self.A) + self.f(self.A + h_t.get_value())) / 2,
                ),
                RIGHT,
                buff=0.15,
            )
        )

        self.play(
            FadeIn(pt_B),
            Write(lbl_ah),
            Create(dx_line),
            Write(lbl_dx),
            Create(dy_line),
            Write(lbl_dy),
            Create(fa_guide),
            Write(lbl_fa),
            FadeIn(fah_guide),
            Write(lbl_fah),
            run_time=1.2,
        )
        self.wait(0.6)

        #
        # DIFFERENCE QUOTIENT FORMULA
        #
        formula_dq = MathTex(
            r"\frac{\Delta y}{\Delta x} = \frac{f(a+h)-f(a)}{h}",
            color=C_TEXT,
            font_size=28,
        ).to_corner(UR, buff=0.35)

        self.play(Write(formula_dq), run_time=1.0)
        self.wait(0.5)

        #
        # SECANT LINE — first between the two points, then extended to frame edges
        #
        def _slope(h):
            return (self.f(self.A + h) - self.f(self.A)) / h

        def _y_sec(h, x):
            return self.f(self.A) + _slope(h) * (x - self.A)

        X_LO, X_HI = -0.3, 3.2

        secant_short = Line(
            axes.c2p(self.A, self.f(self.A)),
            axes.c2p(self.A + self.H0, self.f(self.A + self.H0)),
            color=C_SECANT,
            stroke_width=2.5,
        )
        self.play(Create(secant_short), run_time=0.8)
        self.wait(0.3)

        secant_ext = Line(
            axes.c2p(X_LO, _y_sec(self.H0, X_LO)),
            axes.c2p(X_HI, _y_sec(self.H0, X_HI)),
            color=C_SECANT,
            stroke_width=2.5,
        )
        self.play(Transform(secant_short, secant_ext), run_time=1.2)
        self.wait(0.5)

        self.remove(secant_short)

        secant = always_redraw(
            lambda: Line(
                axes.c2p(X_LO, _y_sec(h_t.get_value(), X_LO)),
                axes.c2p(X_HI, _y_sec(h_t.get_value(), X_HI)),
                color=C_SECANT,
                stroke_width=2.5,
            )
        )
        self.add(secant)

        #
        # SHRINK h → 0  (offsets collapse, secant converges to tangent)
        # transform formula from difference quotient to derivative limit
        #
        formula_deriv = MathTex(
            r"f'(a) = \lim_{h \to 0} \frac{f(a+h)-f(a)}{h}",
            color=C_TEXT,
            font_size=28,
        ).to_corner(UR, buff=0.35)

        self.play(
            FadeOut(lbl_dx),
            FadeOut(lbl_dy),
            FadeOut(lbl_a),
            FadeOut(lbl_ah),
            FadeOut(lbl_fa),
            FadeOut(lbl_fah),
            FadeOut(fa_guide),
            FadeOut(fah_guide),
            Transform(formula_dq, formula_deriv),
            run_time=0.8,
        )
        self.play(
            h_t.animate.set_value(self.H1),
            run_time=5.0,
            rate_func=smooth,
        )
        self.wait(1.0)

        #
        # ZOOM IN to base point — tangent line locally matches the curve
        #
        pt = axes.c2p(self.A, self.f(self.A))
        self.play(
            self.camera.frame.animate.scale(0.12).move_to(pt),
            FadeOut(formula_dq),
            run_time=3.0,
            rate_func=smooth,
        )
        self.wait(2.5)

        self.play(Restore(self.camera.frame), run_time=2.0, rate_func=smooth)
        self.wait(1.5)
