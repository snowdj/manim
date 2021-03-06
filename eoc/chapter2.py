from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from scene import Scene
from scene.zoomed_scene import ZoomedScene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from eoc.chapter1 import OpeningQuote
from eoc.graph_scene import *


class Car(SVGMobject):
    CONFIG = {
        "file_name" : "Car", 
        "height" : 1,
        "color" : "#BBBBBB",
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_height(self.height)
        self.set_stroke(color = WHITE, width = 0)
        self.set_fill(self.color, opacity = 1)

        randy = Randolph(mode = "happy")
        randy.scale_to_fit_height(0.6*self.get_height())
        randy.stretch(0.8, 0)
        randy.look(RIGHT)
        randy.move_to(self)
        randy.shift(0.07*self.height*(RIGHT+UP))
        self.add_to_back(randy)

        orientation_line = Line(self.get_left(), self.get_right())
        orientation_line.set_stroke(width = 0)
        self.add(orientation_line)
        self.orientation_line = orientation_line


        self.add_treds_to_tires()

    def move_to(self, point_or_mobject):
        vect = rotate_vector(
            UP+LEFT, self.orientation_line.get_angle()
        )
        self.next_to(point_or_mobject, vect, buff = 0)
        return self

    def get_front_line(self):
        return DashedLine(
            self.get_corner(UP+RIGHT), 
            self.get_corner(DOWN+RIGHT),
            color = YELLOW,
            dashed_segment_length = 0.05,
        )

    def add_treds_to_tires(self):
        for tire in self.get_tires():
            radius = tire.get_width()/2
            center = tire.get_center()
            tred = Line(
                0.9*radius*RIGHT, 1.4*radius*RIGHT,
                stroke_width = 2,
                color = BLACK
            )
            tred.rotate_in_place(np.pi/4)
            for theta in np.arange(0, 2*np.pi, np.pi/4):
                new_tred = tred.copy()
                new_tred.rotate(theta)
                new_tred.shift(center)
                tire.add(new_tred)
        return self

    def get_tires(self):
        return self[1][1], self[1][3]

class MoveCar(ApplyMethod):
    def __init__(self, car, target_point, **kwargs):
        ApplyMethod.__init__(self, car.move_to, target_point, **kwargs)
        displacement = self.ending_mobject.get_right()-self.starting_mobject.get_right()
        distance = np.linalg.norm(displacement)
        tire_radius = car.get_tires()[0].get_width()/2
        self.total_tire_radians = -distance/tire_radius

    def update_mobject(self, alpha):
        ApplyMethod.update_mobject(self, alpha)
        if alpha == 0:
            return
        radians = alpha*self.total_tire_radians
        for tire in self.mobject.get_tires():
            tire.rotate_in_place(radians)

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            TexMobject(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )

class IncrementTest(Scene):
    def construct(self):
        num = TexMobject("0")
        num.shift(UP)
        self.play(IncrementNumber(num))
        self.dither()



############################

class Chapter2OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "So far as the theories of mathematics are about",
            "reality,", 
            "they are not",
            "certain;", 
            "so far as they are",
            "certain,", 
            "they are not about",
            "reality.",
        ],
        "highlighted_quote_terms" : {
            "reality," : BLUE,
            "certain;" : GREEN,
            "certain," : GREEN,
            "reality." : BLUE,
        },
        "author" : "Albert Einstein"
    }

class Introduction(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What is a derivative?"
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.dither()
        self.teacher_says(
            "It's actually a \\\\",
            "very subtle idea",
            target_mode = "well"
        )
        self.change_student_modes(None, "pondering", "thinking")
        self.dither()
        self.change_student_modes("erm")
        self.student_says(
            "Doesn't the derivative measure\\\\",
            "instantaneous rate of change", "?",
            student_index = 0,
        )
        self.dither()

        bubble = self.get_students()[0].bubble
        phrase = bubble.content[1]
        bubble.content.remove(phrase)
        self.play(
            phrase.center,
            phrase.scale, 1.5,
            phrase.to_edge, UP,
            FadeOut(bubble),
            FadeOut(bubble.content),
            *it.chain(*[
                [
                    pi.change_mode, mode,
                    pi.look_at, SPACE_HEIGHT*UP
                ]
                for pi, mode in zip(self.get_everyone(), [
                    "speaking", "pondering", "confused", "confused",
                ])
            ])
        )
        self.dither()
        change = VGroup(*phrase[-len("change"):])
        instantaneous = VGroup(*phrase[:len("instantaneous")])
        change_brace = Brace(change)
        change_description = change_brace.get_text(
            "Requires multiple \\\\ points in time"
        )
        instantaneous_brace = Brace(instantaneous)
        instantaneous_description = instantaneous_brace.get_text(
            "One point \\\\ in time"
        )
        clock = Clock()
        clock.next_to(change_description, DOWN)
        def get_clock_anim(run_time = 3):
            return ClockPassesTime(
                clock,
                hours_passed = 0.4*run_time,
                run_time = run_time,
            )
        self.play(FadeIn(clock))
        self.play(
            change.gradient_highlight, BLUE, YELLOW,
            GrowFromCenter(change_brace),
            Write(change_description),
            get_clock_anim()
        )
        self.play(get_clock_anim(1))
        stopped_clock = clock.copy()
        stopped_clock.next_to(instantaneous_description, DOWN)
        self.play(
            instantaneous.highlight, BLUE,
            GrowFromCenter(instantaneous_brace),
            Transform(change_description.copy(), instantaneous_description),
            clock.copy().next_to, instantaneous_description, DOWN,
            get_clock_anim(3)
        )
        self.play(get_clock_anim(6))

class FathersOfCalculus(Scene):
    CONFIG = {
        "names" : [
            "Barrow",
            "Newton", 
            "Leibniz",
            "Cauchy",
            "Weierstrass",
        ],
        "picture_height" : 2.5,
    }
    def construct(self):
        title = TextMobject("(A few) Fathers of Calculus")
        title.to_edge(UP)
        self.add(title)

        men = Mobject()
        for name in self.names:
            image = ImageMobject(name, invert = False)
            image.scale_to_fit_height(self.picture_height)
            title = TextMobject(name)
            title.scale(0.8)
            title.next_to(image, DOWN)
            image.add(title)
            men.add(image)
        men.arrange_submobjects(RIGHT, aligned_edge = UP)
        men.shift(DOWN)

        discover_brace = Brace(Mobject(*men[:3]), UP)
        discover = discover_brace.get_text("Discovered it")
        VGroup(discover_brace, discover).highlight(BLUE)
        rigor_brace = Brace(Mobject(*men[3:]), UP)
        rigor = rigor_brace.get_text("Made it rigorous")
        rigor.shift(0.1*DOWN)
        VGroup(rigor_brace, rigor).highlight(YELLOW)


        for man in men:
            self.play(FadeIn(man))
        self.play(
            GrowFromCenter(discover_brace),
            Write(discover, run_time = 1)
        )
        self.play(
            GrowFromCenter(rigor_brace),
            Write(rigor, run_time = 1)
        )
        self.dither()

class IntroduceCar(Scene):
    def construct(self):
        point_A = DOWN+4*LEFT
        point_B = DOWN+5*RIGHT
        A = Dot(point_A)
        B = Dot(point_B)
        line = Line(point_A, point_B)
        VGroup(A, B, line).highlight(WHITE)        
        for dot, tex in (A, "A"), (B, "B"):
            label = TexMobject(tex).next_to(dot, DOWN)
            dot.add(label)

        car = Car()
        car.move_to(point_A)
        front_line = car.get_front_line()

        time_label = TextMobject("Time (in seconds):", "0")
        time_label.shift(2*UP)

        distance_brace = Brace(line, UP)
        # distance_brace.set_fill(opacity = 0.5)
        distance = distance_brace.get_text("100m")

        self.add(A, B, line, car, time_label)
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))
        self.play(
            MoveCar(car, point_B, run_time = 10),
            IncrementNumber(time_label[1], run_time = 11)
        )
        front_line = car.get_front_line()
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))
        self.play(
            GrowFromCenter(distance_brace),
            Write(distance)
        )
        self.dither()
        self.play(
            car.move_to, point_A,
            FadeOut(time_label),
            FadeOut(distance_brace),
            FadeOut(distance)
        )
        graph_scene = GraphCarTrajectory(skip_animations = True)
        origin = graph_scene.graph_origin
        top = graph_scene.coords_to_point(0, 100)
        new_length = np.linalg.norm(top-origin)
        new_point_B = point_A + new_length*RIGHT

        group = VGroup(car, A, B, line)
        for mob in group:
            mob.generate_target()
        group.target = VGroup(*[m.target for m in group])
        B.target.shift(new_point_B - point_B)
        line.target.put_start_and_end_on(
            point_A, new_point_B
        )

        group.target.rotate(np.pi/2, about_point = point_A)
        group.target.shift(graph_scene.graph_origin - point_A)
        self.play(MoveToTarget(group, path_arc = np.pi/2))
        self.dither()

class GraphCarTrajectory(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10.01,
        "x_labeled_nums" : range(1, 11),
        "x_axis_label" : "Time (seconds)",
        "y_min" : 0,
        "y_max" : 110,
        "y_tick_frequency" : 10,
        "y_labeled_nums" : range(10, 110, 10),
        "y_axis_label" : "Distance traveled \\\\ (meters)",
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.graph_function(lambda t : 100*smooth(t/10.))
        origin = self.coords_to_point(0, 0)

        self.introduce_graph(graph, origin)
        self.comment_on_slope(graph, origin)
        self.show_velocity_graph()
        self.ask_critically_about_velocity()

    def introduce_graph(self, graph, origin):
        h_line, v_line = [
            Line(origin, origin, color = color, stroke_width = 2)
            for color in MAROON_B, YELLOW
        ]
        def h_update(h_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            t_axis_point = end[0]*RIGHT + origin[1]*UP
            h_line.put_start_and_end_on(t_axis_point, end)
        def v_update(v_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            d_axis_point = origin[0]*RIGHT + end[1]*UP
            v_line.put_start_and_end_on(d_axis_point, end)

        car = Car()
        car.rotate(np.pi/2)
        car.move_to(origin)
        self.add(car)
        self.play(
            ShowCreation(
                graph,
                rate_func = None,
            ),
            MoveCar(
                car, self.coords_to_point(0, 100),
            ),
            UpdateFromFunc(h_line, h_update),
            UpdateFromFunc(v_line, v_update),
            run_time = 10,
        )
        self.dither()
        self.play(*map(FadeOut, [h_line, v_line, car]))

        #Show example vertical distance
        h_update(h_line, 0.6)
        t_dot = Dot(h_line.get_start(), color = h_line.get_color())
        t_dot.save_state()
        t_dot.move_to(self.x_axis_label_mob)
        t_dot.set_fill(opacity = 0)
        dashed_h = DashedLine(*h_line.get_start_and_end())
        dashed_h.highlight(h_line.get_color())
        brace = Brace(dashed_h, RIGHT)
        brace_text = brace.get_text("Distance traveled")
        self.play(t_dot.restore)
        self.dither()
        self.play(ShowCreation(dashed_h))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.dither(2)
        self.play(*map(FadeOut, [t_dot, dashed_h, brace, brace_text]))

        #Name graph
        s_of_t = TexMobject("s(t)")
        s_of_t.next_to(
            graph.point_from_proportion(1), 
            DOWN+RIGHT,
            buff = SMALL_BUFF
        )
        s = s_of_t[0]
        d = TexMobject("d")
        d.move_to(s, DOWN)
        d.highlight(YELLOW)

        self.play(Write(s_of_t))
        self.dither()
        s.save_state()
        self.play(Transform(s, d))
        self.dither()
        self.play(s.restore)

    def comment_on_slope(self, graph, origin):
        delta_t = 1
        curr_time = 0
        ghost_line = Line(
            origin, 
            self.coords_to_point(delta_t, self.y_max)
        )
        rect = Rectangle().replace(ghost_line, stretch = True)
        rect.set_stroke(width = 0)
        rect.set_fill(BLUE, opacity = 0.3)
        def get_change_lines():
            p1 = self.input_to_graph_point(curr_time)
            p2 = self.input_to_graph_point(curr_time+delta_t)
            interim_point = p2[0]*RIGHT + p1[1]*UP
            delta_t_line = Line(p1, interim_point, color = YELLOW)
            delta_s_line = Line(interim_point, p2, color = MAROON_B)
            brace = Brace(delta_s_line, RIGHT, buff = SMALL_BUFF)
            return VGroup(delta_t_line, delta_s_line, brace)

        change_lines = get_change_lines()
        self.play(FadeIn(rect))
        self.dither()
        self.play(Write(change_lines))
        self.dither()
        for x in range(1, 10):
            curr_time = x
            new_change_lines = get_change_lines()
            self.play(
                rect.move_to, self.coords_to_point(curr_time, 0), DOWN+LEFT,
                Transform(change_lines, new_change_lines)
            )
            if curr_time == 5:
                text = change_lines[-1].get_text(
                    "$\\frac{\\text{meters}}{\\text{second}}$"
                )
                self.play(Write(text))
                self.dither()
                self.play(FadeOut(text))
            else:
                self.dither()
        self.play(*map(FadeOut, [rect, change_lines]))
        self.rect = rect

    def show_velocity_graph(self):
        velocity_graph = self.get_derivative_graph()

        self.play(ShowCreation(velocity_graph))
        def get_velocity_label(v_graph):
            result = self.label_graph(
                v_graph,
                label = "v(t)",
                direction = UP+RIGHT,
                proportion = 0.5,
                buff = SMALL_BUFF,
                animate = False,
            )
            self.remove(result)
            return result
        label = get_velocity_label(velocity_graph)
        self.play(Write(label))
        self.dither()
        self.rect.move_to(self.coords_to_point(0, 0), DOWN+LEFT)
        self.play(FadeIn(self.rect))
        self.dither()
        for time in 4.5, 9:
            self.play(
                self.rect.move_to, self.coords_to_point(time, 0), DOWN+LEFT
            )
            self.dither()
        self.play(FadeOut(self.rect))

        #Change distance and velocity graphs
        self.graph.save_state()
        velocity_graph.save_state()
        label.save_state()
        def shallow_slope(t):
            return 100*smooth(t/10., inflection = 4)
        def steep_slope(t):
            return 100*smooth(t/10., inflection = 25)
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph_funcs = [
            shallow_slope,
            steep_slope,
            double_smooth_graph_function,
        ]
        for graph_func in graph_funcs:
            new_graph = self.graph_function(
                graph_func,
                is_main_graph = False
            )
            self.remove(new_graph)
            new_velocity_graph = self.get_derivative_graph(graph = new_graph)
            new_velocity_label = get_velocity_label(new_velocity_graph)

            self.play(Transform(self.graph, new_graph))
            self.play(
                Transform(velocity_graph, new_velocity_graph),
                Transform(label, new_velocity_label),
            )
            self.dither(2)
        self.play(self.graph.restore)
        self.play(
            velocity_graph.restore,
            label.restore,
        )
        self.dither(2)

    def ask_critically_about_velocity(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        self.play(PiCreatureSays(morty,
            "Think critically about \\\\",
            "what velocity means."
        ))
        self.play(Blink(morty))
        self.dither()











































