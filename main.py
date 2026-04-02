from manim import *
import numpy as np


class LimitDefinition(MovingCameraScene):
    # fmt: off
    A = 1.0
    L = 1.0                             # limit value at x = A
    F = staticmethod(lambda x: x**2)    # function to plot
    EPS_0 = 0.55                        # initial epsilon
    EPS_1 = 0.09                        # final epsilon
    # fmt: on

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.frame.save_state()

        # fmt: off
        C_FUNC = "#1A6FC4"   # blue   - graph
        C_EPS = "#B03A2E"    # red    - epsilon band
        C_DELTA = "#1D6A39"  # green  - delta band
        C_POINT = "#CA6F1E"  # orange - limit point
        C_TEXT = "#1A1A1A"
        C_AXES = "#555555"
        # fmt: on

        #
        # AXES with ticks and labels
        #
        axes = Axes(
            x_range=[0, 2.5, 1],
            y_range=[0, 2.5, 1],
            x_length=5.4,
            y_length=5.4,
            axis_config={
                "color": C_AXES,
                "include_tip": True,
                "tip_length": 0.20,
                "stroke_width": 2,
            },
            x_axis_config={
                "numbers_to_include": [1, 2],
                "numbers_with_elongated_ticks": [1, 2],
            },
            y_axis_config={
                "numbers_to_include": [1, 2],
                "numbers_with_elongated_ticks": [1, 2],
            },
        ).shift(DOWN * 0.3)

        for n in [*axes.get_x_axis().numbers, *axes.get_y_axis().numbers]:
            n.set_color(C_TEXT)

        ax_x = MathTex("x", color=C_TEXT, font_size=26).next_to(
            axes.get_x_axis(), RIGHT, buff=0.12
        )
        ax_y = MathTex("y", color=C_TEXT, font_size=26).next_to(
            axes.get_y_axis(), UP, buff=0.12
        )

        self.play(Create(axes), Write(ax_x), Write(ax_y), run_time=1.2)

        graph = axes.plot(
            self.F,
            x_range=[0.05, 2.12, 0.01],
            color=C_FUNC,
            stroke_width=3,
        )
        g_lbl = MathTex(r"f(x)=x^2", color=C_FUNC, font_size=30).next_to(
            axes.c2p(2.05, self.F(2.05)), UR, buff=0.10
        )

        self.play(Create(graph, run_time=1.4), Write(g_lbl))
        self.wait(0.25)

        #
        # LIMIT POINT (a, L) with dashed guide lines
        #
        pt = axes.c2p(self.A, self.L)
        dot = Dot(pt, color=C_POINT, radius=0.09, z_index=5)

        h_guide = DashedLine(
            axes.c2p(0, self.L), pt, color=C_POINT, stroke_width=1.8, dash_length=0.13
        )
        v_guide = DashedLine(
            axes.c2p(self.A, 0), pt, color=C_POINT, stroke_width=1.8, dash_length=0.13
        )

        lbl_a = MathTex("a", color=C_POINT, font_size=30).next_to(
            axes.c2p(self.A, 0), DOWN, buff=0.20
        )
        lbl_L = MathTex("L", color=C_POINT, font_size=30).next_to(
            axes.c2p(0, self.L), LEFT, buff=0.20
        )

        self.play(
            Create(h_guide),
            Create(v_guide),
            FadeIn(dot),
            Write(lbl_a),
            Write(lbl_L),
        )
        self.wait(0.3)

        #
        # EPSILON-DELTA BANDS
        #
        eps_t = ValueTracker(self.EPS_0)

        _x0 = axes.c2p(0, 0)[0]
        _x1 = axes.c2p(2.4, 0)[0]
        _y0 = axes.c2p(0, 0)[1]
        _y1 = axes.c2p(0, 2.4)[1]

        def _delta(e: float) -> float:
            dr = np.sqrt(self.L + e) - self.A
            dl = self.A - np.sqrt(max(self.L - e, 1e-6))
            return min(dr, dl) * 0.88

        def mk_eps_band():
            e = eps_t.get_value()
            yt = axes.c2p(0, self.L + e)[1]
            yb = axes.c2p(0, self.L - e)[1]
            return Rectangle(
                width=_x1 - _x0,
                height=yt - yb,
                fill_color=C_EPS,
                fill_opacity=0.18,
                stroke_color=C_EPS,
                stroke_width=1.5,
            ).move_to([(_x0 + _x1) / 2, (yt + yb) / 2, 0])

        def mk_eps_dashes():
            e = eps_t.get_value()
            return VGroup(
                DashedLine(
                    axes.c2p(0, self.L + e),
                    axes.c2p(2.4, self.L + e),
                    color=C_EPS,
                    stroke_width=1.8,
                    dash_length=0.10,
                ),
                DashedLine(
                    axes.c2p(0, self.L - e),
                    axes.c2p(2.4, self.L - e),
                    color=C_EPS,
                    stroke_width=1.8,
                    dash_length=0.10,
                ),
            )

        def mk_eps_labels():
            e = eps_t.get_value()
            return VGroup(
                MathTex(r"L+\varepsilon", color=C_EPS, font_size=20).next_to(
                    axes.c2p(0, self.L + e), LEFT, buff=0.10
                ),
                MathTex(r"L-\varepsilon", color=C_EPS, font_size=20).next_to(
                    axes.c2p(0, self.L - e), LEFT, buff=0.10
                ),
            )

        def mk_delta_band():
            d = _delta(eps_t.get_value())
            xl = axes.c2p(self.A - d, 0)[0]
            xr = axes.c2p(self.A + d, 0)[0]
            return Rectangle(
                width=xr - xl,
                height=_y1 - _y0,
                fill_color=C_DELTA,
                fill_opacity=0.18,
                stroke_color=C_DELTA,
                stroke_width=1.5,
            ).move_to([(xl + xr) / 2, (_y0 + _y1) / 2, 0])

        def mk_delta_dashes():
            d = _delta(eps_t.get_value())
            return VGroup(
                DashedLine(
                    axes.c2p(self.A - d, 0),
                    axes.c2p(self.A - d, 2.4),
                    color=C_DELTA,
                    stroke_width=1.8,
                    dash_length=0.10,
                ),
                DashedLine(
                    axes.c2p(self.A + d, 0),
                    axes.c2p(self.A + d, 2.4),
                    color=C_DELTA,
                    stroke_width=1.8,
                    dash_length=0.10,
                ),
            )

        def mk_delta_labels():
            d = _delta(eps_t.get_value())
            return VGroup(
                MathTex(r"a-\delta", color=C_DELTA, font_size=20).next_to(
                    axes.c2p(self.A - d, 0), DOWN, buff=0.12
                ),
                MathTex(r"a+\delta", color=C_DELTA, font_size=20).next_to(
                    axes.c2p(self.A + d, 0), DOWN, buff=0.12
                ),
            )

        eps_band = always_redraw(mk_eps_band)
        eps_dashes = always_redraw(mk_eps_dashes)
        eps_labels = always_redraw(mk_eps_labels)
        dlt_band = always_redraw(mk_delta_band)
        dlt_dashes = always_redraw(mk_delta_dashes)
        dlt_labels = always_redraw(mk_delta_labels)

        self.play(FadeIn(eps_band), Create(eps_dashes), FadeIn(eps_labels))
        self.wait(0.3)

        self.play(FadeIn(dlt_band), Create(dlt_dashes), FadeIn(dlt_labels))
        self.wait(0.5)

        #
        # ZOOM IN on (a, L)
        #
        self.play(
            self.camera.frame.animate.scale(0.38).move_to(pt),
            run_time=2.6,
            rate_func=smooth,
        )
        self.wait(1.8)

        self.play(
            Restore(self.camera.frame),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(0.4)

        #
        # SHRINK EPSILON + ZOOM IN
        #

        self.play(
            eps_t.animate.set_value(self.EPS_1),
            self.camera.frame.animate.scale(0.30).move_to(pt),
            run_time=4.5,
            rate_func=smooth,
        )
        self.wait(2.0)

        self.play(
            Restore(self.camera.frame),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(2.5)
