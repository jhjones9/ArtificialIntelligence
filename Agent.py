# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageOps, ImageFilter, ImageChops
#import numpy
from collections import Counter, defaultdict, OrderedDict


class Attributes(object):
    SHAPE = 'shape'
    SIZE = 'size'
    WIDTH = 'width'
    HEIGHT = 'height'
    FILL = 'fill'
    INSIDE = 'inside'
    ABOVE = 'above'
    ANGLE = 'angle'
    ALIGN = 'alignment'
    OVERLAPS = 'overlaps'
    LEFT_OF = 'left-of'


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    size_list = ['very small',
                 'small',
                 'medium',
                 'large',
                 'very large',
                 'huge']

    UNCHANGED = 'unchanged'
    FILLED = 'filled'
    RIGHT_FILLED = 'right-half'
    LEFT_FILLED = 'left-half'
    TOP_FILLED = 'top-half'
    BOTTOM_FILLED = 'bottom-half'
    ROTATED = 'rotated'
    REFLECTED = 'reflected'
    EXPANDED = 'expanded'
    CONTRACTED = 'contracted'
    DELETED = 'deleted'
    ADDED = 'added'
    MOVED_RIGHT = 'moved right'
    MOVED_LEFT = 'moved left'
    MOVED_UP = 'moved up'
    MOVED_DOWN = 'moved down'
    OVERLAP = 'overlaps'
    CHANGED = 'changed'
    PENALTY = 'penalty'
    ABOVE = 'above'

    rel = dict()
    rel[UNCHANGED] = 9
    rel[REFLECTED] = 8
    rel[ROTATED] = 7
    rel[EXPANDED] = 6
    rel[CONTRACTED] = -6
    rel[ADDED] = 5
    rel[DELETED] = -5
    rel[FILLED] = 4
    rel[RIGHT_FILLED] = 3
    rel[LEFT_FILLED] = -3
    rel[TOP_FILLED] = 2
    rel[BOTTOM_FILLED] = -2
    rel[ABOVE] = .5
    rel[MOVED_RIGHT] = 1
    rel[MOVED_LEFT] = -1
    rel[MOVED_UP] = 1.5
    rel[MOVED_DOWN] = -1.5
    rel[OVERLAP] = .25
    rel[CHANGED] = -9
    rel[PENALTY] = -6

    @staticmethod
    def get_object_keys(fig1, fig2):
        keys = zip(sorted(fig1.objects.keys()), sorted(fig2.objects.keys()))
        return keys

    def compare_shape(self, obj1, obj2, attr):
        if obj1.attributes[attr] == obj2.attributes[attr]:
            return self.UNCHANGED
        return self.CHANGED

    def compare_size(self, obj1, obj2, attr):
        if obj1.attributes[attr] != obj2.attributes[attr]:
            if obj1.attributes['shape'] == obj2.attributes['shape']:
                index1 = self.size_list.index(obj1.attributes['size'])
                index2 = self.size_list.index(obj2.attributes['size'])
                if index1 < index2:
                    return self.CONTRACTED
                return self.CONTRACTED
            return self.CHANGED
        return self.UNCHANGED

    def compare_fill(self, obj1, obj2, attr):
        obj1_fill = obj1.attributes[attr].split('-')
        obj2_fill = obj2.attributes[attr].split('-')
        if obj1_fill[0] != obj2_fill[0]:
            if obj2_fill[0] == 'right':
                return self.RIGHT_FILLED
            elif obj2_fill[0] == 'left':
                return self.LEFT_FILLED
            elif obj2_fill[0] == 'top':
                return self.TOP_FILLED
            elif obj2_fill[0] == 'bottom':
                return self.BOTTOM_FILLED
            return self.FILLED
        return self.UNCHANGED

    def compare_inside(self, obj1, obj2, attr):
        num_obj1 = int(len(obj1.attributes[attr]))
        num_obj2 = int(len(obj2.attributes[attr]))
        if num_obj1 > num_obj2:
            return self.DELETED
        elif num_obj1 < num_obj2:
            return self.ADDED
        return self.UNCHANGED

    def compare_width(self, obj1, obj2, attr):
        index1 = self.size_list.index(obj1.attributes[attr])
        index2 = self.size_list.index(obj2.attributes[attr])
        if index1 < index2:
            return self.EXPANDED
        elif index1 > index2:
            return self.CONTRACTED
        return self.UNCHANGED

    def compare_height(self, obj1, obj2, attr):
        index1 = self.size_list.index(obj1.attributes[attr])
        index2 = self.size_list.index(obj2.attributes[attr])
        if index1 < index2:
            return self.EXPANDED
        elif index1 > index2:
            return self.CONTRACTED
        return self.UNCHANGED

    @staticmethod
    def get_rotations(obj1_rot, obj2_rot):
        rot = abs(obj2_rot - obj1_rot)
        num_rots = rot / 90
        return num_rots

    def compare_left_of(self, obj1, obj2, attr):
        n1 = obj1.attributes[attr].split(',')
        n2 = obj2.attributes[attr].split(',')
        length1 = len(n1)
        length2 = len(n2)
        if length1 < length2:
            return self.DELETED
        elif length1 > length2:
            return self.ADDED
        return self.UNCHANGED

    def compare_above(self, obj1, obj2, attr):
        n1 = obj1.attributes[attr].split(',')
        n2 = obj2.attributes[attr].split(',')
        length1 = len(n1)
        length2 = len(n2)
        if length1 < length2:
            return self.DELETED
        elif length1 > length2:
            return self.ADDED
        return self.UNCHANGED

    def compare_attributes(self, obj1, obj2):
        analogy = []
        for attr in obj1.attributes:
            if attr in obj2.attributes:
                if attr == Attributes.SHAPE:
                    analogy.append(self.compare_shape(obj1, obj2, attr))
                elif attr == Attributes.SIZE:
                    analogy.append(self.compare_size(obj1, obj2, attr))
                elif attr == Attributes.WIDTH:
                    analogy.append(self.compare_width(obj1, obj2, attr))
                elif attr == Attributes.HEIGHT:
                    analogy.append(self.compare_height(obj1, obj2, attr))
                elif attr == Attributes.FILL:
                    analogy.append(self.compare_fill(obj1, obj2, attr))
                elif attr == Attributes.INSIDE:
                    obj1_in = int(len(obj1.attributes[attr]))
                    obj2_in = int(len(obj2.attributes[attr]))
                    if obj1_in > obj2_in:
                        for i in range(obj1_in):
                            analogy.append(self.DELETED)
                    elif obj1_in < obj2_in:
                        for i in range(obj2_in):
                            analogy.append(self.ADDED)
                    else:
                        analogy.append(self.UNCHANGED)
                elif attr == Attributes.ANGLE:
                    obj1_rot = int(obj1.attributes[attr])
                    obj2_rot = int(obj2.attributes[attr])
                    num_rots = self.get_rotations(obj1_rot, obj2_rot)
                    difference = int(abs(obj1_rot - obj2_rot))
                    if difference == 0:
                        analogy.append(self.UNCHANGED)
                        analogy.append(self.PENALTY)
                    else:
                        for i in range(num_rots):
                            analogy.append(self.ROTATED)
                elif attr == Attributes.ALIGN:
                    obj1_align = obj1.attributes[attr].split('-')
                    obj2_align = obj2.attributes[attr].split('-')
                    if obj1_align[0] != obj2_align[0]:
                        if obj2_align[0] == 'bottom':
                            analogy.append(self.MOVED_DOWN)
                        elif obj2_align[0] == 'top':
                            analogy.append(self.MOVED_UP)
                    if obj1_align[1] != obj2_align[1]:
                        if obj2_align[1] == 'left':
                            analogy.append(self.MOVED_LEFT)
                        elif obj2_align[1] == 'right':
                            analogy.append(self.MOVED_RIGHT)
                elif attr == Attributes.ABOVE:
                    analogy.append(self.UNCHANGED)
                elif attr == Attributes.OVERLAPS:
                    length1 = len(obj1.attributes[attr])
                    length2 = len(obj2.attributes[attr])
                    if length1 > 2:
                        length1 = length1 / 2 + 1
                    if length2 > 2:
                        length2 = length2 / 2 + 1
                    if length1 == length2:
                        analogy.append(self.UNCHANGED)
                    elif length1 > length2:
                        analogy.append(self.DELETED)
                    else:
                        analogy.append(self.ADDED)
                elif attr == Attributes.LEFT_OF:
                    analogy.append(self.UNCHANGED)
            else:
                if attr == Attributes.INSIDE:
                    obj1_in = int(len(obj1.attributes[attr]))
                    for i in range(obj1_in):
                        analogy.append(self.DELETED)
                else:
                    analogy.append(self.DELETED)
        for attr in obj2.attributes:
            if attr not in obj1.attributes:
                if attr == Attributes.INSIDE:
                    obj2_in = int(len(obj2.attributes[attr]))
                    for i in range(obj2_in):
                        analogy.append(self.ADDED)
                else:
                    analogy.append(self.ADDED)
            else:
                pass
        return analogy

    def get_verbal_transformation(self, fig1, fig2):
        transformation = []
        object_keys = self.get_object_keys(fig1, fig2)
        for k, v in object_keys:
            obj1 = fig1.objects[k]
            obj2 = fig2.objects[v]
            transformation.extend(self.compare_attributes(obj1, obj2))
        return transformation

    def get_visual_transformation(self, fig1, fig2):
        img_diff = ImageChops.difference(fig1, fig2).histogram()
        return img_diff

    def get_visual_score(self, trans_AB, trans_CX, trans_AC, trans_BX):
        pass

    def get_verbal_score(self, trans_AB, trans_CX, trans_AC, trans_BX):
        # Horizontal Transformations
        scores_AB = []
        scores_CX = []
        # Vertical Transformations
        scores_AC = []
        scores_BX = []
        # For each element, multiply the element by the value.
        # Get values for A->B
        for k, v in Counter(trans_AB).iteritems():
            scores_AB.append(self.rel[k] * v)
        # Get values for C->X
        for k, v in Counter(trans_CX).iteritems():
            scores_CX.append(self.rel[k] * v)
        # Get values for A->C
        for k, v in Counter(trans_AC).iteritems():
            scores_AC.append(self.rel[k] * v)
        # Get values for B->X
        for k, v in Counter(trans_BX).iteritems():
            scores_BX.append(self.rel[k] * v)

        # transformation_scores = [x + y for x, y in zip(scores_AB, scores_AC)]
        # solution_scores = [x + y for x, y in zip(scores_CX, scores_BX)]
        # Get the elements that are in common
        intersectionABCX = Counter(trans_AB) & Counter(trans_CX)
        # Get the difference between the two transformations
        differenceABCX = abs(sum(scores_AB) - sum(scores_CX))

        intersectionACBX = Counter(trans_AC) & Counter(trans_BX)
        differenceACBX = abs(sum(scores_AC) - sum(scores_BX))

        intersection = int(len(intersectionABCX) + len(intersectionACBX)) / 2
        difference = (differenceABCX + differenceACBX) / 2
        result = intersection - difference
        return result

    def get_row_score(self, trans1, trans2):
        scores1 = []
        scores2 = []
        for k, v in Counter(trans1).iteritems():
            scores1.append(self.rel[k] * v)
        for k, v in Counter(trans2).iteritems():
            scores2.append(self.rel[k] * v)

        print("\nTrans 1:")
        print(trans1)
        print("\nTrans 2:")
        print(trans2)

        intersection = Counter(trans1) & Counter(trans2)
        difference = abs(sum(scores1) - sum(scores2))
        result = int(len(intersection) - difference)
        return result

    def get_column_score(self, trans1, trans2):
        scores1 = []
        scores2 = []
        for k, v in Counter(trans1).iteritems():
            scores1.append(self.rel[k] * v)
        for k, v in Counter(trans2).iteritems():
            scores2.append(self.rel[k] * v)

        intersection = Counter(trans1) & Counter(trans2)
        difference = abs(sum(scores1) - sum(scores2))
        result = int(len(intersection) - difference)
        return result

    def get_max_score(self, scores1, scores2):
        maximum1 = max(scores1, key=scores1.get)
        maximum2 = max(scores2, key=scores2.get)
        max_score = max(scores1[maximum1], scores2[maximum2])
        if max_score == scores1[maximum1]:
            return int(maximum1)
        else:
            return int(maximum2)

    def get_max_scores(self, scores1, scores2, scores3):
        max1 = max(scores1, key=scores1.get)
        max2 = max(scores2, key=scores2.get)
        max3 = max(scores3, key=scores3.get)
        maximum1 = max(scores1[max1], scores2[max2])
        maximum2 = max(scores1[max1], scores3[max3])
        maximum3 = max(scores2[max2], scores3[max3])
        if maximum1 >= maximum2 and maximum1 >= maximum3:
            return int(max1)
        elif maximum2 >= maximum1 and maximum2 >= maximum3:
            return int(max2)
        else:
            return int(max3)

    def dsum(self, *dicts):
        ret = defaultdict(int)
        for d in dicts:
            for k, v in d.items():
                ret[k] += v
        return dict(ret)

    def get_diff(self, *dicts):
        ret = defaultdict(int)
        for d in dicts:
            for k, v in d.items():
                ret[k] -= v
        return dict(ret)

    def Solve(self,problem):
        answer = 1

        # Check if problem is a '2x2' matrix and has a verbal representation.
        if problem.problemType == '2x2' and problem.hasVerbal:
            print("\n")
            print(problem.name)
            print("\n")
            candidates = ['1', '2', '3', '4', '5', '6']

            figure_A = problem.figures['A']
            figure_B = problem.figures['B']
            figure_C = problem.figures['C']

            # Horizontal Transformation for A->B
            trans_AB = self.get_verbal_transformation(figure_A, figure_B)
            # Vertical Transformation for A->C
            trans_AC = self.get_verbal_transformation(figure_A, figure_C)
            # Diagonal Transformation for B->C
            trans_BC = self.get_verbal_transformation(figure_B, figure_C)
            # Get solutions for X (6 possible solutions)
            solutions = {figure: value for figure, value in problem.figures.iteritems()
                         if figure in candidates}
            # Horizontal transformations for C->X
            trans_CX = {x: self.get_verbal_transformation(figure_C, figure)
                        for x, figure in solutions.iteritems()}
            # Vertical Transformations for B->X
            trans_BX = {x: self.get_verbal_transformation(figure_B, figure)
                        for x, figure in solutions.iteritems()}
            # Diagonal transformation for A->X
            trans_AX = {x: self.get_verbal_transformation(figure_A, figure)
                        for x, figure in solutions.iteritems()}
            # Get the scores
            scores1 = {solution: self.get_row_score(trans_AB, transformation_CX)
                       for solution, transformation_CX in trans_CX.iteritems()}
            scores2 = {solution: self.get_column_score(trans_AC, transformation_BX)
                       for solution, transformation_BX in trans_BX.iteritems()}
            scores3 = {solution: self.get_row_score(trans_BC, transformation_AX)
                       for solution, transformation_AX in trans_AX.iteritems()}

            sum1 = self.dsum(scores1, scores2)
            sum2 = self.dsum(sum1, scores3)
            od = OrderedDict(sum2)
            answer = int(max(od.iteritems(), key=lambda x: x[1])[0])
            #answer = self.get_max_score(scores1, scores2)
            # Get answer: The score with the greatest value should be the correct answer
            #   since we take the intersection of two transformations and subtract the
            #   difference.
            #answer = int(max(scores1.iteritems(), key=lambda x: x[1])[0])
        # Solve for 3x3 matrices with verbal representation
        elif problem.problemType == '3x3' and problem.hasVerbal:
            print("\n")
            print(problem.name)
            print("\n")
            candidates = ['1', '2', '3', '4', '5', '6', '7', '8']

            figure_A = problem.figures['A']
            figure_B = problem.figures['B']
            figure_C = problem.figures['C']
            figure_D = problem.figures['D']
            figure_E = problem.figures['E']
            figure_F = problem.figures['F']
            figure_G = problem.figures['G']
            figure_H = problem.figures['H']

            # Horizontal
            trans_AB = self.get_verbal_transformation(figure_A, figure_B)
            trans_BC = self.get_verbal_transformation(figure_B, figure_C)
            trans_ABC = trans_AB + trans_BC
            scoreABC = self.get_row_score(trans_AB, trans_BC)

            trans_DE = self.get_verbal_transformation(figure_D, figure_E)
            trans_EF = self.get_verbal_transformation(figure_E, figure_F)
            trans_DEF = trans_DE + trans_EF
            scoreDEF = self.get_row_score(trans_DE, trans_EF)

            trans_GH = self.get_verbal_transformation(figure_G, figure_H)
            # Vertical
            trans_AD = self.get_verbal_transformation(figure_A, figure_D)
            trans_DG = self.get_verbal_transformation(figure_D, figure_G)
            trans_ADG = trans_AD + trans_DG
            scoreADG = self.get_row_score(trans_AD, trans_DG)

            trans_BE = self.get_verbal_transformation(figure_B, figure_E)
            trans_EH = self.get_verbal_transformation(figure_E, figure_H)
            trans_BEH = trans_BE + trans_EH
            scoreBEH = self.get_column_score(trans_BE, trans_EH)

            trans_CF = self.get_verbal_transformation(figure_C, figure_F)
            # Diagonal
            trans_AE = self.get_verbal_transformation(figure_A, figure_E)

            trans_CE = self.get_verbal_transformation(figure_C, figure_E)
            trans_EG = self.get_verbal_transformation(figure_E, figure_G)
            trans_GEC = trans_CE + trans_EG
            scoreCEG = self.get_row_score(trans_CE, trans_EG)

            trans_FH = self.get_verbal_transformation(figure_F, figure_H)

            # Get solutions for X (8 possible solutions)
            solutions = {figure: value for figure, value in problem.figures.iteritems()
                         if figure in candidates}

            # Horizontal transformations for H->X
            trans_HX = {x: self.get_verbal_transformation(figure_H, figure)
                        for x, figure in solutions.iteritems()}
            # Vertical transformations for F->X
            trans_FX = {x: self.get_verbal_transformation(figure_F, figure)
                        for x, figure in solutions.iteritems()}
            # Diagonal transformations for E->X
            trans_EX = {x: self.get_verbal_transformation(figure_E, figure)
                        for x, figure in solutions.iteritems()}
            # Get the scores for Horizontal and Vertical transformations
            scoresEFHX = {solution: self.get_row_score(trans_EF, transformation_HX)
                       for solution, transformation_HX in trans_HX.iteritems()}
            scoresEHFX = {solution: self.get_column_score(trans_EH, transformation_FX)
                       for solution, transformation_FX in trans_FX.iteritems()}
            scoresAEX = {solution: self.get_row_score(trans_AE, transformation_EX)
                       for solution, transformation_EX in trans_EX.iteritems()}
            scoresGHX = {solution: self.get_row_score(trans_GH, transformation_EX)
                         for solution, transformation_EX in trans_EX.iteritems()}
            scoresCFX = {solution: self.get_column_score(trans_CF, transformation_FX)
                         for solution, transformation_FX in trans_FX.iteritems()}
            scoresFHEX = {solution: self.get_row_score(trans_FH, transformation_EX)
                          for solution, transformation_EX in trans_EX.iteritems()}
           # answer = self.get_max_scores(scoresEFHX, scoresEHFX, scoresAEX)
            # Get answer: The score with the greatest value should be the correct answer
            #   since we take the intersection of two transformations and subtract the
            #   difference.
            #answer = int(max(scores.iteritems(), key=lambda x: x[1])[0])

            # Problem structure: A->B->C
            #                    D->E->F
            #                    G->H->X?
            sum1 = self.dsum(scoresEHFX, scoresEFHX)
            sum2 = self.dsum(sum1, scoresAEX)
            sum3 = self.dsum(sum2, scoresGHX)
            sum4 = self.dsum(sum3, scoresCFX)
            od = OrderedDict(sum3)
            print("\n")
            print(od)
            items = od.items()
            items.reverse()
            final_od = OrderedDict(items)
            print(final_od)
            answer = int(max(final_od.iteritems(), key=lambda x: x[1])[0])
            if (trans_AB == trans_BC and trans_DE == trans_EF):
                result = max(scoresFHEX.iteritems(), key=lambda x: x[1])[0]
                print(result)
                scoresFHEX[result] -= 1
                answer = int(max(scoresFHEX.iteritems(), key=lambda x: x[1])[0])
        return answer