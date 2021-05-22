from manimlib import *

A_COLOR = BLUE
B_COLOR = GREEN
C_COLOR = YELLOW
SIDE_COLORS = [A_COLOR, B_COLOR, C_COLOR]
U_COLOR = GREEN
V_COLOR = RED

class Introduction(Scene):
    def construct(self):
        text = Text("Pythagorean Theorem", font="Times New Roman", font_size=90)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))

class PythagorasTheorem(Scene):
    def construct(self):

        title = Tex("a", "^2", "+", "b", "^2", "=", "c", "^2")
        for color, char in zip(SIDE_COLORS, "abc"):
            title.set_color_by_tex(char, color)
        title.to_corner(UP + RIGHT)
        self.add(title)
       
        triples = [
            (3, 4, 5), 
            (5, 12, 13),
            (8, 15, 17),
            (7, 24, 25),
        ] 
          
        for a, b, c in triples:
            triangle = Polygon(
                ORIGIN, a*RIGHT, a*RIGHT+b*UP,
                stroke_width = 0,
                fill_color = WHITE,
                fill_opacity = 0.5
            )

            hyp_line = Line(ORIGIN, a*RIGHT+b*UP)
            elbow = VMobject()
            elbow.set_points_as_corners([LEFT, LEFT+UP, UP])
            elbow.set_width(0.2*triangle.get_width())
            elbow.move_to(triangle, DOWN+RIGHT)
            triangle.add(elbow)

            square = Square(side_length = 1)
            square_groups = VGroup()
            for n, color in zip([a, b, c], SIDE_COLORS):
                square_group = VGroup(*[
                    square.copy().shift(x*RIGHT + y*UP)
                    for x in range(n)
                    for y in range(n)
                ])
                square_group.set_stroke(color, width = 3)
                square_group.set_fill(color, opacity = 0.5)
                square_groups.add(square_group)

            a_square, b_square, c_square = square_groups
            a_square.move_to(triangle.get_bottom(), UP)
            b_square.move_to(triangle.get_right(), LEFT)
            c_square.move_to(hyp_line.get_center(), DOWN)
            c_square.rotate(
                hyp_line.get_angle(),
                about_point = hyp_line.get_center()
            )
            if c in [5, 13, 25]:
                if c == 5:
                    keys = list(range(0, 5, 2))
                elif c == 13:
                    keys = list(range(0, 13, 3))
                elif c == 25:
                    keys = list(range(0, 25, 4))
                i_list = [i for i in range(c**2) if (i%c) in keys and (i//c) in keys]
            else:
                i_list = list(range(a**2))
            not_i_list = list(filter(
                lambda i : i not in i_list,
                list(range(c**2)),
            ))
            c_square_parts = [
                VGroup(*[c_square[i] for i in i_list]),
                VGroup(*[c_square[i] for i in not_i_list]),
            ]
            full_group = VGroup(triangle, square_groups)
            full_group.set_height(4)
            full_group.center()
            full_group.to_edge(UP)

            equation = Tex(
                str(a), "^2", "+", str(b), "^2", "=", str(c), "^2"
            )
            for num, color in zip([a, b, c], SIDE_COLORS):
                equation.set_color_by_tex(str(num), color)
            equation.next_to(title, DOWN, MED_LARGE_BUFF)
            equation.shift_onto_screen()
            
            self.play(
                FadeIn(triangle),
            )
            self.play(LaggedStartMap(FadeIn, a_square))
            for start, target in zip([a_square, b_square], c_square_parts):
                mover = start.copy().set_fill(opacity = 0)
                target.set_color(start.get_color())
                self.play(ReplacementTransform(
                    mover, target,
                    run_time = 2,
                    path_arc = np.pi/2
                ))
            self.play(Write(equation))
            self.play(c_square.set_color, C_COLOR)
            self.wait()
            self.play(*list(map(FadeOut, [full_group, equation])))

class CompareToFermatsLastTheorem(Scene):
    def construct(self):
        expressions = [
            Tex(
                "a", "^%d"%d, "+", "b", "^%d"%d, 
                "=", "c", "^%d"%d
            )
            for d in range(2, 9)
        ]
        for expression in expressions:
            for char, color in zip("abc", SIDE_COLORS):
                expression.set_color_by_tex(char, color)
        square_expression = expressions[0]
        low_expression = expressions[1]
        square_expression.to_edge(UP, buff = 1.3)
        top_brace = Brace(square_expression, UP, buff = SMALL_BUFF)
        top_text = top_brace.get_text(
            "Abundant integer solutions", buff = SMALL_BUFF
        )
        low_brace = Brace(low_expression, DOWN, buff = SMALL_BUFF)
        low_text = low_brace.get_text(
            "No integer solutions", buff = SMALL_BUFF
        )
        low_text.set_color(RED)

        self.add(square_expression, top_brace, top_text)
        self.play(
            ReplacementTransform(
                square_expression.copy(),
                low_expression
            ),
        )
        self.wait(1)
        self.play(Transform(low_expression, expressions[2]))
        self.play(
            GrowFromCenter(low_brace),
            FadeIn(low_text),
        )
        for expression in expressions[4:]:
            self.play(Transform(low_expression, expression))
            self.wait(1) 
        

class BabylonianTablets(Scene):
    def construct(self):
        title = TexText("Plimpton 322 Tablets \\\\ (1800 BC)")
        title.to_corner(UP+LEFT)
        ac_pairs = [
            (119, 169),
            (3367, 4825),
            (4601, 6649),
            (12709, 18541),
            (65, 97),
            (319, 481),
            (2291, 3541),
            (799, 1249),
            (481, 769),
            (4961, 8161),
            (45, 75),
            (1679, 2929),
            (161, 289),
            (1771, 3229),
            (56, 106),
        ]
        triples = VGroup()
        for a, c in ac_pairs:
            b = int(np.sqrt(c**2 - a**2))
            tex = "%s^2 + %s^2 = %s^2"%tuple(
                map("{:,}".format, [a, b, c])
            )
            tex = tex.replace(",", "{,}")
            triple = Tex(tex)
            triples.add(triple)
        triples.arrange(DOWN, aligned_edge = LEFT)
        triples.set_height(FRAME_HEIGHT - LARGE_BUFF)
        triples.to_edge(RIGHT)

        self.add(title)
        self.wait()
        self.play(LaggedStartMap(FadeIn, triples, run_time = 5))
        self.wait()   